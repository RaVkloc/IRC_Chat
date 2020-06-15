import datetime

from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QListWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidgetItem, QPlainTextEdit
from PyQt5.QtCore import Qt

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_SENDMESSAGE_NAME


class MessagesList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setWordWrap(True)
        self.show()


class MessageInput(QPlainTextEdit):

    def __init__(self, parent_widget: QWidget):
        super().__init__(parent_widget)
        self.parent = parent_widget

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_Return and e.key() != Qt.Key_Shift:
            self.parent.send_new_message()
        else:
            super().keyPressEvent(e)


class NewMessageWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.message_input = None

        self.create_gui()

    def create_message_input(self):
        # If pressing 'Enter' should send message uncomment line below.
        # text_edit = MessageInput(self)
        text_edit = QPlainTextEdit
        text_edit.setMaximumHeight(60)
        return text_edit

    def send_new_message(self):
        text = self.message_input.toPlainText()
        if len(text) > 0:
            self.message_input.clear()

            # TODO change the string to the modouledef param
            body = {
                MESSAGE_ACTION_SENDMESSAGE_NAME: text
            }
            self.client.send_message(body=body)

    def handle_button_clicked(self):
        self.send_new_message()

    def create_push_button(self):
        button = QPushButton(">")
        button.setMaximumWidth(50)
        button.clicked.connect(self.handle_button_clicked)
        return button

    def create_gui(self):
        self.message_input = self.create_message_input()
        push_button = self.create_push_button()

        box_layout = QHBoxLayout()
        box_layout.addWidget(self.message_input)
        box_layout.addWidget(push_button)

        box_layout.setSpacing(10)
        self.setLayout(box_layout)

    def reset_items(self):
        self.message_input.clear()


class Chat(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.new_message_input = None
        self.chat_box_layout = QVBoxLayout()
        self.chat_box_layout.setSpacing(15)

        self.messages = MessagesList()
        self.set_default_messages_text()

        self.chat_box_layout.addWidget(self.messages)

        self.setLayout(self.chat_box_layout)

    def set_default_messages_text(self):
        # TODO move strings to utils
        self.messages.addItem("Choose room to start chat.")

    def handle_joining_room(self, room_name):
        self.messages.clear()
        # TODO move strings to utils
        self.messages.addItem(f"Welcome to the {room_name} channel.")
        self.messages.addItem("")

        self.reset_input()

    def reset_input(self):
        if self.new_message_input is not None:
            self.new_message_input.reset_items()
        else:
            self.create_input()

    def create_input(self):
        self.new_message_input = NewMessageWidget(self.client)
        self.chat_box_layout.addWidget(self.new_message_input, alignment=Qt.AlignBottom)

    def remove_input(self):

        self.chat_box_layout.removeWidget(self.new_message_input)
        if self.new_message_input is not None:
            self.new_message_input.close()
            self.new_message_input = None

    def handle_new_message(self, timestamp, user, text):
        # [date] user: message
        item_template = "[{}] {}: {}"
        date = datetime.datetime.fromtimestamp(float(timestamp))
        item = item_template.format(date.strftime("%d.%m.%Y %H:%M:%S"), user, text)
        self.messages.addItem(QListWidgetItem(item))

    def show_list_users(self, list_users):

        self.messages.addItem(QListWidgetItem(''))
        # TODO move strings to utils
        title = QListWidgetItem('Currently available users on this channel:')
        title.setForeground(QColor("#07125c"))
        self.messages.addItem(title)
        users = QListWidgetItem('  ' + list_users)
        users.setForeground(QColor("#363434"))
        self.messages.addItem(users)
        self.messages.addItem(QListWidgetItem(''))

    def leave_room(self):
        self.remove_input()
        self.messages.clear()
        self.set_default_messages_text()
