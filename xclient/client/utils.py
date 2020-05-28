import socket
import types

from settings import BASE_HEADERS, CLIENT_SEND_ACTIONS
from xcomm.message import Message
from xcomm.settings import DELIMITER_BYTE


class Reciver:

    @staticmethod
    def recive_headers( s: socket.socket):
        headers = b''
        while True:
            if 2 * DELIMITER_BYTE in headers:
                break
            recv_byte = s.recv(1)
            headers += recv_byte
        headers = headers.rstrip(DELIMITER_BYTE)
        return headers

    @staticmethod
    def recive_body(s: socket.socket, content_length):
        return s.recv(int(content_length))


class Sender:
    @staticmethod
    def send_message(f: types.FunctionType, *args, **kwargs):
        try:
            body = kwargs.get('body')
            headers = BASE_HEADERS.update(kwargs.get('headers', {}))
            if not headers:
                headers = BASE_HEADERS
            headers.update({'action': CLIENT_SEND_ACTIONS[f.__name__]})
            message = Message(header=headers, body=body)
            socket_ = f(*args, **kwargs)
            socket_.sendall(message.convert_message_to_bytes())
        except KeyError:
            raise KeyError(f"There is no action for {f.name} function")
