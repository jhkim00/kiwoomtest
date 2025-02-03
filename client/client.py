import sys
import logging

import asyncio
import socketio

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

logger = logging.getLogger()

class Client(QObject):
    instance = None

    def __init__(self):
        super().__init__()
        logger.debug("")

        self.sio = socketio.AsyncClient()

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

    def login(self):
        logging.debug("")

