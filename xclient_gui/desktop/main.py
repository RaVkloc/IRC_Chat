from PyQt5.QtWidgets import (QApplication)
import sys
import threading

from xclient_gui.desktop.controllers.connection import GUIClient
from xclient_gui.desktop.controllers.navigation import ScreenController
from xserver.coreserver.coreserver_moduledefs import SERVER_ADDRESS, SERVER_PORT


class GUI:
    def __init__(self):
        self.client = None
        self.app = None
        self.controller = None

    def start_client(self):
        self.client = GUIClient(SERVER_ADDRESS, SERVER_PORT)
        thread_gui = threading.Thread(target=self.client.start, daemon=True)
        thread_gui.start()

    def start_gui(self):
        self.app = QApplication(sys.argv)
        self.controller = ScreenController(self.client)
        self.controller.show_login()
        sys.exit(self.app.exec_())

    def start(self):
        self.start_client()
        self.start_gui()


if __name__ == '__main__':
    main = GUI()
    main.start()
