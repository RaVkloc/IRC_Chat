import json
import threading
import time
import logging

from xclient.client.actions import Response
from xclient.client.connection import Connection
from xclient.client.decorators import request_action
from xclient.client.settings import CLIENT_SEND_ACTIONS, RESPONSE_ACTION_HEADER, STATUS_KEY, SUCCESS_RESPONSES, \
    CLIENT_LOG_CONFIG


class Client:

    def __init__(self, ip, port):
        self.connection = Connection(ip=ip, port=port, client=self)
        self.token = None

        self.__init_logger()

    def __init_logger(self):
        logging.basicConfig(**CLIENT_LOG_CONFIG)
        self.logger = logging.getLogger("Client")

    def send(self, *args, **kwargs):
        raise NotImplementedError

    def receive(self, *args, **kwargs):
        while True:
            message = self.connection.receive()
            self.logger.debug(f"Received from server: {message.get_complete_message()}")
            response = Response(message)
            if not self.token:
                self.token = response.get_token()

            self.clear_token_if_needed(message)
            self.handle_receive(response)

    def clear_token_if_needed(self, message):
        if message.get_header_param(RESPONSE_ACTION_HEADER) == str(CLIENT_SEND_ACTIONS['logout']) and \
                message.get_body_param(STATUS_KEY).lower() in SUCCESS_RESPONSES:
            self.token = None

    @request_action()
    def login(self, *args, **kwargs):
        return self.connection.get_socket(), self.token

    @request_action()
    def register(self, *args, **kwargs):
        return self.connection.get_socket(), self.token

    @request_action()
    def join_room(self, *args, **kwargs):
        return self.connection.get_socket(), self.token

    @request_action()
    def leave_room(self, *args, **kwargs):
        return self.connection.get_socket(), self.token

    @request_action()
    def send_message(self, *args, **kwargs):
        return self.connection.get_socket(), self.token

    @request_action()
    def create_room(self, *args, **kwargs):
        return self.connection.get_socket(), self.token

    @request_action()
    def list_rooms(self, *args, **kwargs):
        return self.connection.get_socket(), self.token

    @request_action()
    def logout(self, *args, **kwargs):
        return self.connection.get_socket(), self.token

    @request_action()
    def list_user(self, *args, **kwargs):
        return self.connection.get_socket(), self.token

    def handle_receive(self, message):
        raise NotImplementedError

    def start(self):
        self.logger.debug("Client starting...")
        try:
            self.connection.connect()
        except ConnectionRefusedError:
            self.logger.debug("Some errors occurred. Unable to start properly.")
            return

        with self.connection:
            thread_receive = threading.Thread(target=self.receive, daemon=True)
            thread_send = threading.Thread(target=self.send, daemon=True)
            thread_receive.start()
            thread_send.start()
            time.sleep(1)
            while threading.active_count() > 1:
                pass


class TerminalClient(Client):

    def send(self, *args, **kwargs):
        while True:
            print("Choose one action from following:")
            self.show_actions()
            action = input("Action: ")
            if action not in CLIENT_SEND_ACTIONS.keys():
                continue
            method = getattr(self, action)
            if not method:
                print("Such action does not exists.")
                continue

            body = input("Put JSON to send: ")
            body = json.loads(body)

            method(body=body)

            # FIXME: Temporary solution for printing result in incorrect place.
            print("Response: ", end='')
            time.sleep(1)

    def handle_receive(self, response: Response):
        print(response.message.body)

    def show_actions(self):
        print(" ".join(CLIENT_SEND_ACTIONS.keys()))

    def ask_arguments(self, func):
        body = {}
        for arg in func.__code__.co_varnames:
            body[arg.capitalize()] = input(f"Podaj {arg.capitalize()}: ")
        return body
