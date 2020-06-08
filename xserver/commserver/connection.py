import socket


class Connection:
    def __init__(self, ip, port, max_connection=10):
        self.ip = ip
        self.port = port
        self.max_connection = max_connection

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
