from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter, QMainWindow, QAction, QMenu, QInputDialog

from xclient_gui.desktop.views.base.BaseWidget import BaseWidget
from xclient_gui.desktop.views.components.chat import Chat
from xclient_gui.desktop.views.components.tree import Tree

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LISTROOMS_CODE, MESSAGE_ACTION, MESSAGE_ACTION_LISTROOMS_LIST, \
    MESSAGE_ACTION_JOIN_ROOM_CODE, MESSAGE_ACTION_RECVMESSAGE_CODE, MESSAGE_ACTION_SENDMESSAGE_CODE, \
    MESSAGE_ACTION_SENDMESSAGE_NAME, MESSAGE_STATUS, MESSAGE_STATUS_OK, MESSAGE_ACTION_NEW_ROOM_ROOM_NAME, \
    MESSAGE_ACTION_NEW_ROOM_CODE, MESSAGE_ACTION_LEAVEROOM_CODE, MESSAGE_ACTION_LOGOUT_CODE


class CentralWidget(QSplitter, BaseWidget):
    def __init__(self, client, on_logout):
        super().__init__()
        self.on_logout = on_logout
        self.tree = Tree(client)
        self.chat = Chat(client)

        self.addWidget(self.tree)
        self.addWidget(self.chat)
        self.setSizes([50, 200])
        self.setOrientation(QtCore.Qt.Horizontal)

    def handle_recieve_status(self, response):
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
            if self.handle_recieve_status(response):
                if header[MESSAGE_ACTION] == MESSAGE_ACTION_LISTROOMS_CODE:
                    self.tree.set_room_list(body[MESSAGE_ACTION_LISTROOMS_LIST])
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_JOIN_ROOM_CODE:
                    self.chat.handle_joining_room()
                #     TODO chane actions "*_SENDMESSAGE_*" TO "*_RECVMESSAGE_*"
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_SENDMESSAGE_CODE:
                    if MESSAGE_ACTION_SENDMESSAGE_NAME in body.keys():
                        self.chat.handle_new_message(body[MESSAGE_ACTION_SENDMESSAGE_NAME])
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_NEW_ROOM_CODE:
                    self.tree.refresh_room_list()
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_LEAVEROOM_CODE:
                    self.tree.clear_selection()
                    self.chat.leave_room()
                elif header[MESSAGE_ACTION] == MESSAGE_ACTION_LOGOUT_CODE:
                    self.on_logout.emit()

        except KeyError:
            self.show_error_box("Server error.")


class Dashboard(QMainWindow):
    on_logout = QtCore.pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client

        self.set_widget_default_values()
        self.create_menu()

        self.setCentralWidget(CentralWidget(self.client, self.on_logout))
        self.show()

    def create_menu(self):
        self.statusBar()
        main_menu = self.menuBar()
        main_menu.setNativeMenuBar(False)

        room = self.get_room_menu()
        user = self.get_user_menu()

        main_menu.addMenu(room)
        main_menu.addMenu(user)

    def get_user_menu(self):
        user = QMenu("User", self)

        user_logout = QAction("Logout", self)
        user_logout.setStatusTip('Logout from current account.')
        user_logout.triggered.connect(self.logout)

        user.addAction(user_logout)
        return user

    def get_room_menu(self):
        room = QMenu("Room", self)

        room_new_room = QAction("New room", self)
        room_new_room.setStatusTip('Create new room')
        room_new_room.triggered.connect(self.create_room)

        room_leave_room = QAction("Leave room", self)
        room_leave_room.setStatusTip('Leave from the current room')
        room_leave_room.triggered.connect(self.leave_room)

        room_refresh_list_rooms = QAction("Refresh rooms", self)
        room_refresh_list_rooms.setStatusTip('Refresh the list of rooms')
        room_refresh_list_rooms.triggered.connect(self.refresh_room_list)

        room.addAction(room_new_room)
        room.addAction(room_leave_room)
        room.addAction(room_refresh_list_rooms)

        return room

    def logout(self):
        self.client.logout()

    def create_room(self):
        text, ok = QInputDialog.getText(self, 'New room', 'Enter room name:')
        if ok:
            body = {
                MESSAGE_ACTION_NEW_ROOM_ROOM_NAME: text
            }
            self.client.create_room(body=body)

    def leave_room(self):
        self.client.leave_room()

    def refresh_room_list(self):
        self.client.list_rooms()

    def set_widget_default_values(self):
        self.setWindowTitle('Login Form')
        self.resize(500, 500)
