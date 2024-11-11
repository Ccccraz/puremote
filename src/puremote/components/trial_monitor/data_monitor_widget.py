from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Slot

from puremote.components.trial_monitor.data_view.trial_data_view import TrialDataView
from puremote.components.trial_monitor.dialog.add_trial_data_dialog import (
    AddTrialDataDialog,
)
from puremote.components.card.base_card import BaseCard
from qfluentwidgets import PrimaryPushButton, FluentIcon


class TrialDataCard(QWidget):
    def __init__(self, parent) -> None:
        """Trial data monitor widget"""
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        self.card = BaseCard("Trial data monitor", self)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.card)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        button = PrimaryPushButton(FluentIcon.ADD, self.tr("Add data"), self)
        button.clicked.connect(self.show_status)

        button_close = PrimaryPushButton(FluentIcon.CLOSE, self.tr("Close"), self)
        button_close.clicked.connect(self.stop)

        self.card.addFunctionButtons([button, button_close])

    @Slot(str, str)
    def add_data(self, address: str, option: str) -> None:
        self.table = TrialDataView()
        self.table.init_listener(address, option)

        self.card.viewLayout.addWidget(self.table)
        self.card.viewLayout.setContentsMargins(10, 10, 10, 10)
        self.card.viewLayout.setSpacing(0)

    def show_status(self) -> None:
        dialog = AddTrialDataDialog(self.window())
        dialog.emit_accept.connect(self.add_data)
        dialog.exec()

    def stop(self):
        try:
            self.table.stop()
            self.card.viewLayout.removeWidget(self.table)
            self.table.deleteLater()
        except AttributeError:
            pass

    def closeEvent(self, event: QCloseEvent) -> None:
        self.stop()
        return super().closeEvent(event)
