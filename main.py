import sys
import pandas as pd

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
        self.savitzkyWinLenSpinBox.setValue(51)          # must be odd
        self.savitzkyPolyorderSlider.setValue(3)

        self._fixing_savgol_winlen = False
        self.savitzkyWinLenSpinBox.valueChanged.connect(self._enforce_odd_savgol_winlen)

        # Optional: keep polyorder < window_length (prevents Baseline.savgol auto-clamping surprises)
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
        self.updateButton.clicked.connect(self.update_plot_and_baseline)

        # Optional UX: when dropdown changes, switch to the right tab
        self.baselineBox.currentIndexChanged.connect(self._sync_tab_to_baseline)

        # sync once at startup
        self._sync_tab_to_baseline()

    # ---------- UX helpers ----------
    def _sync_tab_to_baseline(self):
        """
        Make the tab follow the baseline dropdown.
        Assumes tab order: airPLS, Polynomial, Piecewise, Savitzky-Golay
        (from your latest ui_main.py snippet).
        """
        name = (self.baselineBox.currentText() or "").strip().lower()
        name = name.replace("–", "-").replace("—", "-")

        if name == "airpls":
            self.tabWidget.setCurrentIndex(0)
        elif name == "polynomial":
            self.tabWidget.setCurrentIndex(1)
        elif name in ("piecewise spline", "piecewise"):
            self.tabWidget.setCurrentIndex(2)
        elif name in ("savitzky-golay", "savitzky golay", "savgol"):
            self.tabWidget.setCurrentIndex(3)

    def _enforce_odd_savgol_winlen(self, v: int):
        """
        If user types an even value, snap to the next odd.
        This avoids modal errors and ensures always-valid input.
        """
        if self._fixing_savgol_winlen:
            return
        if v % 2 == 0:
            self._fixing_savgol_winlen = True
            self.savitzkyWinLenSpinBox.setValue(v + 1)
            self._fixing_savgol_winlen = False
        self._clamp_savgol_polyorder()

    def _clamp_savgol_polyorder(self):
        """
        Keep polyorder < window_length. Your Baseline.savgol will clamp anyway,
        but this keeps the UI honest.
        """
        win = int(self.savitzkyWinLenSpinBox.value())
        current = int(self.savitzkyPolyorderSlider.value())
        max_allowed = max(1, win - 1)

        if current >= win:
            # snap down to win-1
            self.savitzkyPolyorderSlider.setValue(max_allowed)

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

    # ---------- Update plot ----------
    def update_plot_and_baseline(self):
        if self.df is None:
            QMessageBox.warning(self, "No data loaded", "Please load a file before updating the plot.")
            return

        col_x = self.df.columns[0]
        col_y = self.df.columns[1]
        x = self.df[col_x].values
        y = self.df[col_y].values

        method_text = self.baselineBox.currentText() or "None"
        method_norm = (method_text or "").strip().lower()
        method_norm = method_norm.replace("–", "-").replace("—", "-")

        x_label = self.xAxisLine.text().strip() or str(col_x)
        y_label = self.yAxisLine.text().strip() or str(col_y)
        title = self.titleLine.text().strip() or f"{col_x} vs {col_y}"

        try:
            if method_norm in ("none", ""):
                baseline = None
                x_vals = x
                y_corr = y

            elif method_norm == "airpls":
                lam = float(self.airLambdaSpinBox.value())
                porder = int(self.airPorderSlider.value())
                itermax = int(self.airItermaxSpinBox.value())

                x_vals, y_corr, baseline = Baseline.apply(
                    x, y, method=method_text, lam=lam, porder=porder, itermax=itermax
                )

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

                # Final guard (should already be handled by UI hooks)
                if window_length % 2 == 0:
                    window_length += 1
                if polyorder >= window_length:
                    polyorder = window_length - 1

                x_vals, y_corr, baseline = Baseline.apply(
                    x, y, method=method_text, window_length=window_length, polyorder=polyorder
                )

            else:
                raise ValueError(f"Unknown baseline selection: {method_text}")

        except Exception as e:
            QMessageBox.critical(self, "Baseline error", f"Failed to apply baseline method '{method_text}':\n{e}")
            baseline = None
            x_vals = x
            y_corr = y

        self.ax.clear()
        self.ax.plot(x_vals, y_corr, label="Signal")

        if baseline is not None:
            self.ax.plot(x_vals, baseline, linestyle="--", alpha=0.6, label="Baseline")
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
