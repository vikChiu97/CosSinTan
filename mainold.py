import sys
import pandas as pd

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel Column Plotter")
        self.df = None

        # Button to open file
        self.open_button = QPushButton("Open Excel / CSV")
        self.open_button.clicked.connect(self.open_file)

        # Label to show file path
        self.file_label = QLabel("No file loaded")

        # Matplotlib figure embedded in Qt
        self.figure = Figure(figsize=(5, 4))
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Plot will show here")

        self.canvas = FigureCanvas(self.figure)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel or CSV file",
            "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*.*)"
        )

        if not file_path:
            return

        # Read file into DataFrame
        try:
            if file_path.lower().endswith((".xlsx", ".xls")):
                self.df = pd.read_excel(file_path)
            elif file_path.lower().endswith(".csv"):
                self.df = pd.read_csv(file_path)
            else:
                QMessageBox.critical(self, "Unsupported file",
                                     "Please choose an Excel or CSV file.")
                return
        except Exception as e:
            QMessageBox.critical(self, "Error reading file", str(e))
            return

        # Basic sanity check
        if self.df.shape[1] < 2:
            QMessageBox.critical(
                self,
                "Not enough columns",
                "File needs at least 2 columns (first vs second).",
            )
            return

        self.file_label.setText(file_path)
        self.plot_first_two_columns()

    def plot_first_two_columns(self):
        col_x = self.df.columns[0]
        col_y = self.df.columns[1]

        x = self.df[col_x]
        y = self.df[col_y]

        self.ax.clear()
        self.ax.plot(x, y, marker="o")

        self.ax.set_xlabel(str(col_x))
        self.ax.set_ylabel(str(col_y))
        self.ax.set_title(f"{col_x} vs {col_y}")
        self.ax.grid(True)

        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
