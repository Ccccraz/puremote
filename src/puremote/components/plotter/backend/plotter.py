import numpy as np

from PySide6.QtCore import Slot, QModelIndex
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas  # type: ignore
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar  # type: ignore

from puremote.models.trail_data import TrialData, TrialDataModel


class Plotter(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)

    def initialize_plot(self, xlabel: str, ylabel: str, data_address: str):
        # Create a plotter
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.data_address = data_address
        self.data = TrialData()
        self.data.data[self.data_address].rowsInserted.connect(self.update_canvas)

        self.xvalue = [
            item[self.xlabel] for item in self.data.data[self.data_address]._data
        ]
        self.yvalue = [
            item[self.ylabel] for item in self.data.data[self.data_address]._data
        ]

        (self.line,) = self.ax.plot(self.xvalue, self.yvalue)

    @Slot(QModelIndex, int, int)
    def update_canvas(self, parent: QModelIndex, first: int, last: int):
        # Update the plot if new data is added
        xdata = self.line.get_xdata()
        ydata = self.line.get_ydata()
        xdata = np.append(
            xdata, self.data.data[self.data_address]._data[first][self.xlabel]
        )
        ydata = np.append(
            ydata, self.data.data[self.data_address]._data[first][self.ylabel]
        )

        self.line.set_data(xdata, ydata)

        self.ax.relim()
        self.ax.autoscale_view()

        self.line.figure.canvas.draw()  # type: ignore


if __name__ == "__main__":
    import sys
    import random
    from tqdm.rich import tqdm

    item_1 = {"x": 1, "y": 2}
    data = TrialDataModel(item_1)

    for _ in tqdm(range(1000)):
        data.insert_new_data({"x": random.random(), "y": random.random()})

        data_store = TrialData()
        data_store.add_data("test", data)

    app = QApplication(sys.argv)

    widget = Plotter()
    widget.initialize_plot("x", "y", "test")
    widget.show()

    sys.exit(app.exec())
