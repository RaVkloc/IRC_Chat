from PyQt5.QtCore import QObject, pyqtSignal


class Signal(QObject):
    signal = pyqtSignal(object)


class MediatorMeta(type):
    _instance = None

    def __call__(cls):
        if cls._instance is None:
            cls._instance = Signal()
        return cls._instance


class Mediator(metaclass=MediatorMeta):
    def __init__(self):
        self.signal = None
