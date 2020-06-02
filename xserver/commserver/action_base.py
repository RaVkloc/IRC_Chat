from abc import abstractmethod

from xcomm.xcomm_moduledefs import MESSAGE_STATUS

class ActionBase:
    errors = {}

    def __init__(self, message):
        self.result = None
        self.error = False
        self.msg = message

    @abstractmethod
    def get_action_number(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    def set_error_with_status(self, status):
        self.error = True
        self.result.add_body_param(MESSAGE_STATUS, status)

    def get_action_result(self):
        return self.result

    def get_error(self):
        return self.error
