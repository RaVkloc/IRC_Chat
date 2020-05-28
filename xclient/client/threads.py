import socket
from threading import Thread

from handlers import MessageHandler
from utils import Reciver
from xcomm.message import Message
from xcomm.xcomm_moduledefs import MESSAGE_CONTENT_LENGTH


class RecvThread(Thread):
    def __init__(self, s:socket.socket):
        super(RecvThread, self).__init__()
        self.s = s

    def handle_recv_thread(self):
        while True:
            m = Message()
            headers = Reciver.recive_headers(self.s)
            m.set_header_bytes(headers)
            content_length = m.get_header_param(MESSAGE_CONTENT_LENGTH)
            body = Reciver.recive_body(self.s, content_length)
            m.set_body_bytes(body)
            message_handler = MessageHandler(m)
            print(message_handler.client_message())

    def run(self) -> None:
        self.handle_recv_thread()
