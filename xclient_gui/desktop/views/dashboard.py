from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter, QMainWindow

from xclient_gui.desktop.views.components.chat import Chat
from xclient_gui.desktop.views.components.tree import Tree


class CentralWidget(QSplitter):
    def __init__(self):
        super().__init__()
        tree = Tree()
        chat = Chat()

        self.addWidget(tree)
        self.addWidget(chat)
        self.setSizes([50, 200])
        self.setOrientation(QtCore.Qt.Horizontal)


class Dashboard(QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.set_widget_default_values()

        self.setCentralWidget(CentralWidget())

    def set_widget_default_values(self):
        self.setWindowTitle('Login Form')
        self.resize(500, 500)
