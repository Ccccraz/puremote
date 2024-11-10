import sys
from queue import Queue
from threading import Thread

from puremote.shared.web_requests.http_listener import HttpListener, HttpListenerSse
from puremote.models.trail_data import TrialDataModel, TrialData
from puremote.components.card.base_card import BaseCard

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication

from qfluentwidgets import TableWidget, TableView


class TrialDataView(QWidget):
    received = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.table = TableWidget()
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)

        self.table.setRowCount(10)
        self.table.setColumnCount(10)
        self.layout_main.addWidget(self.table)

    def init_listener(self, address: str, option: str) -> None:
        self.address = address
        if option == "sse":
            self.listener = HttpListenerSse(address)
        elif option == "polling":
            self.listener = HttpListener(address)

        self.data_queue: Queue = Queue()

        self._listener_thread = Thread(target=self._update_data)
        self._listener_thread.start()
        self._is_init = False
        self.received.connect(self._update_view)

    def _update_data(self):
        for data in self.listener.listen():
            self.data_queue.put(data)
            self.received.emit()

    def _update_view(self) -> None:
        data = self.data_queue.get()
        if self._is_init is not True:
            self.layout_main.removeWidget(self.table)
            self.table.deleteLater()

            self.data_model = TrialDataModel(data)
            trial_data = TrialData()
            trial_data.add_data(self.address, self.data_model)
            self.table = TableView()
            self.table.setModel(self.data_model)
            self.layout_main.addWidget(self.table)
            self._is_init = True
        else:
            self.data_model.insert_new_data(data)
            self.table.resizeColumnsToContents()
            self.table.scrollToBottom()

    def stop(self) -> None:
        if self.listener is not None:
            self.listener.stop()
            self.is_running = False
            self._listener_thread.join()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = TrialDataView()
    # window = BaseCard("hello", data, 0)
    # window.init_listener("test", "sse")

    # window.show()
    sys.exit(app.exec())
