import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QGridLayout, QMessageBox)
from xclient_gui.desktop.controllers.clientMediator import Mediator
from xclient_gui.desktop.views.components.formInput import FormInput


class RegisterForm(QWidget):
    open_next_screen = QtCore.pyqtSignal()
    open_registration = QtCore.pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.slot = None
        
        self.lineEdit_username = None
        self.lineEdit_password = None
        self.lineEdit_confirm_password = None

        self.connect_to_slot()
        self.create_gui()

    def connect_to_slot(self):
        self.slot = Mediator()
        self.slot.signal.connect(self.handle_receive)

    def handle_receive(self, response):
        status = response.message.body['Status']
        if status == 'OK':
            self.open_next_screen.emit()
        else:
            msg = QMessageBox()
            msg.setText(status)
            msg.exec_()

    def create_gui(self):
        self.set_widget_default_values()

        layout = QGridLayout()
        self.create_username_input(layout)
        self.create_password_input(layout)
        self.create_login_button(layout)
        self.create_register_encouragement(layout)

        self.setLayout(layout)

    def set_widget_default_values(self):
        self.setWindowTitle('Login Form')
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

    def create_login_button(self, layout):
        button_login = QPushButton('Login')
        button_login.clicked.connect(self.login)
        button_login.setStyleSheet("padding-top: 5px; padding-bottom: 5px;")
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

    def create_register_encouragement(self, layout):
        register = QPushButton("Don't have account? REGISTER")
        register.clicked.connect(self.asd)
        register.setStyleSheet("font-size: 9px;")
        layout.addWidget(register, 3, 2, 1, 2)

    def asd(self):
        self.open_registration.emit()

    def login(self):
        login = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        body = {
            "login": login,
            "password": password
        }
        self.client.login(body=body)
