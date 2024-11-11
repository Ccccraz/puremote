from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QLabel,
    QFormLayout,
)

from puremote.config.config import get_config
from puremote.models.trail_data import TrialData
from qfluentwidgets import (
    EditableComboBox,
    BodyLabel,
    ComboBox,
    Dialog,
)


class RefreshComboBox(ComboBox):
    clicked = Signal()

    def __init__(self, *args, **kwargs):
        super(RefreshComboBox, self).__init__(*args, **kwargs)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.clicked.emit()
        return super(RefreshComboBox, self).mousePressEvent(e)


class AddFigureDialog(Dialog):
    """Dialog to select a figure to plot"""

    emit_accepted = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(self.tr("Add figure"), "", parent)
        self.data = TrialData()
        self._init_ui()

    def _init_ui(self):
        self.setTitleBarVisible(False)
        self.setFixedSize(640, 320)

        self.layout_input = QFormLayout()

        self.textLayout.addLayout(self.layout_input)

        self._init_plotter()

        self.yesButton.clicked.connect(self._emit_accepted)
        self.yesButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def _init_plotter(self):
        self.config = get_config()

        # Add Plot data source
        label_data = BodyLabel(self.tr("data"))
        self.combo_box_data = RefreshComboBox()
        self.combo_box_data.clicked.connect(self.index_data)
        self.combo_box_data.currentTextChanged.connect(self.index_axis)
        self.layout_input.addRow(label_data, self.combo_box_data)

        # Add x axis data
        labels_xaxis = BodyLabel(self.tr("x axis"))
        self.combo_box_xaxis = EditableComboBox()
        self.layout_input.addRow(labels_xaxis, self.combo_box_xaxis)

        # Add y axis data
        label_yaxis = QLabel("y axis")
        label_yaxis = BodyLabel(self.tr("y axis"))
        self.combo_box_yaxis = EditableComboBox()
        self.layout_input.addRow(label_yaxis, self.combo_box_yaxis)

        # Add figure type
        label_type = BodyLabel(self.tr("type"))
        self.combo_box_type = EditableComboBox()
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
