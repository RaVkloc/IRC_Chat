import sys

from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtWidgets import QMainWindow, QApplication

from xclient_gui.qtclient.login import LoginWindow


class GUIMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IRC Chat")
        self.__show_login_dialog()

    def __show_login_dialog(self):
        login_dialog = LoginWindow(self)
        login_dialog.login_user.connect(self.__login_required)
        login_dialog.exec()

    def __login_required(self, username, password):
        print(username, password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = GUIMainWindow()
    a.show()
    app.exec_()
