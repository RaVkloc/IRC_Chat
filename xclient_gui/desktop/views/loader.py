import asyncio

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from xclient_gui.desktop.utils.messages import LOADING


class Loader(QWidget):
    handle_successful_connection = QtCore.pyqtSignal()
    handle_error_connection = QtCore.pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.create_gui()

    def create_gui(self):
        layout = QVBoxLayout()
        message = self.get_message()

        layout.addWidget(message)
        layout.setAlignment(message, QtCore.Qt.AlignHCenter)
        self.setLayout(layout)

    def get_message(self):
        label = LOADING + '...'
        return QLabel(label)

    def asynchronously_observe_client_connection(self):
        asyncio.run(self.listen_to_server_connection())

    async def listen_to_server_connection(self):
        while self.client.connection.connected is None:
            pass
        if self.client.connection.connected:
            self.handle_successful_connection.emit()
        else:
            self.handle_error_connection.emit()
