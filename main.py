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

from ui_main import Ui_MainWindow  # generated from main.ui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up all the widgets from Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.df = None

        # Short aliases to UI widgets
        self.openButton = self.ui.openButton
        self.fileLabel = self.ui.fileLabel
        self.plotWidget = self.ui.plotWidget

        # New line edits for labels and title
        self.xAxisLine = self.ui.xAxisLine
        self.yAxisLine = self.ui.yAxisLine
        self.titleLine = self.ui.titleLine
        self.updateButton = self.ui.updateButton

        # Wire up buttons
        self.openButton.clicked.connect(self.open_file)
        self.updateButton.clicked.connect(self.update_plot_labels)

        # Set up matplotlib figure inside plotWidget
        self.figure = Figure(figsize=(5, 4))
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Plot will show here")

        self.canvas = FigureCanvas(self.figure)

        # Add canvas into plotWidget's layout
        layout = self.plotWidget.layout()
        if layout is None:
            layout = QVBoxLayout(self.plotWidget)
            layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel or CSV file",
            "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*.*)"
        )

        if not file_path:
            return

        try:
            if file_path.lower().endswith((".xlsx", ".xls")):
                self.df = pd.read_excel(file_path)
            elif file_path.lower().endswith(".csv"):
                self.df = pd.read_csv(file_path)
            else:
                QMessageBox.critical(
                    self,
                    "Unsupported file",
                    "Please choose an Excel or CSV file.",
                )
                return
        except Exception as e:
            QMessageBox.critical(self, "Error reading file", str(e))
            return

        if self.df.shape[1] < 2:
            QMessageBox.critical(
                self,
                "Not enough columns",
                "File needs at least 2 columns (first vs second).",
            )
            return

        self.fileLabel.setText(file_path)
        self.plot_first_two_columns()

    def plot_first_two_columns(self):
        col_x = self.df.columns[0]
        col_y = self.df.columns[1]

        x = self.df[col_x]
        y = self.df[col_y]

        self.ax.clear()
        self.ax.plot(x, y, marker="o")

        default_x_label = str(col_x)
        default_y_label = str(col_y)
        default_title = f"{col_x} vs {col_y}"

        # Set labels and title on the plot
        self.ax.set_xlabel(default_x_label)
        self.ax.set_ylabel(default_y_label)
        self.ax.set_title(default_title)
        self.ax.grid(True)

        # Update line edits to match current labels/title
        self.xAxisLine.setText(default_x_label)
        self.yAxisLine.setText(default_y_label)
        self.titleLine.setText(default_title)

        self.canvas.draw()

    def update_plot_labels(self):
        if self.df is None:
            QMessageBox.warning(
                self,
                "No data loaded",
                "Please load a file before updating plot labels.",
            )
            return

        x_label = self.xAxisLine.text().strip()
        y_label = self.yAxisLine.text().strip()
        title = self.titleLine.text().strip()

        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)
        if title:
            self.ax.set_title(title)

        self.canvas.draw_idle()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
