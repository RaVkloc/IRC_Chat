import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)


class LoginForm(QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.lineEdit_username = None
        self.lineEdit_password = None

        self.create_gui()

    def create_gui(self):
        self.set_widget_default_values()

        layout = QGridLayout()
        self.create_username_input(layout)
        self.create_password_input(layout)
        self.create_login_button(layout)

        self.setLayout(layout)

    def set_widget_default_values(self):
        self.setWindowTitle('Login Form')
        self.resize(500, 120)

    def create_username_input(self, layout):
        label_name = QLabel('<font size="4"> Username: </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

    def create_password_input(self, layout):
        label_password = QLabel('<font size="4"> Password: </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

    def create_login_button(self, layout):
        button_login = QPushButton('Login')
        button_login.clicked.connect(self.login)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

    def login(self):

        if self.lineEdit_username.text() == 'a' and self.lineEdit_password.text() == 'a':
            # dashboard = Dashboard()
            # dashboard.show()
            # self.hide()
            # app.quit()
            self.switch_window.emit()

        else:
            msg = QMessageBox()
            msg.setText('Incorrect Password')
            msg.exec_()


