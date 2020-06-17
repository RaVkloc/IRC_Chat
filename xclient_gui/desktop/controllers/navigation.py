from xclient_gui.desktop.views.connection_fail import ConnectionFail
from xclient_gui.desktop.views.login import LoginForm
from xclient_gui.desktop.views.register import RegisterForm
from xclient_gui.desktop.views.dashboard import Dashboard


class ScreenController:
    def __init__(self, client):
        self.client = client
        self.screen = None

    def close_screen(self):
        if self.screen is not None:
            self.screen.close()

    def set_screen(self, new_screen):
        self.close_screen()
        self.screen = new_screen
        self.screen.show()

    def show_login(self):
        login = LoginForm(self.client)
        login.open_next_screen.connect(self.show_dashboard)
        login.open_registration.connect(self.show_register)
        self.set_screen(login)

    def show_dashboard(self):
        dashboard = Dashboard(self.client)
        dashboard.on_logout.connect(self.show_login)
        self.set_screen(dashboard)

    def show_register(self):
        register = RegisterForm(self.client)
        register.open_next_screen.connect(self.show_login)
        self.set_screen(register)

    def show_connection_fail(self):
        connection_fail = ConnectionFail()
        self.set_screen(connection_fail)
