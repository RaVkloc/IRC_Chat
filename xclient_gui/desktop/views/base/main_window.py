from PyQt5.QtWidgets import QMainWindow, QMessageBox

from xclient_gui.desktop.utils.messages import CLOSE, CLOSE_WINDOW_ARE_YOU_SURE


class MainWindow(QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def closeEvent(self, event):
        self.show_prevent_closing_box(event)

    def show_prevent_closing_box(self, event):
        if self.client.token is not None:
            result = QMessageBox.question(self,  # parent
                                          CLOSE,  # window title
                                          CLOSE_WINDOW_ARE_YOU_SURE,  # question
                                          QMessageBox.No | QMessageBox.Yes)  # buttons

            if result == QMessageBox.Yes:
                self.client.logout()
            else:
                event.ignore()
