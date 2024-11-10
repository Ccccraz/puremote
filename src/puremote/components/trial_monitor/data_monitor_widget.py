from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Slot

from puremote.components.trial_monitor.data_view.trial_data_view import TrialDataView
from puremote.components.trial_monitor.dialog.add_trial_data_dialog import (
    AddTrialDataDialog,
)
from puremote.components.card.base_card import BaseCard
from qfluentwidgets import PrimaryPushButton, FluentIcon


class TrialDataCard(QWidget):
    def __init__(self) -> None:
        """Trial data monitor widget"""
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        self.card = BaseCard("Trial data monitor")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.card)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        button = PrimaryPushButton(FluentIcon.ADD, self.tr("Add data"), self)
        button.clicked.connect(self.show_status)

        self.card.addFunctionButton([button])

    @Slot(str, str)
    def add_data(self, address: str, option: str) -> None:
        table = TrialDataView()
        table.init_listener(address, option)

        self.card.viewLayout.addWidget(table)

    def show_status(self) -> None:
        dialog = AddTrialDataDialog(self)
        dialog.emit_accept.connect(self.add_data)
        dialog.exec()
