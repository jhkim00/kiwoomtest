import logging

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
from client import Client

logger = logging.getLogger()

class MainViewModel(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('mainViewModel', self)

        self._connected = False

    connectedChanged = pyqtSignal()

    @pyqtProperty(bool, notify=connectedChanged)
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, val):
        if self._connected != val:
            self._connected = val
            self.connectedChanged.emit()

    @pyqtSlot()
    def login(self):
        logger.debug("")
        Client.getInstance().login()

