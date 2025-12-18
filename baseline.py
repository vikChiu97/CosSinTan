# baseline.py

import numpy as np

from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline, LSQUnivariateSpline


class Baseline:
    """
    Collection of static methods for 1D baseline estimation and correction.

    Convention: each method returns the estimated baseline (same shape as y).
    Baseline.apply(...) returns (x, y_corrected, baseline).
    """

    # -----------------------------
    # Public dispatch method
    # -----------------------------
    @staticmethod
    def apply(x, y, method="none", **kwargs):
        x = np.asarray(x)
        y = np.asarray(y)

        # Normalize name and dashes
        name = (method or "").strip().lower()
        name = name.replace("–", "-").replace("—", "-")  # en/em dash → hyphen

        if name in ("none", ""):
            baseline = np.zeros_like(y, dtype=float)
        elif name == "airpls":
            baseline = Baseline.airPLS(y, **kwargs)
        elif name in ("rubber band", "rubberband"):
            baseline = Baseline.rubberband(x, y, **kwargs)
        elif name == "polynomial":
            baseline = Baseline.polynomial(x, y, **kwargs)
        elif name in ("piecewise spline", "piecewise_spline", "spline"):
            baseline = Baseline.piecewise_spline(x, y, **kwargs)
        elif name in ("savitzky-golay", "savgol", "savitzky golay"):
            baseline = Baseline.savgol(y, **kwargs)
        else:
            raise ValueError(f"Unknown baseline method: {method}")

        y_corr = y - baseline
        return x, y_corr, baseline

    # -----------------------------
    # Whittaker smoother helper (used by airPLS)
    # -----------------------------
    @staticmethod
    def _whittaker_smooth(x, w, lam, differences=2):
        """
        Penalized least squares baseline (Whittaker smoother).

        Solves: (W + lam * D.T D) z = W x
        where D is a finite-difference operator of given order.

        Parameters
        ----------
        x : array-like
        w : array-like (weights, same length as x)
        lam : float
        differences : int
            finite difference order (porder)
        """
        x = np.asarray(x, dtype=float).ravel()
        w = np.asarray(w, dtype=float).ravel()
        m = x.size

        if m < 3:
            return x.copy()

        lam = float(lam)
        differences = int(max(1, differences))

        # Build D as sparse difference operator of requested order
        D = sparse.eye(m, format="csc")
        for _ in range(differences):
            D = D[1:] - D[:-1]

        W = sparse.diags(w, 0, shape=(m, m), format="csc")
        A = W + (lam * (D.T @ D))
        b = W @ x

        z = spsolve(A, b)
        return np.asarray(z, dtype=float)

    # -----------------------------
    # airPLS
    # -----------------------------
    @staticmethod
    def airPLS(y, lam=1e5, porder=2, itermax=50, conv_threshold=1e-3):
        """
        Adaptive iteratively reweighted penalized least squares (airPLS).

        Parameters
        ----------
        y : array-like
            Input signal.
        lam : float
            Smoothness parameter (lambda). Higher gives smoother baseline.
        porder : int
            Difference order (controls stiffness). Typical: 1–3.
        itermax : int
            Maximum iterations.
        conv_threshold : float
            Convergence threshold relative to sum(|y|).

        Returns
        -------
        baseline : np.ndarray
        """
        y = np.asarray(y, dtype=float).ravel()
        n = y.size
        if n < 3:
            return y.copy()

        lam = float(lam)
        porder = int(max(1, porder))
        itermax = int(max(1, itermax))
        conv_threshold = float(max(0.0, conv_threshold))

        w = np.ones(n, dtype=float)
        y_abs_sum = np.sum(np.abs(y)) + 1e-12  # avoid div-by-zero

        z = y.copy()
        for i in range(1, itermax + 1):
            z = Baseline._whittaker_smooth(y, w, lam, differences=porder)
            d = y - z

            neg = d[d < 0]
            if neg.size == 0:
                break

            dssn = np.abs(neg.sum())  # sum of negative residuals magnitude
            if dssn <= 1e-12:
                break

            # Convergence check (common airPLS criterion)
            if dssn < (conv_threshold * y_abs_sum):
                break

            # Update weights: only negative residuals get weight
            w[:] = 0.0
            exp_arg = i * np.abs(d[d < 0]) / dssn
            # Guard against overflow for large i/lambda or tiny dssn
            exp_arg = np.clip(exp_arg, 0.0, 50.0)
            w[d < 0] = np.exp(exp_arg)

            # Endpoint boosting (helps edge behavior)
            w0_arg = i * np.max(np.abs(d[d < 0])) / dssn
            w0 = float(np.exp(min(50.0, w0_arg)))
            w[0] = w0
            w[-1] = w0

        return z

    # -----------------------------
    # Rubber band (convex hull)
    # -----------------------------
    @staticmethod
    def rubberband(x, y):
        """
        Rubber band baseline using lower convex hull.
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if x.size < 2:
            return y.copy()

        # Ensure x is increasing
        order = np.argsort(x)
        x_sorted_full = x[order]
        y_sorted_full = y[order]

        # Handle duplicate x values (np.interp requires increasing xp with no duplicates).
        # For a "lower envelope" baseline, keeping the minimum y per x is the safest choice.
        x_sorted = x_sorted_full
        y_sorted = y_sorted_full
        if np.any(np.diff(x_sorted) == 0):
            uniq_x, inv = np.unique(x_sorted, return_inverse=True)
            y_min = np.full(uniq_x.shape, np.inf, dtype=float)
            np.minimum.at(y_min, inv, y_sorted)
            x_sorted = uniq_x
            y_sorted = y_min
            if x_sorted.size < 2:
                return y.copy()

        # Compute lower hull indices
        hull = [0, 1]
        for i in range(2, len(x_sorted)):
            hull.append(i)
            while len(hull) >= 3:
                x1, y1 = x_sorted[hull[-3]], y_sorted[hull[-3]]
                x2, y2 = x_sorted[hull[-2]], y_sorted[hull[-2]]
                x3, y3 = x_sorted[hull[-1]], y_sorted[hull[-1]]

                cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
                if cross <= 0:
                    hull.pop(-2)
                else:
                    break

        hull = np.array(hull, dtype=int)
        baseline_unique = np.interp(x_sorted, x_sorted[hull], y_sorted[hull])
        baseline_sorted = (
            np.interp(x_sorted_full, x_sorted, baseline_unique)
            if baseline_unique.size != x_sorted_full.size
            else baseline_unique
        )

        # Undo sorting
        baseline = np.empty_like(baseline_sorted)
        baseline[order] = baseline_sorted
        return baseline

    # -----------------------------
    # Polynomial baseline
    # -----------------------------
    @staticmethod
    def polynomial(x, y, order=3):
        """
        Global polynomial fit.
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        order = int(max(0, order))
        if x.size <= order:
            # Not enough points to fit that order; degrade gracefully
            order = max(0, x.size - 1)

        coeffs = np.polyfit(x, y, order)
        p = np.poly1d(coeffs)
        return p(x)

    # -----------------------------
    # Piecewise spline baseline
    # -----------------------------
    @staticmethod
    def piecewise_spline(x, y, n_knots=10, s=None, k=3):
        """
        Piecewise smoothing spline baseline using LSQUnivariateSpline
        when possible; otherwise falls back to UnivariateSpline.
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        k = int(max(1, k))

        order = np.argsort(x)
        x_sorted = x[order]
        y_sorted = y[order]

        # If x has duplicates, spline can fail. This is a quick, safe fix:
        # collapse duplicates by averaging y at the same x.
        if np.any(np.diff(x_sorted) == 0):
            uniq_x, inv = np.unique(x_sorted, return_inverse=True)
            accum = np.zeros_like(uniq_x, dtype=float)
            counts = np.zeros_like(uniq_x, dtype=float)
            np.add.at(accum, inv, y_sorted)
            np.add.at(counts, inv, 1.0)
            x_sorted = uniq_x
            y_sorted = accum / np.maximum(counts, 1.0)

        if x_sorted.size < (k + 2):
            spline = UnivariateSpline(x_sorted, y_sorted, s=s, k=min(k, max(1, x_sorted.size - 1)))
            baseline_sorted = spline(x_sorted)
        else:
            max_knots = max(0, x_sorted.size - (k + 1))
            n_knots = int(max(0, min(n_knots, max_knots)))

            if n_knots < 1:
                spline = UnivariateSpline(x_sorted, y_sorted, s=s, k=k)
                baseline_sorted = spline(x_sorted)
            else:
                x_min, x_max = x_sorted.min(), x_sorted.max()
                knots = np.linspace(x_min, x_max, n_knots + 2)[1:-1]
                spline = LSQUnivariateSpline(x_sorted, y_sorted, knots, k=k)
                baseline_sorted = spline(x_sorted)

        # Map back to original x positions
        # If we had to de-duplicate x, use interpolation onto original x.
        if baseline_sorted.size != np.asarray(x)[order].size:
            baseline_on_sorted = np.interp(np.asarray(x)[order], x_sorted, baseline_sorted)
            baseline = np.empty_like(baseline_on_sorted)
            baseline[order] = baseline_on_sorted
            return baseline

        baseline = np.empty_like(baseline_sorted)
        baseline[order] = baseline_sorted
        return baseline

    # -----------------------------
    # Savitzky–Golay baseline
    # -----------------------------
    @staticmethod
    def savgol(y, window_length=51, polyorder=3):
        """
        Savitzky–Golay smoothing used as a baseline estimate.
        """
        y = np.asarray(y, dtype=float)

        window_length = int(window_length)
        polyorder = int(polyorder)

        if window_length < 3:
            window_length = 3
        if window_length % 2 == 0:
            window_length += 1
        if window_length > y.size:
            window_length = y.size if y.size % 2 == 1 else max(3, y.size - 1)

        if polyorder < 0:
            polyorder = 0
        if polyorder >= window_length:
            polyorder = window_length - 1

        return savgol_filter(y, window_length=window_length, polyorder=polyorder)
