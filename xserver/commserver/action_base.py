from abc import abstractmethod


class ActionBase:
    errors = {}

    def __init__(self):
        self.result = None
        self.error = False

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
