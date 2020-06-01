import socket
import logging

from xserver.commserver.client import Client
from xserver.commserver.connection import Connection
from xserver.coreserver.coreserver_moduledefs import *


class CoreServer(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, type(cls)):
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.__init_logger()
        self.clients = []
        self.connection = Connection(SERVER_ADDRESS, SERVER_PORT)

    def __init_logger(self):
        logging.basicConfig(**SERVER_LOG_CONFIG)
        self.logger = logging.getLogger("ServerCore")

    def run(self):
        with self.connection as conn:
            self.logger.debug(f"Server started ({SERVER_ADDRESS}:{SERVER_PORT})")
            while True:
                client_socket, client_addr = conn.socket.accept()
                self.logger.debug(f"New client {client_addr} connected.")
                new_client = Client(client_socket, client_addr)
                self.clients.append(new_client)


if __name__ == "__main__":
    server = CoreServer()
    server.run()
