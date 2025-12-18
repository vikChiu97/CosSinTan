import sys
import pandas as pd
import numpy as np

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui_main import Ui_MainWindow
from baseline import Baseline
from normalization import Normalization


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.df = None

        # ---- Aliases ----
        self.openButton = self.ui.openButton
        self.fileLabel = self.ui.fileLabel
        self.plotWidget = self.ui.plotWidget
        self.updateButton = self.ui.updateButton

        self.xAxisLine = self.ui.xAxisLine
        self.yAxisLine = self.ui.yAxisLine
        self.titleLine = self.ui.titleLine

        self.baselineBox = self.ui.baselineBox
        self.tabWidget = self.ui.tabWidget

        # NEW: normalization dropdown
        self.normalizationComboBox = self.ui.normalizationComboBox

        # airPLS controls
        self.airLambdaSpinBox = self.ui.airLambdaSpinBox
        self.airPorderSlider = self.ui.airPorderSlider
        self.airItermaxSpinBox = self.ui.airItermaxSpinBox

        # Polynomial controls
        self.polyOrderSlider = self.ui.polyOrderSlider

        # Piecewise controls
        self.piecewiseKnotsSpinBox = self.ui.piecewiseKnotsSpinBox
        self.piecewiseDegreeSlider = self.ui.piecewiseDegreeSlider

        # Savitzky controls
        self.savitzkyWinLenSpinBox = self.ui.savitzkyWinLenSpinBox
        self.savitzkyPolyorderSlider = self.ui.savitzkyPolyorderSlider

        # ---- Set sane defaults (only in main.py) ----
        self.airLambdaSpinBox.setValue(1e5)
        self.airPorderSlider.setValue(2)
        self.airItermaxSpinBox.setValue(50)

        self.polyOrderSlider.setValue(3)

        self.piecewiseKnotsSpinBox.setValue(10)
        self.piecewiseDegreeSlider.setValue(3)

        # Savitzky: enforce odd window length via main.py
        self.savitzkyWinLenSpinBox.setValue(51)  # must be odd
        self.savitzkyPolyorderSlider.setValue(3)

        self._fixing_savgol_winlen = False
        self.savitzkyWinLenSpinBox.valueChanged.connect(self._enforce_odd_savgol_winlen)
        self.savitzkyPolyorderSlider.valueChanged.connect(self._clamp_savgol_polyorder)

        # ---- Matplotlib canvas ----
        self.figure = Figure(figsize=(5, 4))
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Plot will show here")
        self.canvas = FigureCanvas(self.figure)

        layout = self.plotWidget.layout()
        if layout is None:
            layout = QVBoxLayout(self.plotWidget)
            layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        # ---- Signals ----
        self.openButton.clicked.connect(self.open_file)
        self.updateButton.clicked.connect(self.update_plot_and_processing)

        # Optional UX: when dropdown changes, switch to the right tab
        self.baselineBox.currentIndexChanged.connect(self._sync_tab_to_baseline)

        # sync once at startup
        self._sync_tab_to_baseline()

    # ---------- Small string normalizer ----------
    @staticmethod
    def _norm_name(s: str) -> str:
        s = (s or "").strip().lower()
        return s.replace("–", "-").replace("—", "-")

    # ---------- UX helpers ----------
    def _sync_tab_to_baseline(self):
        """
        Make the tab follow the baseline dropdown.
        Assumes tab order: airPLS, Polynomial, Piecewise, Savitzky-Golay.
        """
        name = self._norm_name(self.baselineBox.currentText())

        # Methods with no extra parameters: disable the settings tabs to avoid confusion.
        if name in ("none", "", "rubber band", "rubberband"):
            self.tabWidget.setEnabled(False)
            return
        self.tabWidget.setEnabled(True)

        if name == "airpls":
            self.tabWidget.setCurrentIndex(0)
        elif name == "polynomial":
            self.tabWidget.setCurrentIndex(1)
        elif name in ("piecewise spline", "piecewise"):
            self.tabWidget.setCurrentIndex(2)
        elif name in ("savitzky-golay", "savitzky golay", "savgol"):
            self.tabWidget.setCurrentIndex(3)

    def _enforce_odd_savgol_winlen(self, v: int):
        if self._fixing_savgol_winlen:
            return
        if v % 2 == 0:
            self._fixing_savgol_winlen = True
            self.savitzkyWinLenSpinBox.setValue(v + 1)
            self._fixing_savgol_winlen = False
        self._clamp_savgol_polyorder()

    def _clamp_savgol_polyorder(self):
        win = int(self.savitzkyWinLenSpinBox.value())
        current = int(self.savitzkyPolyorderSlider.value())
        if current >= win:
            self.savitzkyPolyorderSlider.setValue(max(1, win - 1))

    # ---------- File loading ----------
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel or CSV file",
            "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*.*)",
        )
        if not file_path:
            return

        try:
            if file_path.lower().endswith((".xlsx", ".xls")):
                self.df = pd.read_excel(file_path)
            elif file_path.lower().endswith(".csv"):
                self.df = pd.read_csv(file_path)
            else:
                QMessageBox.critical(self, "Unsupported file", "Please choose an Excel or CSV file.")
                return
        except Exception as e:
            QMessageBox.critical(self, "Error reading file", str(e))
            return

        if self.df.shape[1] < 2:
            QMessageBox.critical(self, "Not enough columns", "File needs at least 2 columns (first vs second).")
            return

        self.fileLabel.setText(file_path)
        self.plot_first_two_columns_raw()

    def plot_first_two_columns_raw(self):
        col_x = self.df.columns[0]
        col_y = self.df.columns[1]
        x = self.df[col_x].values
        y = self.df[col_y].values

        self.ax.clear()
        self.ax.plot(x, y)

        default_x_label = str(col_x)
        default_y_label = str(col_y)
        default_title = f"{col_x} vs {col_y}"

        self.ax.set_xlabel(default_x_label)
        self.ax.set_ylabel(default_y_label)
        self.ax.set_title(default_title)
        self.ax.grid(True)

        self.xAxisLine.setText(default_x_label)
        self.yAxisLine.setText(default_y_label)
        self.titleLine.setText(default_title)

        self.canvas.draw_idle()

    # ---------- Normalization helper (apply same constants to baseline overlay) ----------
    def _apply_norm_with_info(self, y, norm_name: str, info: dict):
        y = np.asarray(y, dtype=float)
        eps = 1e-12
        n = self._norm_name(norm_name)

        if n in ("none", ""):
            return y

        if n in ("min-max", "minmax", "min max"):
            denom = float(info.get("denom", 0.0))
            y_min = float(info.get("min", 0.0))
            if not np.isfinite(denom) or abs(denom) < eps:
                return np.zeros_like(y, dtype=float)
            return (y - y_min) / denom

        if n in ("z-score", "zscore", "z score", "standardize", "standardization"):
            mu = float(info.get("mean", 0.0))
            sigma = float(info.get("std", 0.0))
            if not np.isfinite(sigma) or sigma < eps:
                return np.zeros_like(y, dtype=float)
            return (y - mu) / sigma

        if n in ("l1", "l1 norm", "l1-normalize", "l1 normalize"):
            l1 = float(info.get("l1", 0.0))
            if not np.isfinite(l1) or l1 < eps:
                return np.zeros_like(y, dtype=float)
            return y / l1

        if n in ("l2", "l2 norm", "l2-normalize", "l2 normalize"):
            l2 = float(info.get("l2", 0.0))
            if not np.isfinite(l2) or l2 < eps:
                return np.zeros_like(y, dtype=float)
            return y / l2

        if n in ("standard normal variate", "snv"):
            mu = float(info.get("mean", 0.0))
            sigma = float(info.get("std", 0.0))
            if not np.isfinite(sigma) or sigma < eps:
                return np.zeros_like(y, dtype=float)
            return (y - mu) / sigma

        # Fallback: if a new method name slips in, just return unchanged
        return y

    # ---------- Update plot ----------
    def update_plot_and_processing(self):
        if self.df is None:
            QMessageBox.warning(self, "No data loaded", "Please load a file before updating the plot.")
            return

        col_x = self.df.columns[0]
        col_y = self.df.columns[1]
        x = self.df[col_x].values
        y = self.df[col_y].values

        # baseline selection
        method_text = self.baselineBox.currentText() or "None"
        method_norm = self._norm_name(method_text)

        # normalization selection
        norm_text = self.normalizationComboBox.currentText() or "None"
        norm_norm = self._norm_name(norm_text)

        x_label = self.xAxisLine.text().strip() or str(col_x)
        y_label = self.yAxisLine.text().strip() or str(col_y)
        title = self.titleLine.text().strip() or f"{col_x} vs {col_y}"

        # 1) Baseline correction
        try:
            if method_norm in ("none", ""):
                x_vals = x
                y_corr = y
                baseline = None

            elif method_norm == "airpls":
                lam = float(self.airLambdaSpinBox.value())
                porder = int(self.airPorderSlider.value())
                itermax = int(self.airItermaxSpinBox.value())
                x_vals, y_corr, baseline = Baseline.apply(x, y, method=method_text, lam=lam, porder=porder, itermax=itermax)

            elif method_norm in ("rubber band", "rubberband"):
                x_vals, y_corr, baseline = Baseline.apply(x, y, method=method_text)

            elif method_norm == "polynomial":
                order = int(self.polyOrderSlider.value())
                x_vals, y_corr, baseline = Baseline.apply(x, y, method=method_text, order=order)

            elif method_norm in ("piecewise spline", "piecewise", "piecewise_spline", "spline"):
                n_knots = int(self.piecewiseKnotsSpinBox.value())
                k = int(self.piecewiseDegreeSlider.value())
                x_vals, y_corr, baseline = Baseline.apply(x, y, method=method_text, n_knots=n_knots, k=k)

            elif method_norm in ("savitzky-golay", "savitzky golay", "savgol"):
                window_length = int(self.savitzkyWinLenSpinBox.value())
                polyorder = int(self.savitzkyPolyorderSlider.value())
                if window_length % 2 == 0:
                    window_length += 1
                if polyorder >= window_length:
                    polyorder = window_length - 1
                x_vals, y_corr, baseline = Baseline.apply(x, y, method=method_text, window_length=window_length, polyorder=polyorder)

            else:
                raise ValueError(f"Unknown baseline selection: {method_text}")

        except Exception as e:
            QMessageBox.critical(self, "Baseline error", f"Failed to apply baseline method '{method_text}':\n{e}")
            x_vals = x
            y_corr = y
            baseline = None

        # 2) Normalization (applied AFTER baseline correction)
        y_plot = y_corr
        baseline_plot = baseline

        try:
            if norm_norm not in ("none", ""):
                _, y_plot, info = Normalization.apply(x_vals, y_corr, method=norm_text)

                if baseline is not None:
                    baseline_plot = self._apply_norm_with_info(baseline, norm_text, info)

        except Exception as e:
            QMessageBox.critical(self, "Normalization error", f"Failed to apply normalization '{norm_text}':\n{e}")
            y_plot = y_corr
            baseline_plot = baseline

        # 3) Plot
        self.ax.clear()
        sig_label = "Signal" if norm_norm in ("none", "") else f"Signal ({norm_text})"
        self.ax.plot(x_vals, y_plot, label=sig_label)

        if baseline_plot is not None:
            base_label = "Baseline" if norm_norm in ("none", "") else f"Baseline ({norm_text})"
            self.ax.plot(x_vals, baseline_plot, linestyle="--", alpha=0.6, label=base_label)
            self.ax.legend()

        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        self.ax.grid(True)
        self.canvas.draw_idle()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1162, 720)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
