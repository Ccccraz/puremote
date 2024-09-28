from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QPushButton

from puremote.ui.dialog.plotter_dialog import FigurePlotterDialog
from puremote.ui.plotter import Plotter


class PlotterWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.layout_figures = QVBoxLayout()
        group = QGroupBox("figure")
        group.setLayout(self.layout_figures)
        self.layout_main.addWidget(group)

        button = QPushButton("add figure")
        button.clicked.connect(self.show_dialog)
        self.layout_figures.addWidget(button)

    def show_dialog(self):
        dialog = FigurePlotterDialog(self)
        dialog.emit_accepted.connect(self.add_figure)
        dialog.exec()

    @Slot(str, str, str)
    def add_figure(self, data: str, xaxis: str, yaxis: str):
        plotter = Plotter()
        plotter.initialize_plot(xaxis, yaxis, data)
        self.layout_figures.insertWidget(self.layout_figures.count() - 1, plotter)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = PlotterWidget()
    widget.show()
    sys.exit(app.exec())
