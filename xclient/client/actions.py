from xclient.client.exceptions import InvalidStatusCode
from xclient.client.settings import STATUS_KEY, SUCCESS_RESPONSES, RESPONSE_ACTION_HEADER, CLIENT_SEND_ACTIONS, \
    RESPONSE_TOKEN_KEY
from xcomm.message import Message


class Response:
    """
    Message wrapper.
    """

    def __init__(self, message: Message):
        self.message = message

    def is_login_reponse(self):
        return self.message.get_header_param(RESPONSE_ACTION_HEADER) == str(CLIENT_SEND_ACTIONS['login'])

    def get_token(self):
        """
        Method return token or not, if there is not in response
        :return:
        """
        if not self.is_login_reponse():
            return None
        try:
            token = self.message.get_body_param(RESPONSE_TOKEN_KEY)
        except KeyError:
            token = None
        return token

    def is_valid_response(self):
        try:
            self.message.get_body_param(STATUS_KEY)
            return True
        except KeyError:
            raise InvalidStatusCode()

    def is_success(self):
        """
        :return: True if response message has success status
        :rtype: bool
        """
        return self.message.get_body_param(STATUS_KEY) in SUCCESS_RESPONSES

    def error_message(self):
        """
        :return: Error description
        :rtype: str
        """
        if not self.is_success():
            return self.message.get_body_param(STATUS_KEY)

    def parse_response(self):
        self.is_valid_response()
        if self.is_success():
            return self.message.body
        return self.error_message()
