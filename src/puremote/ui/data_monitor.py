from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton
from PySide6.QtCore import Slot

from puremote.ui.data_table_view import DataTableView
from puremote.ui.dialog import StatusDialog


class TrialDataMonitor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        group = QGroupBox("Trial data Monitor")
        group.setMaximumHeight(240)
        group.setMinimumWidth(640)
        button = QPushButton("Add monitor")
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(group)
        self.layout_data = QHBoxLayout()
        group.setLayout(self.layout_data)
        self.layout_data.addWidget(button)
        self.setLayout(self.layout_main)

        button.clicked.connect(self.show_status)

    @Slot(str, str)
    def add_data(self, address, option) -> None:
        table = DataTableView()
        table.init_listener(address, option)
        layout = QVBoxLayout()
        layout.addWidget(table)

        group = QGroupBox(address)
        group.setLayout(layout)

        self.layout_main.insertWidget(self.layout_data.count() - 1, group)

    def show_status(self) -> None:
        dialog = StatusDialog(self)
        dialog.emit_accept.connect(self.add_data)
        dialog.show()
