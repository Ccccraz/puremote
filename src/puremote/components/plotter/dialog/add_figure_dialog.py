from logging import config
import tomllib

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QDialogButtonBox,
    QComboBox,
    QFormLayout,
)

from puremote.config.config import get_config
from puremote.models.trail_data import TrialData


class ComboBox(QComboBox):
    popupAboutToBeShown = Signal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()


class AddFigureDialog(QDialog):
    """Dialog to select a figure to plot"""

    emit_accepted = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = TrialData()
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Select data to plot")
        self.layout_main = QVBoxLayout()

        self.layout_input = QFormLayout()

        self.layout_main.addLayout(self.layout_input)
        self.setLayout(self.layout_main)

        self._init_plotter()

        q_dialog_btn = (
            QDialogButtonBox.StandardButton.Open
            | QDialogButtonBox.StandardButton.Cancel
        )

        button_box = QDialogButtonBox(q_dialog_btn)

        button_box.accepted.connect(self._emit_accepted)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.layout_main.addWidget(button_box)

    def _init_plotter(self):
        self.config = get_config()

        # Add Plot data source
        label_data = QLabel("data")
        self.combo_box_data = ComboBox()
        self.combo_box_data.setEditable(True)
        self.combo_box_data.popupAboutToBeShown.connect(self.index_data)
        self.combo_box_data.currentTextChanged.connect(self.index_axis)
        self.layout_input.addRow(label_data, self.combo_box_data)

        # Add x axis data
        labels_xaxis = QLabel("x axis")
        self.combo_box_xaxis = ComboBox()
        self.combo_box_xaxis.setEditable(True)
        self.layout_input.addRow(labels_xaxis, self.combo_box_xaxis)

        # Add y axis data
        label_yaxis = QLabel("y axis")
        self.combo_box_yaxis = ComboBox()
        self.combo_box_yaxis.setEditable(True)
        self.layout_input.addRow(label_yaxis, self.combo_box_yaxis)

        # Add figure type
        label_type = QLabel("type")
        self.combo_box_type = ComboBox()
        self.layout_input.addRow(label_type, self.combo_box_type)

        # Add preset
        for i in self.config.figure:
            self.combo_box_data.addItem(i.nickname)

    def _emit_accepted(self):
        """Emit accepted signal with selected data"""
        self.emit_accepted.emit(
            self.combo_box_data.currentText(),
            self.combo_box_xaxis.currentText(),
            self.combo_box_yaxis.currentText(),
        )

    def index_data(self):
        self.combo_box_data.clear()

        # add preset
        for i in self.config.figure:
            self.combo_box_data.addItem(i.nickname)

        # add data address from trialdata
        for i in self.data.data:
            self.combo_box_data.addItem(i)

    def index_axis(self):
        self.combo_box_xaxis.clear()
        self.combo_box_yaxis.clear()

        for i in self.config.figure:
            if self.combo_box_data.currentText() == i.nickname:
                self.combo_box_xaxis.addItem(i.x_axis)
                self.combo_box_yaxis.addItem(i.y_axis)

        if self.data.data != {}:
            keys = self.data.data[self.combo_box_data.currentText()]._data[0].keys()

            for i in keys:
                self.combo_box_xaxis.addItem(i)
                self.combo_box_yaxis.addItem(i)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog = AddFigureDialog()
    dialog.show()

    sys.exit(app.exec())
