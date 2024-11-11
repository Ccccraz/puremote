from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QFileDialog,
    QHBoxLayout,
)

from puremote.config.config import get_config

from qfluentwidgets import (
    EditableComboBox,
    PushButton,
    Dialog,
)


class RecordStreamingDialog(Dialog):
    emit_accepted = Signal(str)  # Return rtsp server url and backend type

    def __init__(self, parent: QWidget | None = None) -> None:
        """Dialog for set record streaming

        Args:
            parent (QWidget): parent widget
        """
        super().__init__("Record Streaming", "Using for record streaming", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize ui"""
        self.setTitleBarVisible(False)
        self.setFixedSize(640, 320)

        self.layout_input = QHBoxLayout()
        self.textLayout.addLayout(self.layout_input)

        # Create input component
        self._init_recorder()

        self.yesButton.clicked.connect(self._emit_accept)
        self.yesButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def _init_recorder(self) -> None:
        """
        Create input component
        """

        config = get_config()

        self.combobox_address = EditableComboBox()
        self.combobox_address.setPlaceholderText(
            self.tr("Folder for store video streaming")
        )

        item_list: list = [i for i in config.video_source.values()]
        self.combobox_address.addItems(item_list)
        self.button_browse = PushButton(self.tr("Browse"))
        self.button_browse.clicked.connect(self._get_floder)

        # Add input component to layout
        self.layout_input.addWidget(self.combobox_address, 70)
        self.layout_input.addWidget(self.button_browse, 30)

    def _get_floder(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr("Select Folder"))
        self.combobox_address.addItem(folder)

    def _emit_accept(self) -> None:
        self.emit_accepted.emit(self.combobox_address.currentText())
