from xclient.client.client import Client
from xclient.client.actions import Response

from xclient_gui.desktop.controllers.clientMediator import Mediator


class GUIClient(Client):
    def __init__(self, ip, port):
        super().__init__(ip, port)

        self.slot = None

        self.connect_to_slot()

    def connect_to_slot(self):
        self.slot = Mediator().signal

    def handle_receive(self, response: Response):
        self.slot.emit(response)
        print(response.message.body)

    def send(self):
        pass
