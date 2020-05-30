import socket
import logging

from xserver.commserver.client import Client
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
        self.__server_socket__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.__server_socket__.bind((SERVER_ADDRESS, SERVER_PORT))
            self.__server_socket__.listen(SERVER_MAX_CONNECTION)
        except socket.error as err:
            self.logger.error(err)
            # FIXME: We should do it better. Maybe ContextManager
            self.__server_socket__.close()
            exit(1)

        self.__run()

    def __init_logger(self):
        logging.basicConfig(**SERVER_LOG_CONFIG)
        self.logger = logging.getLogger("ServerCore")

    def __run(self):
        self.__server_socket__.listen(SERVER_MAX_CONNECTION)
        self.logger.debug(f"Server started ({SERVER_ADDRESS}:{SERVER_PORT})")

        while True:
            client_socket, client_addr = self.__server_socket__.accept()
            self.logger.debug(f"New client {client_addr} connected.")
            new_client = Client(client_socket, client_addr)
            self.clients.append(new_client)


if __name__ == "__main__":
    server = CoreServer()
