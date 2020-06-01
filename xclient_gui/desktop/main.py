from PyQt5.QtWidgets import (QApplication, QMainWindow, QGridLayout)
import sys
from xclient_gui.desktop.views.dashboard.dashboard import Dashboard
from xclient_gui.desktop.views.login import LoginForm
from xclient_gui.desktop.controllers.navigation import ScreenController


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setCentralWidget(LoginForm())
    window.show()
    # window.setLayout(layout)

    # controller = ScreenController()
    # controller.show_login()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
