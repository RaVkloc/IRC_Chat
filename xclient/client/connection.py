import socket

from xclient.client.utils import Reciver
from xcomm.message import Message
from xcomm.xcomm_moduledefs import MESSAGE_CONTENT_LENGTH


class Connection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()

    def __enter__(self):
        self.socket.connect((self.ip, self.port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        self.socket.close()

    def send(self, message:Message):
        return self.socket.sendall(message.convert_message_to_bytes())

    def receive(self):
        m = Message()
        headers = Reciver.recive_headers(self.socket)
        m.set_header_bytes(headers)
        content_length = m.get_header_param(MESSAGE_CONTENT_LENGTH)
        body = Reciver.recive_body(self.socket, content_length)
        m.set_body_bytes(body)
        return m
