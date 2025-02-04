import logging

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
from client import Client
from .stockComboBoxModel import StockComboBoxModel

logger = logging.getLogger()

class MarketViewModel(QObject):
    stockComboBoxModelChanged = pyqtSignal()

    def __init__(self, qmlContext, parent=None):
        logger.debug("")
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('marketViewModel', self)

        self._stockComboBoxModel = StockComboBoxModel()

    @pyqtProperty(StockComboBoxModel, notify=stockComboBoxModelChanged)
    def stockComboBoxModel(self):
        return self._stockComboBoxModel

    @stockComboBoxModel.setter
    def stockComboBoxModel(self, val: StockComboBoxModel):
        self._stockComboBoxModel = val
        self.stockComboBoxModelChanged.emit()

    @pyqtSlot()
    def load(self):
        logger.debug("")
        Client.getInstance().stock_list(self.on_stock_list_result)

    @pyqtSlot(list)
    def on_stock_list_result(self, result):
        logger.debug("")
        self.stockComboBoxModel = StockComboBoxModel(result)

