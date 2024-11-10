from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QPushButton

from puremote.components.plotter.dialog.add_figure_dialog import AddFigureDialog
from puremote.components.plotter.backend.plotter import Plotter
from puremote.components.card.base_card import BaseCard

from qfluentwidgets import PrimaryPushButton


class PlotterCard(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._init_ui()
        self.parent_main = parent

    def _init_ui(self):
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)

        self.card = BaseCard(self.tr("Figures"))
        self.layout_main.addWidget(self.card)

        self.layout_figures = QVBoxLayout()

        button = PrimaryPushButton(self.tr("add figure"))
        button.clicked.connect(self.show_dialog)

        self.card.addFunctionButton([button])

    def show_dialog(self):
        dialog = AddFigureDialog(self.parent_main)
        dialog.emit_accepted.connect(self.add_figure)
        dialog.exec()

    @Slot(str, str, str)
    def add_figure(self, data: str, xaxis: str, yaxis: str):
        plotter = Plotter()
        plotter.initialize_plot(xaxis, yaxis, data)
        self.layout_figures.addWidget(plotter)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = PlotterCard()
    widget.show()
    sys.exit(app.exec())
