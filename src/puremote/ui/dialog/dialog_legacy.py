import tomllib

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

from puremote import CONFIG


class VideoMontiorDialog(QDialog):
    emit_accepted = Signal(str, str)  # Return rtsp server url and backend type

    def __init__(self, parent: QWidget | None = None) -> None:
        """Dialog for set rtsp server url and backend type

        Args:
            parent (QWidget): parent widget
            config (dict): configuration
        """
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize ui"""
        self.setWindowTitle("Rtsp")

        # Main layout of dialog
        self.layout_main = QVBoxLayout()

        self.layout_input = QFormLayout()

        self.layout_main.addLayout(self.layout_input)
        self.setLayout(self.layout_main)

        # Create input component
        self._init_rtsp_server()

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

    def _init_rtsp_server(self) -> None:
        """
        Create input component
        """

        with open(CONFIG, "rb") as f:
            config = tomllib.load(f)

        label_address = QLabel("Server : ")
        self.combobox_address = QComboBox()
        self.combobox_address.setEditable(True)

        item_list: list = [i for i in config["rtsp_server"]["url"]]
        self.combobox_address.addItems(item_list)

        # Add input component to layout
        self.layout_input.addRow(label_address, self.combobox_address)

        label_backend = QLabel("Backend : ")
        self.combobox_backend = QComboBox()

        backend_list: list = [i for i in config["rtsp_server"]["backend"]]
        self.combobox_backend.addItems(backend_list)

        self.layout_input.addRow(label_backend, self.combobox_backend)

    def _emit_accept(self) -> None:
        address = self.combobox_address.currentText()
        backend = self.combobox_backend.currentText()
        self.emit_accepted.emit(address, backend)


class DataMontiorDialog(QDialog):
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
        with open(CONFIG, "rb") as f:
            config = tomllib.load(f)

        label_address = QLabel("Server : ")
        self.combobox_address = QComboBox()
        self.combobox_address.setEditable(True)

        item_list: list = [i for i in config["data_monitor"]["url"]]
        self.combobox_address.addItems(item_list)

        # Add input component to layout
        self.layout_sub.addRow(label_address, self.combobox_address)

        label_option = QLabel("Server type: ")
        self.combobox_option = QComboBox()
        item_list: list = [i for i in config["data_monitor"]["option"]]
        self.combobox_option.addItems(item_list)
        self.layout_sub.addRow(label_option, self.combobox_option)

    def _emit_accept(self) -> None:
        result = self.combobox_address.currentText()
        option = self.combobox_option.currentText()
        self.emit_accept.emit(result, option)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog_address = VideoMontiorDialog()
    dialog_address.exec()

    dialog_status = DataMontiorDialog()
    dialog_status.exec()

    sys.exit(app.exec())
