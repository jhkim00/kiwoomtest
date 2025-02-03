import sys
import logging

from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtQml import QQmlApplicationEngine

from model import Server, Manager
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

    manager = Manager.getInstance()
    server.commConnect.connect(manager.commConnect)

    """ 
    client code
    """
    engine = QQmlApplicationEngine()
    engine.warnings.connect(_handleQmlWarnings)

    mainViewModel = MainViewModel(engine.rootContext(), app)

    engine.load(QUrl.fromLocalFile("qml/Main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())