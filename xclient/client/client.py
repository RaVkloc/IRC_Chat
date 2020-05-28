import socket
import threading

from decorators import request_action
from threads import RecvThread
from xcomm.message import Message
from xcomm.settings import DELIMITER_BYTE, ERROR_KEY, PORT, IP
from xcomm.xcomm_moduledefs import MESSAGE_CONTENT_LENGTH, MESSAGE_ACTIONLOGIN_Login, MESSAGE_ACTIONLOGIN_Password


class Client:

    def __init__(self, client_socket: socket.socket):
        self.client_socket = client_socket

    @request_action()
    def login(self, *args, **kwargs):
        return self.client_socket


class Connection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.client = Client(self.socket)

    def __enter__(self):
        self.socket.connect((self.ip, self.port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        self.socket.close()


with Connection(ip=IP, port=PORT) as conn:
    recv_thread = RecvThread(conn.socket)
    recv_thread.run()

