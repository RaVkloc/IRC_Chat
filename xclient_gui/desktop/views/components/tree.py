from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5 import QtCore


class Tree(QTreeWidget):
    def __init__(self, client):
        super().__init__()
        self.setHeaderLabel("Rooms")
        for i in range(3):
            # parent = QtWidgets.QTreeWidgetItem(self)
            # parent.setText(0, "Parent {}".format(i))
            # parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

            parent_it = QTreeWidgetItem(["Pokój {}".format(i)])
            self.addTopLevelItem(parent_it)
        self.itemDoubleClicked.connect(self.on_item_clicked)
        self.show()

    @QtCore.pyqtSlot(QTreeWidgetItem, int)
    def on_item_clicked(self, it, col):
        print(it, col, it.text(col))
