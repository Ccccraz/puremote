from typing import Dict
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QDialogButtonBox,
    QComboBox,
    QWidget,
)


class RtspDialog(QDialog):
    emit_accepted = Signal(str, str)

    def __init__(self, parent, config: Dict) -> None:
        super().__init__(parent)
        self._config: Dict = config
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("Rtsp")

        # Main layout of dialog
        self.layout_main = QVBoxLayout()
        # Layout of dialog component
        self.layout_address = QHBoxLayout()
        self.layout_backend = QHBoxLayout()

        self.layout_main.addLayout(self.layout_address)
        self.layout_main.addLayout(self.layout_backend)
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
        label_address = QLabel("Server : ")
        self.combobox_address = QComboBox()
        self.combobox_address.setEditable(True)

        item_list: list = [i for i in self._config["rtsp_server"]]
        self.combobox_address.addItems(item_list)

        # Add input component to layout
        self.layout_address.addWidget(label_address)
        self.layout_address.addWidget(self.combobox_address)

        label_backend = QLabel("Backend : ")
        self.combobox_backend = QComboBox()

        backend_list: list = ["opengl", "vlc"]
        self.combobox_backend.addItems(backend_list)

        self.layout_backend.addWidget(label_backend)
        self.layout_backend.addWidget(self.combobox_backend)

    def _emit_accept(self) -> None:
        address = self.combobox_address.currentText()
        backend = self.combobox_backend.currentText()
        self.emit_accepted.emit(address, backend)


class StatusDialog(QDialog):
    emit_accept = Signal(str)

    def __init__(self, parent: QWidget, config: Dict) -> None:
        super().__init__(parent)
        self._config: Dict = config
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("Set status server")

        # Main layout of dialog
        self.layout_main = QVBoxLayout()
        # Layout of dialog component
        self.layout_sub = QHBoxLayout()

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
        label_address = QLabel("Server : ")
        self.combobox_address = QComboBox()
        self.combobox_address.setEditable(True)

        item_list: list = [i for i in self._config["data_monitor"]]
        self.combobox_address.addItems(item_list)

        # Add input component to layout
        self.layout_sub.addWidget(label_address)
        self.layout_sub.addWidget(self.combobox_address)

    def _emit_accept(self) -> None:
        result = self.combobox_address.currentText()
        self.emit_accept.emit(result)


# if __name__ == "__main__":
#     import json
#     import sys

#     with open(r"../config/default.json", "r") as file:
#         config: Dict = json.load(file)

#     from PySide6.QtWidgets import QApplication

#     app = QApplication(sys.argv)

#     widget = RtspDialog(app, config)
#     widget.show()

#     sys.exit(app.exec())
