import socket
import types

from xclient.client.settings import BASE_HEADERS, CLIENT_SEND_ACTIONS, TOKEN_KEY
from xcomm.message import Message
from xcomm.settings import DELIMITER_BYTE


class Reciver:

    @staticmethod
    def receive_headers(s: socket.socket):
        """
        Method receive headers until dbl delimiter sign.
        :param s: socket
        :return: received headers
        """
        headers = b''
        while True:
            if 2 * DELIMITER_BYTE in headers:
                break
            recv_byte = s.recv(1)
            headers += recv_byte
        headers = headers.rstrip(DELIMITER_BYTE)
        return headers

    @staticmethod
    def receive_body(s: socket.socket, content_length):
        return s.recv(int(content_length))


class Sender:
    @staticmethod
    def send_message(f: types.FunctionType, *args, **kwargs):
        """

        :param f: request action
        :param args:
        :param kwargs: message content
        :return:
        """
        try:
            body = kwargs.get('body')
            headers = {}
            headers.update({'Action': CLIENT_SEND_ACTIONS[f.__name__]})
            message = Message(header=headers, body=body)
            socket_, token = f(*args, **kwargs)
            if token:
                message.add_header_param(TOKEN_KEY, token)
            socket_.sendall(message.convert_message_to_bytes())
        except KeyError:
            raise KeyError(f"There is no action for {f.name} function")
