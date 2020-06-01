from xclient.client.client import TerminalClient
from xserver.coreserver.coreserver_moduledefs import SERVER_ADDRESS, SERVER_PORT

if __name__ == '__main__':
    client = TerminalClient(SERVER_ADDRESS,SERVER_PORT)
    client.start()
