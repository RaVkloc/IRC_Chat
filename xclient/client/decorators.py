import threading
from xclient.client.utils import Sender


def request_action():
    def inner(f):
        def func(*args, **kwargs):
            Sender.send_message(f, *args, kwargs)

        return func

    return inner
