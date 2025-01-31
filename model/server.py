import eventlet
eventlet.monkey_patch()  # 반드시 최상단에 위치해야 함

import sys
import logging

from flask import Flask
from flask_socketio import SocketIO

from .kiwoom import Kiwoom

logger = logging.getLogger()

class Server:
    def __init__(self):
        logger.debug("")
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, async_mode="eventlet", cors_allowed_origins="*")

        # 라우트 등록
        self.app.route("/")(self.index)

        # 웹소켓 이벤트 핸들러 등록
        self.socketio.on_event("connect", self.handle_connect)
        self.socketio.on_event("disconnect", self.handle_disconnect)
        self.socketio.on_event("message", self.handle_message)
        self.socketio.on_event("login", self.handle_login)

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

    @classmethod
    def handle_login(cls):
        logger.debug("")
        Kiwoom.getInstance().CommConnect()

    def start(self):
        # Flask-SocketIO 실행 (eventlet 사용)
        self.socketio.run(self.app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)