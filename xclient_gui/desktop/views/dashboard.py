from PyQt5 import QtCore
from PyQt5.QtCore import QMargins
from PyQt5.QtWidgets import QSplitter, QMainWindow, QAction, QMenu, QInputDialog

from xclient_gui.desktop.utils.messages import SERVER_ERROR, USER, LOGOUT, LOGOUT_TIP, ROOM, NEW_ROOM, NEW_ROOM_TIP, \
    LEAVE_ROOM, LEAVE_ROOM_TIP, REFRESH_LIST_ROOMS, REFRESH_LIST_ROOMS_TIP, NEW_ROOM_ENTER_NAME
from xclient_gui.desktop.views.base.BaseWidget import BaseWidget
from xclient_gui.desktop.views.components.chat import Chat
from xclient_gui.desktop.views.components.tree import Tree
from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LISTROOMS_CODE, MESSAGE_ACTION, MESSAGE_ACTION_LISTROOMS_LIST, \
    MESSAGE_ACTION_JOIN_ROOM_CODE, MESSAGE_ACTION_RECVMESSAGE_CODE, MESSAGE_STATUS, MESSAGE_STATUS_OK, \
    MESSAGE_ACTION_NEW_ROOM_ROOM_NAME, MESSAGE_ACTION_NEW_ROOM_CODE, MESSAGE_ACTION_LEAVEROOM_CODE, \
    MESSAGE_ACTION_LOGOUT_CODE, MESSAGE_ACTION_RECVMESSAGE_MESSAGE, MESSAGE_ACTION_RECVMESSAGE_TIMESTAMP, \
    MESSAGE_ACTION_RECVMESSAGE_USER, MESSAGE_ACTION_LISTUSERS_CODE, MESSAGE_ACTION_LISTUSERS_LIST, \
    MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME


class CentralWidget(QSplitter, BaseWidget):
    def __init__(self, client, on_logout):
        super().__init__()
        self.on_logout = on_logout
        self.client = client

        self.tree = None
        self.chat = None

        self.compose_widgets()
        self.set_default_splitter_settings()

    def compose_widgets(self):
        self.tree = Tree(self.client)
        self.chat = Chat(self.client)

        self.addWidget(self.tree)
        self.addWidget(self.chat)

    def set_default_splitter_settings(self):
        self.setSizes([50, 200])
        self.setOrientation(QtCore.Qt.Horizontal)

    def handle_receive_status(self, response):
        if MESSAGE_STATUS in response.message.body.keys():
            status = response.message.body[MESSAGE_STATUS]
            if status != MESSAGE_STATUS_OK:
                self.show_error_box(status)
                return False
        return True

    def handle_receive(self, response):
        try:
            header = response.message.header
            body = response.message.body
            if self.handle_receive_status(response):
                if header[MESSAGE_ACTION] == MESSAGE_ACTION_LISTROOMS_CODE:
                    self.tree.set_room_list(body[MESSAGE_ACTION_LISTROOMS_LIST])
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_JOIN_ROOM_CODE:
                    self.chat.handle_joining_room(body[MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME])
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_RECVMESSAGE_CODE:
                    if MESSAGE_ACTION_RECVMESSAGE_MESSAGE in body.keys():
                        self.chat.handle_new_message(body[MESSAGE_ACTION_RECVMESSAGE_TIMESTAMP],
                                                     body[MESSAGE_ACTION_RECVMESSAGE_USER],
                                                     body[MESSAGE_ACTION_RECVMESSAGE_MESSAGE])
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_NEW_ROOM_CODE:
                    self.tree.refresh_room_list()
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_LEAVEROOM_CODE:
                    self.tree.clear_selection()
                    self.tree.clear_highlight()
                    self.chat.leave_room()
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_LOGOUT_CODE:
                    self.on_logout.emit()
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_LISTUSERS_CODE:
                    self.chat.show_list_users(body[MESSAGE_ACTION_LISTUSERS_LIST])

        except KeyError:
            self.show_error_box(SERVER_ERROR)


class Dashboard(QMainWindow):
    on_logout = QtCore.pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client

        self.set_widget_default_values()
        self.create_menu()

        self.setCentralWidget(CentralWidget(self.client, self.on_logout))

        margins = QMargins()
        margins.setLeft(5)
        self.setContentsMargins(margins)

        self.show()

    def create_menu(self):
        self.statusBar()
        main_menu = self.menuBar()
        main_menu.setNativeMenuBar(False)

        main_menu.addMenu(self.get_room_menu())
        main_menu.addMenu(self.get_user_menu())

    def get_user_menu(self):
        user = QMenu(USER, self)

        user_logout = QAction(LOGOUT, self)
        user_logout.setStatusTip(LOGOUT_TIP)
        user_logout.triggered.connect(self.logout)

        user.addAction(user_logout)
        return user

    def get_room_menu(self):
        room = QMenu(ROOM, self)

        room_new_room = QAction(NEW_ROOM, self)
        room_new_room.setStatusTip(NEW_ROOM_TIP)
        room_new_room.triggered.connect(self.create_room)

        room_leave_room = QAction(LEAVE_ROOM, self)
        room_leave_room.setStatusTip(LEAVE_ROOM_TIP)
        room_leave_room.triggered.connect(self.leave_room)

        room_refresh_list_rooms = QAction(REFRESH_LIST_ROOMS, self)
        room_refresh_list_rooms.setStatusTip(REFRESH_LIST_ROOMS_TIP)
        room_refresh_list_rooms.triggered.connect(self.refresh_room_list)

        room_refresh_list_rooms = QAction("Get users list", self)
        room_refresh_list_rooms.setStatusTip(REFRESH_LIST_ROOMS_TIP)
        room_refresh_list_rooms.triggered.connect(self.get_users_list)

        room.addAction(room_new_room)
        room.addAction(room_leave_room)
        room.addAction(room_refresh_list_rooms)
        return room

    def logout(self):
        self.client.logout()

    def create_room(self):
        text, ok = QInputDialog.getText(self, NEW_ROOM, NEW_ROOM_ENTER_NAME)
        if ok:
            body = {
                MESSAGE_ACTION_NEW_ROOM_ROOM_NAME: text
            }
            self.client.create_room(body=body)

    def leave_room(self):
        self.client.leave_room()

    def refresh_room_list(self):
        self.client.list_rooms()

    def get_users_list(self):
        self.client.list_user()

    def set_widget_default_values(self):
        self.setWindowTitle("IRC Chat")
        self.resize(500, 500)
