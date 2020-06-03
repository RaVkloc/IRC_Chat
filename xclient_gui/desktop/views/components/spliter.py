from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QLineEdit, QHBoxLayout, QSplitter
import sys
from PyQt5.QtCore import Qt
from xclient_gui.desktop.views.dashboard.components.tree import Tree
from xclient_gui.desktop.views.dashboard.components.chat import Chat
import time


class Splitter(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Splitter"
        # self.top = 0
        # self.left = 0
        # self.width = 1000
        # self.height = 1000
        hbox = QHBoxLayout()

        tree = Tree()
        tree.setFrameShape(QFrame.StyledPanel)
        tree.setStyleSheet('background-color:white')

        chat = Chat()
        chat.setStyleSheet('background-color:green')

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(tree)
        splitter.addWidget(chat)

        splitter.setSizes([50, 200])

        hbox.addWidget(splitter)
        self.setLayout(hbox)
        self.show()
