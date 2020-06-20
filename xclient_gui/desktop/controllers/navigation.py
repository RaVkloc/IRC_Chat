from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QGuiApplication

from xclient_gui.desktop.utils.messages import LOADING, CONNECTION_FAILED, REGISTER, LOGIN, APP_TITLE
from xclient_gui.desktop.views.base.main_window import MainWindow
from xclient_gui.desktop.views.connection_fail import ConnectionFail
from xclient_gui.desktop.views.login import LoginForm
from xclient_gui.desktop.views.register import RegisterForm
from xclient_gui.desktop.views.dashboard import Dashboard


class ScreenController:
    def __init__(self, client):
        self.client = client
        self.screen = MainWindow(client)

    def start(self):
        while self.client.connection.connected is None:
            pass
        print(self.client.connection.connected)
        if self.client.connection.connected:
            self.show_login()
        else:
            self.show_connection_fail()

    def resize_window(self, width, height):
        available_size = QGuiApplication.primaryScreen().availableSize()
        self.screen.resize(available_size.width() * width, available_size.height() * height)

    def close_screen(self):
        self.screen.setCentralWidget(None)

    def set_screen(self, new_screen, title=APP_TITLE, width=0.3, height=0.3):
        self.screen.setCentralWidget(new_screen)
        self.screen.setWindowTitle(title)
        self.resize_window(width, height)
        self.screen.show()

    def show_login(self):
        login = LoginForm(self.client)
        login.open_next_screen.connect(self.show_dashboard)
        login.open_registration.connect(self.show_register)
        self.set_screen(login, LOGIN, 0.4, 0.1)

    def show_dashboard(self):
        dashboard = Dashboard(self.client)
        dashboard.on_logout.connect(self.show_login)
        self.set_screen(dashboard, APP_TITLE, 0.3, 0.3)

    def show_register(self):
        register = RegisterForm(self.client)
        register.open_next_screen.connect(self.show_login)
        self.set_screen(register, REGISTER, 0.4, 0.1)

    def show_connection_fail(self):
        connection_fail = ConnectionFail()
        self.set_screen(connection_fail, CONNECTION_FAILED, 0.25, 0.1)
