from PyQt5.QtWidgets import QMainWindow, QMessageBox

from xclient_gui.desktop.utils.messages import CLOSE, CLOSE_WINDOW_ARE_YOU_SURE


class MainWindow(QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def closeEvent(self, event):
        self.show_prevent_closing_box(event)

    def show_prevent_closing_box(self, event):
        msg = QMessageBox()
        msg.setWindowTitle(CLOSE)
        msg.setText(CLOSE_WINDOW_ARE_YOU_SURE)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = msg.exec_()
        if result == QMessageBox.Ok:
            self.client.logout()
        else:
            event.ignore()
