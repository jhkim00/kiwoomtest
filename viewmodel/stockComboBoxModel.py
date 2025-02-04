import logging

from PyQt5.QtCore import QAbstractListModel, Qt, QVariant

logger = logging.getLogger()

class StockComboBoxModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    CodeRole = Qt.UserRole + 2

    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        # logger.debug(f"data:{data}")

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data):
            return QVariant()

        item = self._data[index.row()]
        if role == Qt.DisplayRole:
            return item['name'] + ' ' + item['code']
        if role == self.NameRole:
            return item["name"]
        elif role == self.CodeRole:
            return item["code"]

        return QVariant()

    def roleNames(self):
        return {
            Qt.DisplayRole: b"display",
            self.NameRole: b"name",
            self.CodeRole: b"code"
        }
