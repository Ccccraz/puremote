from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton
from PySide6.QtCore import Slot

from puremote.ui.trial_data_view import TrialDataView
from puremote.ui.dialog import DataMontiorDialog


class TrialDataMonitor(QWidget):
    def __init__(self) -> None:
        """Trial data monitor widget"""
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        self.layout_data = QHBoxLayout()
        group = QGroupBox("Trial data Monitor")
        group.setLayout(self.layout_data)
        self.layout_main.addWidget(group)

        button = QPushButton("Add monitor")
        self.layout_data.addWidget(button)

        button.clicked.connect(self.show_status)

    @Slot(str, str)
    def add_data(self, address, option) -> None:
        table = TrialDataView()
        table.init_listener(address, option)
        layout = QVBoxLayout()
        layout.addWidget(table)

        group = QGroupBox(address)
        group.setLayout(layout)

        self.layout_data.insertWidget(self.layout_data.count() - 1, group)

    def show_status(self) -> None:
        dialog = DataMontiorDialog(self)
        dialog.emit_accept.connect(self.add_data)
        dialog.exec()
