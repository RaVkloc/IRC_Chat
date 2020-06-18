from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QApplication, QSizePolicy, \
    QGridLayout

from xclient_gui.desktop.utils.messages import OK, CONNECTION_FAILED_TRY_LATER, CONNECTION_FAILED
from xclient_gui.desktop.views.base.BaseWidget import BaseWidget


class ConnectionFail(QWidget):

    def __init__(self, ):
        super().__init__()
        self.create_gui()

    def create_gui(self):
        layout = QVBoxLayout()
        message = self.get_message()
        button = self.get_button()

        layout.addWidget(message)
        layout.setAlignment(message, QtCore.Qt.AlignHCenter)

        layout.addWidget(button)
        layout.setAlignment(button, QtCore.Qt.AlignHCenter)

        self.setLayout(layout)

    def get_message(self):
        return QLabel(CONNECTION_FAILED_TRY_LATER)

    def get_button(self):
        button = QPushButton(OK)
        button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.clicked.connect(QApplication.quit)
        return button
