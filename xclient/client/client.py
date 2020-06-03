import json
import threading
import time
from _thread import start_new_thread
from functools import reduce

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
            if not self.token:
                self.token = response.get_token()
            self.handle_receive(response)

    @request_action()
    def login(self, *args, **kwargs):
        return self.connection.socket, self.token

    @request_action()
    def register(self, *args, **kwargs):
        return self.connection.socket, self.token

    @request_action()
    def join_room(self, *args, **kwargs):
        return self.connection.socket, self.token

    @request_action()
    def send_message(self, *args, **kwargs):
        return self.connection.socket, self.token

    @request_action()
    def create_room(self, *args, **kwargs):
        return self.connection.socket, self.token

    @request_action()
    def list_rooms(self, *args, **kwargs):
        return self.connection.socket, self.token

    @request_action()
    def logout(self, *args, **kwargs):
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
            print("Wybierz jedną z akcji")
            self.show_actions()
            action = input("Podaj nazwe akcji: ")
            if action not in CLIENT_SEND_ACTIONS.keys():
                continue
            method = getattr(self, action)
            if not method:
                continue

            body = input("Podaj JSON do wyslania: ")
            body = json.loads(body)

            method(body=body)

    def handle_receive(self, response:Response):
        print(response.message.body)

    def show_actions(self):
        print(" ".join(CLIENT_SEND_ACTIONS.keys()))

    def ask_arguments(self, func):
        body = {}
        for arg in func.__code__.co_varnames:
            body[arg.capitalize()] = input(f"Podaj {arg.capitalize()}: ")
        return body


