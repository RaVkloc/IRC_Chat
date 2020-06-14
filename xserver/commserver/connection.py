import socket
import ssl

from xserver.coreserver.coreserver_moduledefs import TLS, SERVER_CERT, SERVER_KEY


class Connection:
    def __init__(self, ip, port, max_connection=10):
        self.ip = ip
        self.port = port
        self.max_connection = max_connection
        if TLS:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            self.context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)

    def __enter__(self):
        addr = ("", self.port)
        if socket.has_dualstack_ipv6():
            self.socket = socket.create_server(addr, family=socket.AF_INET6, backlog=self.max_connection,
                                               reuse_port=True, dualstack_ipv6=True)
        else:
            self.socket = socket.create_server(addr)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

