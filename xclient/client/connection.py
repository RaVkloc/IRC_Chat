import socket
import ssl
import logging

from xclient.client.settings import TLS, CERT_PATH, SERVER_CERT, KEY_PATH
from xclient.client.utils import Receiver
from xcomm.message import Message
from xcomm.xcomm_moduledefs import MESSAGE_CONTENT_LENGTH
from xserver.coreserver.coreserver_moduledefs import SERVER_HOSTNAME

logger = logging.getLogger("Connection")


class Connection:
    def __init__(self, ip, port, client):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.secure_socket = None
        self.connected = None
        self.client = client
        logger.debug("Creating new connection to: {}:{}".format(ip, port))

    def connect(self):
        try:
            logger.debug("Trying to connect to server.")
            self.socket.connect((self.ip, self.port))
            logger.debug("Connected SUCCESSFULLY.")
        except socket.error as e:
            logger.debug("Connection FAILED: " + str(e))
            raise ConnectionRefusedError(e)

    def __enter__(self):
        logger.debug("Testing if TLS enabled.")
        if TLS:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.context.verify_mode = ssl.CERT_REQUIRED
            self.context.load_verify_locations(SERVER_CERT)
            self.context.load_cert_chain(certfile=CERT_PATH, keyfile=KEY_PATH)
            self.secure_socket = self.context.wrap_socket(self.socket, server_side=False,
                                                          server_hostname=SERVER_HOSTNAME)
            logger.debug("Switching to encrypted communication.")

        self.connected = True
        return self

    def get_socket(self):
        return self.secure_socket if TLS else self.socket

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client.token:
            self.client.logout()

        if TLS:
            self.secure_socket.close()
        self.socket.close()
        logger.debug("Sockets closed.")

    def send(self, message: Message):
        sock = self.get_socket()
        return sock.sendall(message.convert_message_to_bytes())

    def receive(self):
        sock = self.get_socket()
        m = Message()
        headers = Receiver.receive_headers(sock)
        m.set_header_bytes(headers)
        content_length = m.get_header_param(MESSAGE_CONTENT_LENGTH)
        body = Receiver.receive_body(sock, content_length)
        m.set_body_bytes(body)
        return m
