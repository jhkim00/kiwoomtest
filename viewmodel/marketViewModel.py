import logging

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
from PyQt5.QtQml import QJSValue
from client import Client
from .stockComboBoxModel import StockComboBoxModel

logger = logging.getLogger()

class MarketViewModel(QObject):
    stockComboBoxModelChanged = pyqtSignal()
    stockListChanged = pyqtSignal()
    currentStockChanged = pyqtSignal()

    def __init__(self, qmlContext, parent=None):
        logger.debug("")
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('marketViewModel', self)

        self._stockComboBoxModel = StockComboBoxModel()
        self._stockList = []
        self._currentStock = None

    @pyqtProperty(StockComboBoxModel, notify=stockComboBoxModelChanged)
    def stockComboBoxModel(self):
        return self._stockComboBoxModel

    @stockComboBoxModel.setter
    def stockComboBoxModel(self, val: StockComboBoxModel):
        self._stockComboBoxModel = val
        self.stockComboBoxModelChanged.emit()

    @pyqtProperty(list, notify=stockListChanged)
    def stockList(self):
        return self._stockList

    @stockList.setter
    def stockList(self, val: list):
        self._stockList = val
        self.stockListChanged.emit()

    @pyqtProperty(dict, notify=currentStockChanged)
    def currentStock(self):
        return self._currentStock

    @currentStock.setter
    def currentStock(self, val: dict):
        if self._currentStock != val:
            logger.debug(f"stock:{val}")
            self._currentStock = val
            self.currentStockChanged.emit()

    @pyqtSlot()
    def load(self):
        logger.debug("")
        Client.getInstance().stock_list(self.on_stock_list_result)

    @pyqtSlot(QVariant)
    def setCurrentStock(self, val):
        if isinstance(val, dict):
            self.currentStock = val
        elif isinstance(val, QJSValue):
            self.currentStock = val.toVariant()

    @pyqtSlot(list)
    def on_stock_list_result(self, result):
        logger.debug("")
        self.stockComboBoxModel = StockComboBoxModel(result)
        self.stockList = result
        if len(result) > 0:
            self.currentStock = self.stockList[0]

