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
        ...
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
    # airPLS
    # -----------------------------
    @staticmethod
    def airPLS(y, lam=1e5, porder=2, itermax=50, conv_threshold=1e-3):
        """
        Asymmetric reweighted penalized least squares (airPLS).

        Parameters
        ----------
        y : array-like
            Input signal.
        lam : float
            Smoothness parameter (lambda). Higher gives smoother baseline.
        porder : int
            Difference order (usually 2).
        itermax : int
            Maximum iterations.
        conv_threshold : float
            Convergence threshold on total weight change.

        Returns
        -------
        baseline : np.ndarray
        """
        y = np.asarray(y, dtype=float)
        n = y.size

        # Difference matrix
        D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(n, n - 2))
        D = lam * D.dot(D.transpose())

        w = np.ones(n)
        for i in range(itermax):
            W = sparse.spdiags(w, 0, n, n)
            Z = W + D
            z = spsolve(Z, w * y)

            diff = y - z
            # Negative residuals get higher weights (assumes peaks are positive)
            w_new = np.where(diff > 0, 0.0, np.exp(i * np.abs(diff) / diff.std()))

            # Convergence check
            if np.linalg.norm(w_new - w, 1) / np.linalg.norm(w, 1) < conv_threshold:
                w = w_new
                break
            w = w_new

        return z

    # -----------------------------
    # Rubber band (convex hull)
    # -----------------------------
    @staticmethod
    def rubberband(x, y):
        """
        Rubber band baseline using lower convex hull.

        Parameters
        ----------
        x, y : array-like

        Returns
        -------
        baseline : np.ndarray
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        # Ensure x is increasing
        order = np.argsort(x)
        x = x[order]
        y = y[order]

        # Compute lower hull indices
        hull = [0, 1]
        for i in range(2, len(x)):
            hull.append(i)
            while len(hull) >= 3:
                x1, y1 = x[hull[-3]], y[hull[-3]]
                x2, y2 = x[hull[-2]], y[hull[-2]]
                x3, y3 = x[hull[-1]], y[hull[-1]]

                # Area sign to check convexity
                cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
                if cross <= 0:
                    # Remove middle point if hull bends upwards
                    hull.pop(-2)
                else:
                    break

        hull = np.array(hull, dtype=int)
        baseline = np.interp(x, x[hull], y[hull])

        # Undo sorting to match original order
        baseline_unsorted = np.empty_like(baseline)
        baseline_unsorted[order] = baseline
        return baseline_unsorted

    # -----------------------------
    # Polynomial baseline
    # -----------------------------
    @staticmethod
    def polynomial(x, y, order=3):
        """
        Global polynomial fit.

        Parameters
        ----------
        x, y : array-like
        order : int
            Polynomial degree (typical 1–5).

        Returns
        -------
        baseline : np.ndarray
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        # Simple polyfit; for real spectroscopy you often mask peaks first
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

        Parameters
        ----------
        x, y : array-like
        n_knots : int
            Number of interior knot points.
        s : float or None
            Smoothing factor.
        k : int
            Spline degree (default cubic).

        Returns
        -------
        baseline : np.ndarray
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        # Ensure x is strictly increasing for spline fitting
        order = np.argsort(x)
        x_sorted = x[order]
        y_sorted = y[order]

        # Max allowable number of interior knots for LSQUnivariateSpline
        max_knots = max(0, len(x_sorted) - (k + 1))
        n_knots = max(0, min(n_knots, max_knots))

        if n_knots < 1:
            # Fall back to a global smoothing spline
            spline = UnivariateSpline(x_sorted, y_sorted, s=s, k=k)
            baseline_sorted = spline(x_sorted)
        else:
            x_min, x_max = x_sorted.min(), x_sorted.max()
            # Interior knots strictly between min and max
            knots = np.linspace(x_min, x_max, n_knots + 2)[1:-1]
            spline = LSQUnivariateSpline(x_sorted, y_sorted, knots, k=k)
            baseline_sorted = spline(x_sorted)

        # Undo sorting to match original order
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

        Parameters
        ----------
        y : array-like
        window_length : int
            Odd integer. Larger window gives smoother baseline.
        polyorder : int
            Polynomial order inside the S-G filter.

        Returns
        -------
        baseline : np.ndarray
        """
        y = np.asarray(y, dtype=float)
        # Ensure window_length is valid
        if window_length < 3:
            window_length = 3
        if window_length % 2 == 0:
            window_length += 1
        if window_length > y.size:
            window_length = y.size if y.size % 2 == 1 else y.size - 1
        if polyorder >= window_length:
            polyorder = window_length - 1

        return savgol_filter(y, window_length=window_length, polyorder=polyorder)
