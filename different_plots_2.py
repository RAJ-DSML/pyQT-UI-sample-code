'''
Author Name: Raj Kumar Pal
Date Created: 06-09-2023
'''

import sys
import json
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QVBoxLayout, QWidget, QFileDialog, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from scipy.stats import gaussian_kde

class DashboardWithOptions(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visualization Options")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        self.canvas = MplCanvas(self.central_widget, width=5, height=4)
        layout.addWidget(self.canvas)

        self.visualization_selector = QComboBox(self.central_widget)
        self.visualization_selector.addItem("Pie Chart")
        self.visualization_selector.addItem("Bar Chart")
        self.visualization_selector.addItem("Scatter Plot")
        self.visualization_selector.addItem("Kernel Density Plot")
        layout.addWidget(self.visualization_selector)

        self.visualization_selector.currentIndexChanged.connect(self.update_chart)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_file_action = QAction("Open JSON File", self)
        open_file_action.triggered.connect(self.load_json_data)
        file_menu.addAction(open_file_action)

        self.current_data = None

    def load_json_data(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)", options=options)

        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.current_data = data
                self.update_chart()

    def update_chart(self):
        if self.current_data is None:
            return

        self.canvas.clear()
        visualization_option = self.visualization_selector.currentText()

        if visualization_option == "Pie Chart":
            self.create_pie_chart(self.current_data)
        elif visualization_option == "Bar Chart":
            self.create_bar_chart(self.current_data)
        elif visualization_option == "Scatter Plot":
            self.create_scatter_plot(self.current_data)
        elif visualization_option == "Kernel Density Plot":
            self.create_kernel_density_plot(self.current_data)

        self.canvas.draw()

    def create_pie_chart(self, data):
        ax = self.canvas.fig.add_subplot(111)
        labels = list(data.keys())
        sizes = list(data.values())
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title("Pie Chart")

    def create_bar_chart(self, data):
        ax = self.canvas.fig.add_subplot(111)
        labels = list(data.keys())
        sizes = list(data.values())
        x_data = range(len(labels))
        ax.bar(x_data, sizes, tick_label=labels)
        ax.set_xlabel("Category")
        ax.set_ylabel("Value")
        ax.set_title("Bar Chart")

    def create_scatter_plot(self, data):
        ax = self.canvas.fig.add_subplot(111)
        x_data = list(data.keys())
        y_data = list(data.values())
        ax.scatter(x_data, y_data)
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_title("Scatter Plot")

    def create_kernel_density_plot(self, data):
        ax = self.canvas.fig.add_subplot(111)
        values = list(data.values())
        kernel = gaussian_kde(values)
        x_data = np.linspace(min(values), max(values), 100)
        y_data = kernel(x_data)
        ax.plot(x_data, y_data)
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.set_title("Kernel Density Plot")


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

    def clear(self):
        self.fig.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DashboardWithOptions()
    window.show()
    sys.exit(app.exec_())
