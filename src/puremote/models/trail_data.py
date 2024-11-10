from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
)
from puremote.shared.base.singleton_base import SingletonMeta


class TrialDataModel(QAbstractTableModel):
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

        return None

    def insert_new_data(self, row_data: dict):
        position = len(self._data)
        self.beginInsertRows(QModelIndex(), position, position)
        self._data.append(row_data)
        self.endInsertRows()


class TrialData(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._store: dict[str, TrialDataModel] = {}

    def add_data(self, address: str, data: TrialDataModel) -> None:
        self._store[address] = data

    @property
    def data(self):
        return self._store
