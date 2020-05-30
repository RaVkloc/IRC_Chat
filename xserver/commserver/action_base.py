from abc import abstractmethod


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

    @abstractmethod
    def get_action_result(self):
        pass

    @abstractmethod
    def get_error(self):
        pass
