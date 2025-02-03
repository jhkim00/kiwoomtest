import sys
import logging

import asyncio
import socketio

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from qasync import QEventLoop, asyncSlot

logger = logging.getLogger()

class Client(QObject):
    instance = None
    connect_to_server = pyqtSignal()
    login_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        logger.debug("")

        self.sio = socketio.AsyncClient()

        self.connect_to_server.connect(self.connect_async)
        self.login_signal.connect(self.login_async)

        @self.sio.on("message")
        async def on_message(data):
            logging.debug("Received from server:", data)

        @self.sio.on("login_event")
        async def on_login():
            logging.debug("login_event")

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Client()
        return cls.instance

    @asyncSlot()
    async def connect_async(self):
        logging.debug("")
        await self.sio.connect("http://localhost:5000")

    def login(self):
        logging.debug("")
        self.login_signal.emit()

    @asyncSlot()
    async def login_async(self):
        logging.debug("")
        await self.sio.emit("login")

