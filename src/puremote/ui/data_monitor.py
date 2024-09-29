from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton
from PySide6.QtCore import Slot, Signal

from puremote.ui.trial_data_view import TrialDataView
from puremote.ui.dialog.dialog_legacy import DataMontiorDialog


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
    def add_data(self, address: str, option: str) -> None:
        table = TrialDataViewWidget(address)
        table.table.init_listener(address, option)

        self.layout_data.insertWidget(self.layout_data.count() - 1, table)

    def show_status(self) -> None:
        dialog = DataMontiorDialog(self)
        dialog.emit_accept.connect(self.add_data)
        dialog.exec()


class TrialDataViewWidget(QWidget):
    def __init__(self, address: str) -> None:
        super().__init__()
        self.address = address
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout_group = QVBoxLayout()
        layout_data = QHBoxLayout()
        layout_btn = QHBoxLayout()

        group = QGroupBox(self.address)

        layout.addWidget(group)
        group.setLayout(layout_group)
        layout_group.addLayout(layout_data)
        layout_group.addLayout(layout_btn)

        self._table = TrialDataView()
        layout_data.addWidget(self._table)

        refresh_btn = QPushButton("Refresh")
        layout_btn.addWidget(refresh_btn)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self._close)
        layout_btn.addWidget(close_btn)

    @property
    def table(self):
        return self._table

    def _close(self) -> None:
        self.close()

    # TODO: implement this
    def _refresh(self) -> None:
        pass


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = TrialDataViewWidget("test")
    widget.show()
    sys.exit(app.exec())
