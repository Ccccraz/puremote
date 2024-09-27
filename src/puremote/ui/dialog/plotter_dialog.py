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

from puremote import CONFIG


class FigurePlotterDialog(QDialog):
    """Dialog to select a figure to plot"""

    emit_accepted = Signal(str, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
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
        with open(CONFIG, "rb") as f:
            config = tomllib.load(f)

        label_name = QLabel("figure name")
        self.combo_box_name = QComboBox()

        self.combo_box_name.setEditable(True)
        self.layout_input.addRow(label_name, self.combo_box_name)

        label_data = QLabel("data")
        self.combo_box_data = QComboBox()
        self.combo_box_data.setEditable(True)
        self.layout_input.addRow(label_data, self.combo_box_data)

        labels_xaxis = QLabel("x axis")
        self.combo_box_xaxis = QComboBox()
        self.combo_box_xaxis.setEditable(True)
        self.layout_input.addRow(labels_xaxis, self.combo_box_xaxis)

        label_yaxis = QLabel("y axis")
        self.combo_box_yaxis = QComboBox()
        self.combo_box_yaxis.setEditable(True)
        self.layout_input.addRow(label_yaxis, self.combo_box_yaxis)

        for i in config["plot"]["figures"]:
            self.combo_box_name.addItem(i["name"])
            self.combo_box_data.addItem(i["data"])
            self.combo_box_xaxis.addItem(i["xaxis"])
            self.combo_box_yaxis.addItem(i["yaxis"])

    def _emit_accepted(self):
        """Emit accepted signal with selected data"""
        self.emit_accepted.emit(
            self.combo_box_name.currentText(),
            self.combo_box_data.currentText(),
            self.combo_box_xaxis.currentText(),
            self.combo_box_yaxis.currentText(),
        )


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog = FigurePlotterDialog()
    dialog.show()

    sys.exit(app.exec())
