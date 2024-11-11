from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QFormLayout, QFileDialog, QHBoxLayout

from puremote.config.config import get_config

from qfluentwidgets import (
    MessageBoxBase,
    SubtitleLabel,
    EditableComboBox,
    BodyLabel,
    ComboBox,
    SwitchButton,
    PushButton,
)


class LinkStreamingDialog(MessageBoxBase):
    emit_accepted = Signal(str, bool, str)  # Return rtsp server url and backend type

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

        self.titleLabel = SubtitleLabel(self.tr("Link Streaming"))
        self.viewLayout.addWidget(self.titleLabel)

        self.layout_input = QFormLayout()

        self.viewLayout.addLayout(self.layout_input)
        # Create input component
        self._init_rtsp_server()

        self.yesButton.clicked.connect(self._emit_accept)
        self.yesButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def _init_rtsp_server(self) -> None:
        """
        Create input component
        """

        config = get_config()

        label_address = BodyLabel("Server : ")
        self.combobox_address = EditableComboBox()
        self.combobox_address.setPlaceholderText(self.tr("Enter server address"))

        item_list: list = [i for i in config.video_source.values()]
        self.combobox_address.addItems(item_list)

        # Add input component to layout
        self.layout_input.addRow(label_address, self.combobox_address)

        label_record = BodyLabel(self.tr("Need record : "))
        self.switch_record = SwitchButton()
        self.switch_record.checkedChanged.connect(self.get_target_folder)

        self.layout_input.addRow(label_record, self.switch_record)

        self.folder_layout = QHBoxLayout()
        self.folder = EditableComboBox()
        self.folder.setPlaceholderText(self.tr("Folder for store video streaming"))
        self.get_folder_button = PushButton(self.tr("Browse"))
        self.get_folder_button.clicked.connect(self._get_floders)

    def _emit_accept(self) -> None:
        address = self.combobox_address.currentText()
        need_record = self.switch_record.isChecked()
        folder = self.folder.currentText()
        self.emit_accepted.emit(address, need_record, folder)

    def get_target_folder(self):
        self.folder_layout.addWidget(self.folder, 70)
        self.folder_layout.addWidget(self.get_folder_button, 30)
        self.viewLayout.addLayout(self.folder_layout)

    def _get_floders(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr("Select Folder"))
        self.folder.addItem(folder)
