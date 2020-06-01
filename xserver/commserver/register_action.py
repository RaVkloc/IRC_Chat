import hashlib

from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_STATUS, MESSAGE_STATUS_OK
from xcomm.xcomm_moduledefs import MESSAGE_ACTIONREGISTER_Code, MESSAGE_ACTIONREGISTER_Login, \
    MESSAGE_ACTIONREGISTER_Password

from xcomm.message import Message
from xserver.commserver.databaseconnection import DatabaseConnection
from xserver.commserver.action_base import ActionBase


class RegisterAction(ActionBase):

    def __init__(self, message):
        super().__init__(message)

    def get_action_number(self):
        return MESSAGE_ACTIONREGISTER_Code

    def execute(self):
        username = self.msg.get_body_param(MESSAGE_ACTIONREGISTER_Login)
        password = self.msg.get_body_param(MESSAGE_ACTIONREGISTER_Password)
        db_connect = DatabaseConnection()

        self.result = Message()
        self.result.add_header_param(MESSAGE_ACTION, MESSAGE_ACTIONREGISTER_Code)

        # Check if user with such nick does not already exists
        query = f"SELECT * FROM users_user WHERE username='{username}'"
        db_connect.cursor.cursor.execute(query)
        if len(db_connect.cursor.cursor.fetchall()) != 0:
            self.error = True
            self.result.add_body_param(MESSAGE_STATUS, "Given username is already taken. Please try another one.")
            return

        if not self.__validate_password(password):
            self.error = True
            self.result.add_body_param(MESSAGE_STATUS, "To weak password, minimum length = 6.")
            return

        query = "INSERT INTO users_user (username, password) VALUES ('{}', '{}')"
        hash_sha = hashlib.sha3_256()
        hash_sha.update(password.encode())
        db_connect.cursor.cursor.execute(query.format(username,
                                                      hash_sha.hexdigest()))
        db_connect.cursor.connection.commit()
        self.result.add_body_param(MESSAGE_STATUS, MESSAGE_STATUS_OK)

    def __validate_password(self, passwd):
        if len(passwd) > 5:
            return True
        else:
            return False
