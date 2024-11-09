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


class LinkStreamingDialog(QDialog):
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

        config = get_config()

        label_address = QLabel("Server : ")
        self.combobox_address = QComboBox()
        self.combobox_address.setEditable(True)

        item_list: list = [i for i in config.video_source.values()]
        self.combobox_address.addItems(item_list)

        # Add input component to layout
        self.layout_input.addRow(label_address, self.combobox_address)

        label_backend = QLabel("Backend : ")
        self.combobox_backend = QComboBox()

        backend_list: list = [i for i in config.video_monitor_backend]
        self.combobox_backend.addItems(backend_list)

        self.layout_input.addRow(label_backend, self.combobox_backend)

    def _emit_accept(self) -> None:
        address = self.combobox_address.currentText()
        backend = self.combobox_backend.currentText()
        self.emit_accepted.emit(address, backend)
