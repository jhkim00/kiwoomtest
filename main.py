import sys
import logging
import asyncio
import time

from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtQml import QQmlApplicationEngine
from qasync import QEventLoop, asyncSlot

from model import Server, Manager
from client import Client
from viewmodel import MainViewModel

logger = logging.getLogger()

def _handleQmlWarnings(warnings):
    for warning in warnings:
        print("QML Warning:", warning.toString())

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    logger.propagate = 0
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(thread)d][%(filename)s:%(funcName)s:%(lineno)d]'
                                  ' %(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    server = Server.getInstance()
    server.start()

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    manager = Manager.getInstance()

    """ 
    client code
    """
    client = Client.getInstance()
    client.connect_to_server()

    """
    GUI start
    """
    engine = QQmlApplicationEngine()
    engine.warnings.connect(_handleQmlWarnings)

    mainViewModel = MainViewModel(engine.rootContext(), app)

    engine.load(QUrl.fromLocalFile("qml/Main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    with loop:
        loop.run_forever()