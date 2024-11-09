from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QDialogButtonBox,
    QComboBox,
    QWidget,
    QFormLayout,
)

from puremote.config.config import get_config


class AddTrialDataDialog(QDialog):
    emit_accept = Signal(str, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("Set status server")

        # Main layout of dialog
        self.layout_main = QVBoxLayout()
        self.layout_sub = QFormLayout()

        self.layout_main.addLayout(self.layout_sub)
        self.setLayout(self.layout_main)

        # Create input component
        self._init_status_server()

        # Create standard button box for diglog
        q_dialog_btn = (
            QDialogButtonBox.StandardButton.Open
            | QDialogButtonBox.StandardButton.Cancel
        )
        button_box = QDialogButtonBox(q_dialog_btn)

        button_box.accepted.connect(self._emit_accept)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Add standard button to layout
        self.layout_main.addWidget(button_box)

    def _init_status_server(self) -> None:
        """
        Create input component
        """

        config = get_config()

        label_address = QLabel("Server : ")
        self.combobox_address = QComboBox()
        self.combobox_address.setEditable(True)

        item_list: list = [i.values() for i in config.trial_data_source]
        self.combobox_address.addItems(item_list)

        # Add input component to layout
        self.layout_sub.addRow(label_address, self.combobox_address)

        label_option = QLabel("Server type: ")
        self.combobox_option = QComboBox()
        item_list: list = [i for i in config.trial_data_mode]
        self.combobox_option.addItems(item_list)
        self.layout_sub.addRow(label_option, self.combobox_option)

    def _emit_accept(self) -> None:
        result = self.combobox_address.currentText()
        option = self.combobox_option.currentText()
        self.emit_accept.emit(result, option)
