import sys
from threading import Thread

from puremote.shared.http_listener import HttpListener, HttpListenerSse

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Signal,
)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QTableView,
    QTableWidget,
    QVBoxLayout,
    QApplication,
)


class JsonTableModel(QAbstractTableModel):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self._data = [data] or []

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self._data) if self._data else 0

    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self._data[index.row()]
            keys = list(row.keys())
            return row[keys[index.column()]]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter

        if role == Qt.ItemDataRole.FontRole:
            return QFont(["Arial"], pointSize=10)

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return list(self._data[0].keys())[section]

        if role == Qt.ItemDataRole.FontRole:
            font = QFont(["Arial"], pointSize=13)
            font.setBold(True)
            return font
        return None

    def insert_new_data(self, row_data: dict):
        position = len(self._data)
        self.beginInsertRows(QModelIndex(), position, position)
        self._data.append(row_data)
        self.endInsertRows()


class TrialDataView(QWidget):
    received = Signal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.table = QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(10)
        self.layout_main.addWidget(self.table)

    def init_listener(self, address: str, option: str) -> None:
        if option == "sse":
            self.listener = HttpListenerSse(address)
        elif option == "polling":
            self.listener = HttpListener(address)

        self._listener_thread = Thread(target=self._update_data)
        self._listener_thread.start()
        self._is_init = False
        self.received.connect(self._update_view)

    def _update_data(self):
        for data in self.listener.listen():
            self.received.emit(data)

    def _update_view(self, data: dict) -> None:
        if self._is_init is not True:
            self.layout_main.removeWidget(self.table)
            self.table.deleteLater()

            self.data_model = JsonTableModel(data)
            self.table = QTableView()
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
    window = TrialDataView()
    window.init_listener("http://localhost:8000/sse", "sse")

    window.show()
    sys.exit(app.exec())
