from xclient.client.client import TerminalClient

if __name__ == '__main__':
    client = TerminalClient('127.0.0.1',1999)
    client.start()