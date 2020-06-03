import socket


class Connection:
    def __init__(self, ip, port, max_connection=10):
        self.ip = ip
        self.port = port
        self.max_connection = max_connection
        self.socket = socket.socket()

    def __enter__(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(self.max_connection)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()
