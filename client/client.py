import sys
import logging

import asyncio
import socketio

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from qasync import QEventLoop, asyncSlot

logger = logging.getLogger()

class Client(QObject):
    instance = None
    """
    signals for async call
    """
    connect_to_server_signal = pyqtSignal()
    login_signal = pyqtSignal()
    login_info_signal = pyqtSignal()
    account_info_signal = pyqtSignal(dict)

    """
    signals for event callback
    """
    login_result = pyqtSignal()
    login_info_result = pyqtSignal(list)
    account_info_result = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        logger.debug("")

        self.sio = socketio.AsyncClient()

        """
        connect signals for async call
        """
        self.connect_to_server_signal.connect(self.connect_async)
        self.login_signal.connect(self.login_async)
        self.login_info_signal.connect(self.login_info_async)
        self.account_info_signal.connect(self.account_info_async)

        """
        slots for callback
        """
        self._login_result_slot = None
        self._login_info_result_slot = None
        self._account_info_result_slot = None

        @self.sio.on("message")
        async def on_message(data):
            logging.debug("Received from server:", data)

        @self.sio.on("login_event")
        async def on_login():
            logging.debug("login_event")
            self.login_result.emit()

        @self.sio.on("login_info_event")
        async def on_login_info(data):
            logging.debug(f"login_info_event data:{data}")
            self.login_info_result.emit(data)

        @self.sio.on("account_info_event")
        async def on_account_info(data):
            logging.debug(f"account_info_event data:{data}")
            self.account_info_result.emit(data)

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Client()
        return cls.instance

    def is_sever_connected(self):
        return self.sio and self.sio.connected

    def connect_to_server(self):
        logging.debug("")
        self.connect_to_server_signal.emit()

    """
    async functions
    """
    @asyncSlot()
    async def connect_async(self):
        logging.debug("")
        await self.sio.connect("http://localhost:5000")
        if not self.sio.connected:
            logger.debug("web socket server connection failed...")
            sys.exit(-1)

    @asyncSlot()
    async def login_async(self):
        logging.debug("")
        await self.sio.emit("login")

    @asyncSlot()
    async def login_info_async(self):
        logging.debug("")
        await self.sio.emit("login_info")

    @asyncSlot(dict)
    async def account_info_async(self, data):
        logging.debug("")
        await self.sio.emit("account_info", data)

    """
    public method
    """
    def login(self, callback):
        logging.debug("")
        if not self.is_sever_connected():
            logger.debug("web socket server is not connected...")
            pass
        self.login_signal.emit()
        if self._login_result_slot != callback:
            self.login_result.connect(callback)

    def login_info(self, callback):
        logging.debug("")
        self.login_info_signal.emit()
        if self._login_info_result_slot != callback:
            self.login_info_result.connect(callback)

    def account_info(self, callback, account_no, screen_no):
        logging.debug("")
        self.account_info_signal.emit({"account_no": account_no, "screen_no": screen_no})
        if self._account_info_result_slot != callback:
            self.account_info_result.connect(callback)
