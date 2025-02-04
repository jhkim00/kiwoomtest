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

        self.server.commConnect.connect(self.commConnect)
        self.server.getLoginInfo.connect(self.getLoginInfo)
        self.server.getAccountInfo.connect(self.getAccountInfo)

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
    def getLoginInfo(self):
        logger.debug("")
        data = self.kw.GetLoginInfo("ACCNO")
        logger.debug(data)
        self.server.notifyLoginInfo(data)

    @pyqtSlot(dict)
    def getAccountInfo(self, data):
        logger.debug("")
        self.kw.trCallbacks["OPW00004"] = self.onAccountInfo
        self.kw.SetInputValue(id="계좌번호", value=data["account_no"])
        self.kw.SetInputValue(id="비밀번호", value="")
        self.kw.SetInputValue(id="상장폐지조회구분", value="0")
        self.kw.SetInputValue(id="비밀번호입력매체구분", value="00")
        self.kw.CommRqData(rqname="계좌평가현황요청", trcode="OPW00004", next=0, screen=data["screen_no"])

    @pyqtSlot()
    def onLoginCompleted(self):
        logger.debug("")
        self.server.notifyLoginCompleted()

    def onAccountInfo(self, screen, rqname, trcode, record, next):
        logger.debug("")
        if rqname == "계좌평가현황요청":
            cnt = self.kw.GetRepeatCnt(trcode, rqname)
            logger.debug(f"cnt:{cnt}")
            outList = []
            for i in range(cnt):
                outDict = {}
                outKeys = ['계좌명', '예수금', 'D+2추정예수금', '유가잔고평가액', '예탁자산평가액', '총매입금액', '추정예탁자산']
                outKeys2 = ['종목코드', '종목명', '보유수량', '평균단가', '현재가', '평가금액', '손익금액', '손익율']
                for key in outKeys:
                    strData = self.kw.GetCommData(trcode, rqname, i, key)
                    logger.debug(f"{key}:{strData}")
                    outDict[key] = strData
                for key in outKeys2:
                    strData = self.kw.GetCommData(trcode, rqname, i, key)
                    logger.debug(f"{key}:{strData}")
                    outDict[key] = strData
                outList.append(outDict)

            self.server.notifyAccountInfo(outList)
