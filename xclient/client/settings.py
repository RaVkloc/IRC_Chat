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
    'list_room': 5,
    'leave_room': 6,
    'list_user': 7,
    'send_message': 8,
    'logout': 9,
}

RECEIVE_MESSAGE_CODE = 10

TOKEN_KEY = 'Token'
STATUS_KEY = 'Status'

RESPONSE_ACTION_HEADER = 'Action'
RESPONSE_TOKEN_KEY = 'Token'

SUCCESS_RESPONSES = ['ok', ]
