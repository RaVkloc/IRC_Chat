import os


def find_unique_filename():
    num = 1
    while os.path.isfile(CLIENT_LOG_FILENAME.format(num)):
        num += 1
    return CLIENT_LOG_FILENAME.format(num)


BASE_HEADERS = {
    'ConLen': '',
    'Token': '',
    'Action': '',
}

CLIENT_SEND_ACTIONS = {
    'login': 1,
    'register': 2,
    'create_room': 3,
    'join_room': 4,
    'list_rooms': 5,
    'leave_room': 6,
    'list_user': 7,
    'send_message': 8,
    'logout': 9,
}

CLIENT_LOG_FILENAME = "../../logs/client.log{}"
CLIENT_LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s]: %(message)s"
CLIENT_LOG_DATEFORMAT = "%H:%M:%S %m/%d/%Y"

CLIENT_LOG_CONFIG = {"filename": find_unique_filename(),
                     "filemode": "w+",
                     "format": CLIENT_LOG_FORMAT,
                     "datefmt": CLIENT_LOG_DATEFORMAT,
                     "level": "DEBUG"
                     }

RECEIVE_MESSAGE_CODE = 10

TOKEN_KEY = 'Token'
STATUS_KEY = 'Status'

RESPONSE_ACTION_HEADER = 'Action'
RESPONSE_TOKEN_KEY = 'Token'

SUCCESS_RESPONSES = ['ok', ]
TLS = True
ROOT_PATH = os.path.dirname(__file__)
CERT_PATH = os.path.join(ROOT_PATH, 'client.crt')
KEY_PATH = os.path.join(ROOT_PATH, 'client.key')
SERVER_CERT = os.path.abspath('../../xserver/coreserver/server.cert')
