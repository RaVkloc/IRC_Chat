from xcomm.message import Message
from xcomm.settings import ERROR_KEY


class MessageHandler:
    def __init__(self, m: Message):
        self.message = m

    def check_error(self):
        try:
            self.message.get_body_param(ERROR_KEY)
            return False
        except KeyError:
            return True

    def client_message(self):
        if not self.check_error():
            errors = self.message.get_body_param(ERROR_KEY)
            return errors.values()
        else:
            return self.message.body


class LoginHandler:
    pass