import logging

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant

from client import Client

logger = logging.getLogger()

class MainViewModel(QObject):
    login_completedChanged = pyqtSignal()

    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('mainViewModel', self)

        self._login_completed = False

    @pyqtProperty(bool, notify=login_completedChanged)
    def login_completed(self):
        return self._login_completed

    @login_completed.setter
    def login_completed(self, val):
        if self._login_completed != val:
            self._login_completed = val
            self.login_completedChanged.emit()

    """
    method for qml side
    """
    @pyqtSlot()
    def login(self):
        logger.debug("")
        Client.getInstance().login(self.on_login_result)

    """
    client model event
    """
    @pyqtSlot()
    def on_login_result(self):
        logger.debug("")
        self.login_completed = True
