import sys
import logging

from PyQt5.QtWidgets import *
from model import Server, Manager

logger = logging.getLogger()

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

    sys.exit(app.exec_())