from PyQt5.QtWidgets import QMessageBox

from xclient_gui.desktop.controllers.clientMediator import Mediator


class BaseWidget:
    @staticmethod
    def show_error_box(message):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()

    def __init__(self):
        self.slot = None

        self.connect_to_slot()

    def connect_to_slot(self):
        self.slot = Mediator()
        self.slot.signal.connect(self.handle_receive)

    def handle_receive(self, response):
        raise NotImplementedError
