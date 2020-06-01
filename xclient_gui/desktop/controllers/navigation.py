from xclient_gui.desktop.views.login import LoginForm
from xclient_gui.desktop.views.dashboard.dashboard import Dashboard


class ScreenController:
    def __init__(self):
        self.login = None
        self.dashboard = None

    def show_login(self):
        self.login = LoginForm()
        self.login.switch_window.connect(self.show_dashboard)
        self.login.show()

    def show_dashboard(self):
        self.dashboard = Dashboard()
        self.dashboard.switch_window.connect(self.show_window_two)
        self.login.close()
        self.dashboard.show()

    def show_window_two(self, text):
        # self.window_two = WindowTwo(text)
        # self.window.close()
        # self.window_two.show()
        pass
