import sys
import logging
import pythoncom
import time
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

logger = logging.getLogger()

class Kiwoom(QObject):
    instance = None
    loginCompleted = pyqtSignal()

    def __init__(self):
        super().__init__()
        logger.debug("")
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        self.login = False

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Kiwoom()
        return cls.instance

    def CommConnect(self):
        logger.debug("")
        self.ocx.dynamicCall("CommConnect()")
        while self.login is False:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.1)

    def OnEventConnect(self, err_code):
        self.login = True
        logger.debug(f"login is done err_code: {err_code}")
        self.loginCompleted.emit()