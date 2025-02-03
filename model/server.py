import sys
import logging

from flask import Flask
from flask_socketio import SocketIO

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QThread

logger = logging.getLogger()

class Server(QThread):
    instance = None
    commConnect = pyqtSignal()
    getLoginInfo = pyqtSignal()
    getAccountInfo = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        logger.debug("")
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, async_mode="threading")

        # 라우트 등록
        self.app.route("/")(self.index)

        # 웹소켓 이벤트 핸들러 등록
        self.socketio.on_event("connect", self.handle_connect)
        self.socketio.on_event("disconnect", self.handle_disconnect)
        self.socketio.on_event("message", self.handle_message)
        self.socketio.on_event("login", self.handle_login)
        self.socketio.on_event("login_info", self.handle_login_info)
        self.socketio.on_event("account_info", self.handle_account_info)

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Server()
        return cls.instance

    def run(self):
        self.socketio.run(self.app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)

    def notifyLoginCompleted(self):
        logger.debug("")
        self.socketio.emit("login_event")

    def notifyLoginInfo(self, info):
        logger.debug("")
        self.socketio.emit("login_info_event", info)

    """
    web socket event handler
    """
    @classmethod
    def index(cls):
        return "Flask WebSocket Server Running"

    @classmethod
    def handle_connect(cls):
        logger.debug("Client connected")

    @classmethod
    def handle_disconnect(cls):
        logger.debug("Client disconnected")

    def handle_message(self, message):
        logger.debug(f"Received: {message}")
        self.socketio.send(f"Echo: {message}")

    def handle_login(self):
        logger.debug("")
        self.commConnect.emit()

    def handle_login_info(self):
        logger.debug("")
        self.getLoginInfo.emit()

    def handle_account_info(self, data):
        logger.debug(data)
        self.getAccountInfo.emit(data)
