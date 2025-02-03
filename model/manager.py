import sys
import logging

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from .kiwoom import Kiwoom
from .server import Server

logger = logging.getLogger()

class Manager(QObject):
    instance = None

    def __init__(self):
        super().__init__()
        self.kw = Kiwoom.getInstance()
        self.kw.loginCompleted.connect(self.onLoginCompleted)
        self.server = Server.getInstance()

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Manager()
        return cls.instance

    @pyqtSlot()
    def commConnect(self):
        logger.debug("")
        self.kw.CommConnect()

    @pyqtSlot()
    def onLoginCompleted(self):
        logger.debug("")
        self.server.notifyLoginCompleted()
