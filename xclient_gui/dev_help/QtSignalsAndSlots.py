from PyQt5.QtCore import QObject, pyqtSignal


class Dowolna(QObject):
    trigger = pyqtSignal()


ob = Dowolna()

class Foo(QObject):
    def connect_and_emit_trigger(self):
        # ob = Dowolna()
        print('connect')
        print(id(ob.trigger))
        ob.trigger.connect(self.handle_trigger)
        print(id(ob.trigger))

    def handle_trigger(self):
        print("trigger signal received")


class Foo2(QObject):
    def con(self):
        # ob = Dowolna()
        print('emit')
        print(id(ob.trigger))
        ob.trigger.emit()
        print(id(ob.trigger))


foo2 = Foo2()
foo2.con()

foo = Foo()
foo.connect_and_emit_trigger()


