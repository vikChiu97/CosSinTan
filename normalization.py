# normalization.py

import numpy as np


class Normalization:
    """
    Collection of static methods for 1D signal normalization.

    Convention:
      - Each method returns y_normalized (same shape as y).
      - Normalization.apply(...) returns (x, y_normalized, info)

    'info' is a dict with the constants used (min/max/mean/std/norms),
    which can help for debugging or reproducibility.
    """

    _EPS = 1e-12

    @staticmethod
    def apply(x, y, method="none", **kwargs):
        """
        Dispatch normalization method.

        Parameters
        ----------
        x : array-like
            X axis values (passed through unchanged).
        y : array-like
            Signal values.
        method : str
            One of: None, Min-Max, Z-Score, L1, L2, Standard Normal Variate (SNV)

        Returns
        -------
        x : np.ndarray
        y_norm : np.ndarray
        info : dict
            constants used in normalization
        """
        x = np.asarray(x)
        y = np.asarray(y, dtype=float)

        name = (method or "").strip().lower()
        name = name.replace("–", "-").replace("—", "-")

        info = {"method": name}

        if name in ("none", ""):
            y_norm = y.copy()

        elif name in ("min-max", "minmax", "min max"):
            y_norm, info2 = Normalization.min_max(y)
            info.update(info2)

        elif name in ("z-score", "zscore", "z score", "standardize", "standardization"):
            y_norm, info2 = Normalization.z_score(y)
            info.update(info2)

        elif name in ("l1", "l1 norm", "l1-normalize", "l1 normalize"):
            y_norm, info2 = Normalization.l1(y)
            info.update(info2)

        elif name in ("l2", "l2 norm", "l2-normalize", "l2 normalize"):
            y_norm, info2 = Normalization.l2(y)
            info.update(info2)

        elif name in ("standard normal variate", "snv"):
            y_norm, info2 = Normalization.snv(y)
            info.update(info2)

        else:
            raise ValueError(f"Unknown normalization method: {method}")

        return x, y_norm, info

    # -----------------------------
    # Normalization methods
    # -----------------------------
    @staticmethod
    def min_max(y):
        """
        Min-max scaling to [0, 1]:
          y' = (y - min) / (max - min)
        """
        y = np.asarray(y, dtype=float)
        y_min = np.nanmin(y)
        y_max = np.nanmax(y)
        denom = y_max - y_min

        if not np.isfinite(denom) or abs(denom) < Normalization._EPS:
            # Flat or invalid -> return zeros (shape preserved)
            y_norm = np.zeros_like(y, dtype=float)
        else:
            y_norm = (y - y_min) / denom

        info = {"min": float(y_min), "max": float(y_max), "denom": float(denom)}
        return y_norm, info

    @staticmethod
    def z_score(y):
        """
        Z-score standardization:
          y' = (y - mean) / std
        Uses population std (ddof=0). Flat -> zeros.
        """
        y = np.asarray(y, dtype=float)
        mu = np.nanmean(y)
        sigma = np.nanstd(y, ddof=0)

        if not np.isfinite(sigma) or sigma < Normalization._EPS:
            y_norm = np.zeros_like(y, dtype=float)
        else:
            y_norm = (y - mu) / sigma

        info = {"mean": float(mu), "std": float(sigma)}
        return y_norm, info

    @staticmethod
    def l1(y):
        """
        L1 vector normalization:
          y' = y / sum(|y|)
        """
        y = np.asarray(y, dtype=float)
        norm = np.nansum(np.abs(y))

        if not np.isfinite(norm) or norm < Normalization._EPS:
            y_norm = np.zeros_like(y, dtype=float)
        else:
            y_norm = y / norm

        info = {"l1": float(norm)}
        return y_norm, info

    @staticmethod
    def l2(y):
        """
        L2 vector normalization:
          y' = y / sqrt(sum(y^2))
        """
        y = np.asarray(y, dtype=float)
        norm = np.sqrt(np.nansum(y * y))

        if not np.isfinite(norm) or norm < Normalization._EPS:
            y_norm = np.zeros_like(y, dtype=float)
        else:
            y_norm = y / norm

        info = {"l2": float(norm)}
        return y_norm, info

    @staticmethod
    def snv(y):
        """
        Standard Normal Variate (SNV):
          y' = (y - mean(y)) / std(y)
        Typically applied per-spectrum (which is exactly this in 1D).
        Uses sample std (ddof=1). Flat -> zeros.
        """
        y = np.asarray(y, dtype=float)

        mu = np.nanmean(y)
        # ddof=1 needs at least 2 points; if not, std becomes nan
        sigma = np.nanstd(y, ddof=1) if y.size >= 2 else np.nan

        if not np.isfinite(sigma) or sigma < Normalization._EPS:
            y_norm = np.zeros_like(y, dtype=float)
        else:
            y_norm = (y - mu) / sigma

        info = {"mean": float(mu), "std": float(sigma), "ddof": 1}
        return y_norm, info
