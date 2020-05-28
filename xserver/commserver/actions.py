import hashlib
from abc import abstractmethod
from uuid import uuid4

from xcomm.message import Message
from xserver.commserver import databaseconnection as dbconn

from xcomm.xcomm_moduledefs import *


class ActionBase:
    errors = {}

    def __init__(self):
        self.result = None
        self.error = False

    @abstractmethod
    def get_action_number(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_action_result(self):
        pass

    @abstractmethod
    def get_error(self):
        pass


class LoginAction(ActionBase):

    def __init__(self, message):
        super().__init__()
        self.msg = message

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
        db_connection = dbconn.DatabaseConnection().cursor

        sql_query = "SELECT password FROM users_user WHERE username='{}'"
        db_connection.cursor.execute(sql_query.format(login))
        result = db_connection.cursor.fetchall()

        # empty means no such a user in DB
        # if hashes are not equals incorrect password was sent
        if len(result) == 0 or result[2] != passwd:
            self.error = True
            self.result = Message()
            self.result.add_header_param(MESSAGE_ACTION, MESSAGE_ACTIONLOGIN_Code)
            self.result.add_body_param(MESSAGE_CODE_INFORMATION, "Invalid username or password.")
            return

        self.result = Message()
        self.result.add_header_param(MESSAGE_ACTION, MESSAGE_ACTIONLOGIN_Code)
        self.result.add_body_param(MESSAGE_CODE_INFORMATION, "OK")
        token = str(uuid4())

        # Add user's token to database
        sql_query_add_token = "INSERT INTO users_token(token, user_id) VALUES ({}, {})"
        db_connection = dbconn.DatabaseConnection()
        db_connection.cursor.execute(sql_query_add_token.format(token, result[0]))
        db_connection.cursor.connection.commit()
        self.result.add_body_param(MESSAGE_ACTIONLOGIN_Token, token)

    def get_error(self):
        return self.error

    def get_action_result(self):
        return self.result
