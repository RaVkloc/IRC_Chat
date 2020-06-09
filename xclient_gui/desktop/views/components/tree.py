from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5 import QtCore

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME


class Tree(QTreeWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client

        self.setHeaderLabel("Rooms")

        self.itemDoubleClicked.connect(self.on_item_clicked)
        self.get_room_list()
        self.show()

    def get_room_list(self):
        self.client.list_rooms()

    def refresh_room_list(self):
        self.get_room_list()

    def clear_selection(self):
        self.clearFocus()
        self.clearSelection()

    def set_room_list(self, rooms):
        list_rooms = rooms.split(',')
        self.clear()

        for i in list_rooms:
            item = QTreeWidgetItem([i])
            # item.setBackground(QColor(255, 0, 0, 127))

            self.addTopLevelItem(item)

    @QtCore.pyqtSlot(QTreeWidgetItem, int)
    def on_item_clicked(self, it, col):
        body = {
            MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME: it.text(col)
        }
        self.client.join_room(body=body)
