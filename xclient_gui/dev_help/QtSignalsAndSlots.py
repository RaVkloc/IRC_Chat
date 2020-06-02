from PyQt5.QtCore import QObject, pyqtSignal


class Dowolna(QObject):
    trigger = pyqtSignal()


class Foo(QObject):
    # Define a new signal called 'trigger' that has no arguments.
    # trigger = Dowolna

    def connect_and_emit_trigger(self):
        # Connect the trigger signal to a slot.
        ob = Dowolna()
        ob.trigger.connect(self.handle_trigger)

        # Emit the signal.
        ob.trigger.emit()

    def handle_trigger(self):
        # Show that the slot has been called.

        print("trigger signal received")


foo = Foo()
foo.connect_and_emit_trigger()
