import logging

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
from client import Client

logger = logging.getLogger()

class MarketViewModel(QObject):
    stockCodeListChanged = pyqtSignal()

    def __init__(self, qmlContext, parent=None):
        logger.debug("")
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('marketViewModel', self)

        self._stock_code_list = []

    @pyqtProperty(list, notify=stockCodeListChanged)
    def stock_code_list(self):
        return self._stock_code_list

    @stock_code_list.setter
    def stock_code_list(self, val: list):
        self._stock_code_list = val
        self.stockCodeListChanged.emit()

    @pyqtSlot()
    def load(self):
        logger.debug("")
        Client.getInstance().stock_code_list(self.on_stock_code_list_result)

    @pyqtSlot(list)
    def on_stock_code_list_result(self, result):
        logger.debug(f"result:{result}")
        self.stock_code_list = result
