import logging

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
from client import Client

logger = logging.getLogger()

class MainViewModel(QObject):
    login_completedChanged = pyqtSignal()
    accountListChanged = pyqtSignal()
    currentAccountChanged = pyqtSignal()

    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('mainViewModel', self)

        self._login_completed = False

        self._accountList = []
        self._currentAccount = ""

    @pyqtProperty(bool, notify=login_completedChanged)
    def login_completed(self):
        return self._login_completed

    @login_completed.setter
    def login_completed(self, val):
        if self._login_completed != val:
            self._login_completed = val
            self.login_completedChanged.emit()

    @pyqtProperty(QVariant, notify=accountListChanged)
    def accountList(self):
        return self._accountList

    @accountList.setter
    def accountList(self, val: QVariant):
        self._accountList = val
        self.accountListChanged.emit()

    @pyqtProperty(str, notify=currentAccountChanged)
    def currentAccount(self):
        return self._currentAccount

    @currentAccount.setter
    def currentAccount(self, val: str):
        if self._currentAccount != val:
            logger.debug(f"currentAccount changed: {val}")
            self._currentAccount = val
            self.currentAccountChanged.emit()

    """
    method for qml side
    """
    @pyqtSlot()
    def login(self):
        logger.debug("")
        Client.getInstance().login(self.on_login_result)

    @pyqtSlot()
    def login_info(self):
        logger.debug("")
        Client.getInstance().login_info(self.on_login_info_result)

    @pyqtSlot()
    def account_info(self):
        logger.debug("")
        Client.getInstance().account_info(self.on_account_info_result, self.accountList[0], "1001")

    """
    client model event
    """
    @pyqtSlot()
    def on_login_result(self):
        logger.debug("")
        self.login_completed = True

    @pyqtSlot(list)
    def on_login_info_result(self, result):
        logger.debug(f"result:{result}")
        self.accountList = result

    @pyqtSlot(dict)
    def on_account_info_result(self, result):
        logger.debug(f"result:{result}")



