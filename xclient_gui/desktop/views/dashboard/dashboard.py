import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)
from xclient_gui.desktop.views.dashboard.components.spliter import Splitter


class Dashboard(QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.set_widget_default_values()

        layout = QGridLayout()
        layout.addWidget(Splitter(), 0, 0)
        # layout.addWidget(Splitter(), 1, 0)

        # self.create_username_input(layout)
        # self.create_password_input(layout)

        self.setLayout(layout)

    def set_widget_default_values(self):
        self.setWindowTitle('Login Form')
        self.resize(1000, 1000)
