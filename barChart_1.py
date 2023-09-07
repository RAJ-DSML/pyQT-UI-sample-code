'''
Author Name: Raj Kumar Pal
Date Created: 06-09-2023
'''

import sys
import json
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QVBoxLayout, QWidget, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HeadcountDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Headcount Dashboard")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        self.canvas = MplCanvas(self.central_widget, width=5, height=4)
        layout.addWidget(self.canvas)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_file_action = QAction("Open JSON File", self)
        open_file_action.triggered.connect(self.load_json_data)
        file_menu.addAction(open_file_action)

    def load_json_data(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)", options=options)

        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.update_chart(data)

    def update_chart(self, data):
        months = list(data.keys())
        headcounts = list(data.values())

        self.canvas.plot(months, headcounts)


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

    def plot(self, x_data, y_data):
        self.ax.clear()
        self.ax.bar(x_data, y_data)
        self.ax.set_xlabel("Month")
        self.ax.set_ylabel("Headcount")
        self.ax.set_title("Monthly Headcount for the Year")

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HeadcountDashboard()
    window.show()
    sys.exit(app.exec_())