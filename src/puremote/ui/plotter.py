import numpy as np

from PySide6.QtCore import Slot, QModelIndex
from PySide6.QtWidgets import QApplication, QWidget

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas  # type: ignore
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar  # type: ignore
from matplotlib.backends.qt_compat import QtWidgets  # type: ignore

from puremote.ui.trial_data_view import JsonTableModel


class Plotter(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)

    def initialize_plot(
        self, title: str, xlabel: str, ylabel: str, data: JsonTableModel
    ):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.data = data

        self.data.rowsInserted.connect(self.update_canvas)

        self.xvalue = [item[self.xlabel] for item in self.data._data]
        self.yvalue = [item[self.ylabel] for item in self.data._data]

        self.ax.set_title(self.title)
        (self.line,) = self.ax.plot(self.xvalue, self.yvalue)

    @Slot(QModelIndex, int, int)
    def update_canvas(self, parent: QModelIndex, first: int, last: int):
        xdata = self.line.get_xdata()
        ydata = self.line.get_ydata()
        xdata = np.append(xdata, data._data[first][self.xlabel])
        ydata = np.append(ydata, data._data[first][self.ylabel])

        self.line.set_data(xdata, ydata)

        self.ax.relim()
        self.ax.autoscale_view()

        self.line.figure.canvas.draw()  # type: ignore


if __name__ == "__main__":
    import sys
    import random
    from tqdm.rich import tqdm

    item_1 = {"x": 1, "y": 2}
    data = JsonTableModel(item_1)

    for _ in tqdm(range(1000)):
        data.insert_new_data({"x": random.random(), "y": random.random()})

    app = QApplication(sys.argv)

    widget = Plotter()
    widget.initialize_plot("title", "x", "y", data)
    widget.show()

    sys.exit(app.exec())
