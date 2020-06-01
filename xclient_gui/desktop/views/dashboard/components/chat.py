from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QMessageBox, QListView, QVBoxLayout, QCheckBox, QWidget, QLabel, QLineEdit, \
    QFrame, QSplitter

from xclient_gui.desktop.views.dashboard.components.tree import Tree


class Chat(QWidget):
    def __init__(self):
        super().__init__()

        # self.addItem(QLayoutItem())
        # self.addItem("Item 2")
        # self.addItem("Item 3")
        # self.addItem("Item 4")
        # self.addItem("Item 5")
        # self.setView(QListView())
        # box = QVBoxLayout

        #

        hbox = QVBoxLayout()

        tree = Tree()
        tree.setFrameShape(QFrame.StyledPanel)
        tree.setStyleSheet('background-color:white')

        tree2 = Tree()
        tree2.setFrameShape(QFrame.StyledPanel)
        tree2.setStyleSheet('background-color:red')

        # chat = Chat()
        # chat.setStyleSheet('background-color:green')

        # splitter = QSplitter(Qt.Vertival)
        # splitter.addWidget(tree)
        # splitter.addWidget(tree2)

        # splitter.setSizes([50, 200])

        # hbox.direction = QVBoxLayout.BottomToTop

        hbox.addWidget(tree)
        hbox.addWidget(tree2)

        self.setLayout(hbox)
        self.show()

    # def Clicked(self, item):
    #     QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())
