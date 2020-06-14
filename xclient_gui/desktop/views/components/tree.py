from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
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
            self.addTopLevelItem(item)

    @QtCore.pyqtSlot(QTreeWidgetItem, int)
    def on_item_clicked(self, it, col):
        body = {
            MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME: it.text(col)
        }
        self.client.join_room(body=body)

        iterator = QTreeWidgetItemIterator(self)
        transparent_brush = QBrush(QColor(255, 255, 255, 0))
        while iterator.value():
            item = iterator.value()
            item.setBackground(col, transparent_brush)
            iterator += 1

        brush = QBrush(QColor(255, 127, 25))
        it.setBackground(col, brush)
