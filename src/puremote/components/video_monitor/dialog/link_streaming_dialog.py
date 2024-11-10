from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
)

from puremote.config.config import get_config

from qfluentwidgets import (
    MessageBoxBase,
    SubtitleLabel,
    EditableComboBox,
    BodyLabel,
    ComboBox,
)


class LinkStreamingDialog(MessageBoxBase):
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

        label_backend = BodyLabel(self.tr("Backend : "))
        self.combobox_backend = ComboBox()

        backend_list: list = [i for i in config.video_monitor_backend]
        self.combobox_backend.addItems(backend_list)

        self.layout_input.addRow(label_backend, self.combobox_backend)

    def _emit_accept(self) -> None:
        address = self.combobox_address.currentText()
        backend = self.combobox_backend.currentText()
        self.emit_accepted.emit(address, backend)
