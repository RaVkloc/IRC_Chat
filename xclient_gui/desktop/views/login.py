from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QGridLayout)

from xclient_gui.desktop.utils.messages import USERNAME_INPUT_LABEL, USERNAME_INPUT_PLACEHOLDER, PASSWORD_INPUT_LABEL, \
    PASSWORD_INPUT_PLACEHOLDER, REGISTER_INCENTIVE, LOGIN
from xclient_gui.desktop.views.components.formInput import FormInput
from xclient_gui.desktop.views.base.BaseWidget import BaseWidget
from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LOGIN_LOGIN, MESSAGE_ACTION_LOGIN_PASSWORD, MESSAGE_STATUS, \
    MESSAGE_STATUS_OK


class LoginForm(QWidget, BaseWidget):
    open_next_screen = QtCore.pyqtSignal()
    open_registration = QtCore.pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.lineEdit_username = None
        self.lineEdit_password = None

        self.create_gui()

    def handle_receive(self, response):
        status = response.message.body[MESSAGE_STATUS]
        if status == MESSAGE_STATUS_OK:
            self.open_next_screen.emit()
        else:
            self.show_error_box(status)

    def create_gui(self):

        layout = QGridLayout()
        self.create_username_input(layout)
        self.create_password_input(layout)
        self.create_login_button(layout)
        self.create_register_encouragement(layout)

        self.setLayout(layout)

    def create_username_input(self, layout):
        label_name, self.lineEdit_username = FormInput(USERNAME_INPUT_LABEL, USERNAME_INPUT_PLACEHOLDER).get_input()

        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

    def create_password_input(self, layout):
        label_password, self.lineEdit_password = FormInput(PASSWORD_INPUT_LABEL, PASSWORD_INPUT_PLACEHOLDER).get_input()
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

    def create_login_button(self, layout):
        button_login = QPushButton(LOGIN)
        button_login.clicked.connect(self.login)
        button_login.setStyleSheet("padding-top: 5px; padding-bottom: 5px;")
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

    def create_register_encouragement(self, layout):
        register = QPushButton(REGISTER_INCENTIVE)
        register.clicked.connect(self.show_register_screen)
        register.setStyleSheet("font-size: 9px;")
        layout.addWidget(register, 3, 2, 1, 2)

    def show_register_screen(self):
        self.open_registration.emit()

    def login(self):
        login = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        body = {
            MESSAGE_ACTION_LOGIN_LOGIN: login,
            MESSAGE_ACTION_LOGIN_PASSWORD: password
        }
        self.client.login(body=body)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key_Return:
            self.login()
        else:
            super().keyPressEvent(a0)
