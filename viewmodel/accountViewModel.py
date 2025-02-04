import logging

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
from client import Client

logger = logging.getLogger()

class AccountViewModel(QObject):
    accountListChanged = pyqtSignal()
    currentAccountChanged = pyqtSignal()
    currentAccountInfoChanged = pyqtSignal()

    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('accountViewModel', self)

        self._accountList = []
        self._currentAccount = ""
        self._currentAccountInfo = []

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

    @pyqtProperty(list, notify=currentAccountInfoChanged)
    def currentAccountInfo(self):
        return self._currentAccountInfo

    @currentAccountInfo.setter
    def currentAccountInfo(self, val: list):
        if self._currentAccountInfo != val:
            logger.debug(f"currentAccountInfo changed: {val}")
            self._currentAccountInfo = val
            self.currentAccountInfoChanged.emit()

    @pyqtProperty(list)
    def currentAccountInfoKeys(self):
        return ["계좌명", "예수금", "D+2추정예수금", "유가잔고평가액", "예탁자산평가액", "총매입금액", "추정예탁자산"]

    """
    method for qml side
    """

    @pyqtSlot()
    def login_info(self):
        logger.debug("")
        Client.getInstance().login_info(self.on_login_info_result)

    @pyqtSlot()
    def account_info(self):
        logger.debug("")
        Client.getInstance().account_info(self.on_account_info_result, self.currentAccount, "1001")

    """
    client model event
    """
    @pyqtSlot(list)
    def on_login_info_result(self, result):
        logger.debug(f"result:{result}")
        self.accountList = result

    @pyqtSlot(list)
    def on_account_info_result(self, result):
        logger.debug(f"typeof result len:{len(result)}")
        for i in range(len(result)):
            logger.debug(f"data {i}:{result[i]}")

        if len(result) > 0:
            self.currentAccountInfo = [[key, result[0][key]] for key in self.currentAccountInfoKeys if key in result[0]]
            logger.debug(self.currentAccountInfo)
