from abc import abstractmethod

from xcomm.message import Message

from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_STATUS, MESSAGE_STATUS_OK


class ActionBase:
    errors = {}

    def __init__(self, message):
        self.result = Message()
        self.error = False
        self.msg = message

        self.set_basic_params()

    def set_basic_params(self):
        self.result.add_header_param(MESSAGE_ACTION, self.get_action_number())

    @abstractmethod
    def get_action_number(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    def set_error_with_status(self, status):
        self.error = True
        self.result.add_body_param(MESSAGE_STATUS, status)

    def set_status_ok(self):
        self.result.add_body_param(MESSAGE_STATUS, MESSAGE_STATUS_OK)

    def get_action_result(self):
        return self.result

    def get_error(self):
        return self.error
