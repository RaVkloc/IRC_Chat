import logging
import threading

from xcomm.message import Message
from xcomm.settings import DELIMITER_BYTE
from xcomm.xcomm_moduledefs import MESSAGE_CONTENT_LENGTH
from xserver.commserver.commserver_moduledefs import RECEIVE_BYTES_LIMIT
from xserver.commserver.action_provider import ActionProvider


class Client:
    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address
        self.message = None
        self.logger = logging.getLogger("Client")
        recv_thread = threading.Thread(target=self.always_listen, daemon=True)
        recv_thread.start()

    def always_listen(self):
        while True:
            self.message = Message()
            msg = b""
            while DELIMITER_BYTE * 2 not in msg:
                msg += self.client_socket.recv(RECEIVE_BYTES_LIMIT)

            self.message.set_header_bytes(msg)
            content_length = int(self.message.get_header_param(MESSAGE_CONTENT_LENGTH))

            msg = b""
            while len(msg) < content_length:
                msg += self.client_socket.recv(RECEIVE_BYTES_LIMIT)

            self.message.set_body_bytes(msg)
            self.logger.debug(f"({self.client_address}) -> " + self.message.get_complete_message().replace("\0", "\n"))

            # Serve message
            action = ActionProvider.get_action_for(self.message)

            if action is not None:
                action.execute()

                response = action.get_action_result()
                self.client_socket.sendall(response.convert_message_to_bytes())
                self.logger.debug(f"({self.client_address}) <- " + response.get_complete_message().replace("\0", "\n"))
