import hashlib
from uuid import uuid4

from xcomm.message import Message
from xserver.commserver import databaseconnection as dbconn
from xserver.commserver.action_base import ActionBase
from xcomm.xcomm_moduledefs import *


class LoginAction(ActionBase):

    def __init__(self, message):
        super().__init__(message)

    def get_action_number(self):
        return MESSAGE_ACTIONLOGIN_Code

    def execute(self):
        login = self.msg.get_body_param(MESSAGE_ACTIONLOGIN_Login)
        passwd = self.msg.get_body_param(MESSAGE_ACTIONLOGIN_Password)

        # Get hash of password to compare it with DataBase
        hash = hashlib.sha3_256()
        hash.update(passwd.encode())
        passwd = hash.hexdigest()

        # TODO: Add testing if connection is stable
        db_connection = dbconn.DatabaseConnection()

        sql_query = "SELECT username, password FROM users_user WHERE username='{}'"
        db_connection.cursor.cursor.execute(sql_query.format(login))
        result = db_connection.cursor.cursor.fetchall()

        # empty means no such a user in DB
        # if hashes are not equals incorrect password was sent
        if len(result) == 0 or result[0][1] != passwd:
            self.error = True
            self.result = Message()
            self.result.add_header_param(MESSAGE_ACTION, MESSAGE_ACTIONLOGIN_Code)
            self.result.add_body_param(MESSAGE_STATUS, "Invalid username or password.")
            return

        self.result = Message()
        self.result.add_header_param(MESSAGE_ACTION, MESSAGE_ACTIONLOGIN_Code)
        self.result.add_body_param(MESSAGE_STATUS, MESSAGE_STATUS_OK)
        token = str(uuid4())

        # Add user's token to database
        sql_query_add_token = "UPDATE users_user SET token = '{}' WHERE username = '{}'"
        db_connection = dbconn.DatabaseConnection()
        db_connection.cursor.cursor.execute(sql_query_add_token.format(token, result[0][0]))
        db_connection.cursor.connection.commit()
        self.result.add_body_param(MESSAGE_ACTIONLOGIN_Token, token)

    def get_error(self):
        return self.error

    def get_action_result(self):
        return self.result
