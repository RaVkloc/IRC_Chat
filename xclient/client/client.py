import json
import threading
import time
from _thread import start_new_thread

from xclient.client.actions import Response
from xclient.client.connection import Connection
from xclient.client.decorators import request_action
from xclient.client.settings import CLIENT_SEND_ACTIONS


class Client:

    def __init__(self, ip, port):
        self.connection = Connection(ip=ip, port=port)
        self.token = None

    def send(self, *args, **kwargs):
        raise NotImplementedError

    def receive(self, *args, **kwargs):
        while True:
            message = self.connection.receive()
            response = Response(message)
            self.token = response.get_token()
            self.handle_receive(message)

    @request_action()
    def login(self, *args, **kwargs):
        return self.connection.socket, self.token

    @request_action()
    def register(self, *args, **kwargs):
        return self.connection.socket, self.token

    @request_action()
    def send_message(self, *args, **kwargs):
        return self.connection.socket, self.token

    def handle_receive(self, message):
        raise NotImplementedError

    def start(self):
        with self.connection as conn:
            thread_receive = threading.Thread(target=self.receive,daemon=True)
            thread_send = threading.Thread(target=self.send,daemon=True)
            thread_receive.start()
            thread_send.start()
            time.sleep(1)
            while threading.active_count() > 1:
                pass


class TerminalClient(Client):

    def send(self, *args, **kwargs):
        while True:
            action = input("Podaj nazwe akcji")
            if action not in CLIENT_SEND_ACTIONS.keys():
                continue
            body = input("Podaj JSON do wyslania")
            body = json.loads(body)
            method = getattr(self, action)
            if not method:
                continue
            method(body=body)

    def handle_receive(self, message):
        print(message.body)


class GUIClient(Client):
    pass
