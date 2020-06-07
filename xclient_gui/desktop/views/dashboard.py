from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter, QMainWindow

from xclient_gui.desktop.views.base.BaseWidget import BaseWidget
from xclient_gui.desktop.views.components.chat import Chat
from xclient_gui.desktop.views.components.tree import Tree

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LISTROOMS_CODE, MESSAGE_ACTION, MESSAGE_ACTION_LISTROOMS_LIST, \
    MESSAGE_ACTION_JOIN_ROOM_CODE, MESSAGE_ACTION_RECVMESSAGE_CODE


class CentralWidget(QSplitter, BaseWidget):
    def __init__(self, client):
        super().__init__()

        self.tree = Tree(client)
        self.chat = Chat(client)

        self.addWidget(self.tree)
        self.addWidget(self.chat)
        self.setSizes([50, 200])
        self.setOrientation(QtCore.Qt.Horizontal)

    def handle_receive(self, response):
        print("sdfsdf")
        if response.message.header[MESSAGE_ACTION] == MESSAGE_ACTION_LISTROOMS_CODE:
            self.tree.set_room_list(response.message.body[MESSAGE_ACTION_LISTROOMS_LIST])
        elif response.message.header[MESSAGE_ACTION] == MESSAGE_ACTION_JOIN_ROOM_CODE:
            self.chat.reset_room()
        elif response.message.header[MESSAGE_ACTION] == MESSAGE_ACTION_RECVMESSAGE_CODE:
            self.chat.handle_new_message("")
        print(response.message.body)
        print(response.message.header)


class Dashboard(QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self, client):
        super().__init__()
        self.client = client

        self.set_widget_default_values()

        self.setCentralWidget(CentralWidget(self.client))

    def set_widget_default_values(self):
        self.setWindowTitle('Login Form')
        self.resize(500, 500)
