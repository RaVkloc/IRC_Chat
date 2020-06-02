import hashlib
from uuid import uuid4

from xserver.commserver.databaseconnection import DatabaseConnection
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
        passwd = self.__get_user_password_hash(passwd)

        try:
            result = self.__get_user_data_from_db(login)
        except:
            self.set_error_with_status("Unable to read user's data. Try again later.")
            return

        # empty means no such a user in DB
        # hashes are not equals means incorrect password
        if not result or result[1] != passwd:
            # send the same info in two cases so as no to say if such a user exists
            self.set_error_with_status("Invalid username or password.")
            return

        token = str(uuid4())
        try:
            self.__add_user_token_to_db(result[0], token)
        except:
            self.set_error_with_status("Unable to update user's token. Try again later.")
            return

        self.result.add_body_param(MESSAGE_ACTIONLOGIN_Token, token)
        self.set_status_ok()

    def __get_user_password_hash(self, password):
        hash_alg = hashlib.sha3_256()
        hash_alg.update(password.encode())
        return hash_alg.hexdigest()

    def __get_user_data_from_db(self, login):
        db_conn = DatabaseConnection()
        query = "SELECT `username`, `password` FROM `users_user` WHERE `username` = %s"

        # return None if user not found
        db_conn.cursor.cursor.execute(query, (login,))
        return db_conn.cursor.cursor.fetchone()

    def __add_user_token_to_db(self, username, user_token):
        db_conn = DatabaseConnection()
        sql_query_add_token = "UPDATE users_user SET token = '{}' WHERE username = '{}'"

        db_conn.cursor.cursor.execute(sql_query_add_token.format(user_token, username))
        db_conn.cursor.connection.commit()
