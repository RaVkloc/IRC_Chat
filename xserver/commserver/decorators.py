from xcomm.message import Message
from xserver.commserver.databaseconnection import DatabaseConnection
from xserver.commserver.settings import TOKEN_KEY, AUTHENTICATION_ERROR


def login_required(f):
    def inner(self):
        token = self.msg.get_header_param(TOKEN_KEY)
        if not token:
            self.set_error_with_status(AUTHENTICATION_ERROR)
            return
        query = 'SELECT username from users_user where token="{}"'.format(token)
        db_connect = DatabaseConnection()
        db_connect.cursor.cursor.execute(query)
        user = db_connect.cursor.cursor.fetchone()
        if not user:
            self.set_error_with_status(AUTHENTICATION_ERROR)
            return
        self.user = user[0]
        return f()
    return inner
