from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
)

from puremote.config.config import get_config
from qfluentwidgets import (
    EditableComboBox,
    BodyLabel,
    ComboBox,
    Dialog,
)


class AddTrialDataDialog(Dialog):
    emit_accept = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(self.tr("Add trial data"), "", parent)
        self.__init_ui()

    def __init_ui(self):
        self.setTitleBarVisible(False)
        self.setFixedSize(640, 320)

        self.layout_sub = QFormLayout()
        self.textLayout.addLayout(self.layout_sub)

        # Create input component
        self._init_status_server()

        self.yesButton.clicked.connect(self._emit_accept)
        self.yesButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def _init_status_server(self) -> None:
        """
        Create input component
        """

        config = get_config()

        label_address = BodyLabel(self.tr("Server : "))
        self.combobox_address = EditableComboBox()
        self.combobox_address.setPlaceholderText(self.tr("Input server address"))

        item_list: list = [i.values() for i in config.trial_data_source]
        self.combobox_address.addItems(item_list)

        # Add input component to layout
        self.layout_sub.addRow(label_address, self.combobox_address)

        label_option = BodyLabel(self.tr("Server type: "))
        self.combobox_option = ComboBox()
        item_list: list = [i for i in config.trial_data_mode]
        self.combobox_option.addItems(item_list)
        self.layout_sub.addRow(label_option, self.combobox_option)

    def _emit_accept(self) -> None:
        result = self.combobox_address.currentText()
        option = self.combobox_option.currentText()
        self.emit_accept.emit(result, option)
