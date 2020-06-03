from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QGridLayout)

from xclient_gui.desktop.views.components.formInput import FormInput
from xclient_gui.desktop.views.base.BaseWidget import BaseWidget
from xcomm.xcomm_moduledefs import MESSAGE_ACTION_REGISTER_LOGIN, MESSAGE_ACTION_REGISTER_PASSWORD


class RegisterForm(QWidget, BaseWidget):
    open_next_screen = QtCore.pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.lineEdit_username = None
        self.lineEdit_password = None
        self.lineEdit_confirm_password = None

        self.create_gui()

    def handle_receive(self, response):
        status = response.message.body['Status']
        if status == 'OK':
            self.open_next_screen.emit()
        else:
            self.show_error_box(status)

    def create_gui(self):
        self.set_widget_default_values()

        layout = QGridLayout()
        self.create_username_input(layout)
        self.create_password_input(layout)
        self.create_confirm_password_input(layout)
        self.create_register_button(layout)

        self.setLayout(layout)

    def set_widget_default_values(self):
        self.setWindowTitle('Register')
        self.resize(500, 120)

    def create_username_input(self, layout):
        label_name, self.lineEdit_username = FormInput('Username:', "Enter username").get_input()

        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

    def create_password_input(self, layout):
        label_password, self.lineEdit_password = FormInput('Password:', "Enter password").get_input()
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

    def create_confirm_password_input(self, layout):
        label_confirm_password, self.lineEdit_confirm_password = FormInput('Confirm Password:',
                                                                           "Confirm your password").get_input()
        self.lineEdit_confirm_password.setEchoMode(QLineEdit.Password)

        layout.addWidget(label_confirm_password, 2, 0)
        layout.addWidget(self.lineEdit_confirm_password, 2, 1)

    def create_register_button(self, layout):
        button_register = QPushButton('Register')
        button_register.clicked.connect(self.register)
        button_register.setStyleSheet("padding-top: 5px; padding-bottom: 5px;")
        layout.addWidget(button_register, 3, 0, 1, 2)

    def register(self):
        login = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        confirm_password = self.lineEdit_confirm_password.text()
        if password == confirm_password:
            body = {
                MESSAGE_ACTION_REGISTER_LOGIN: login,
                MESSAGE_ACTION_REGISTER_PASSWORD: password
            }
            self.client.register(body=body)
        else:
            self.show_error_box("Passwords are not equal.")
