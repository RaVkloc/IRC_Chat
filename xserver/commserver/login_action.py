import hashlib
from uuid import uuid4

from xserver.commserver.databaseconnection import DatabaseConnection
from xserver.commserver.action_base import ActionBase
from xcomm.xcomm_moduledefs import *
from xserver.commserver.exceptions import InvalidLoginData, InvalidTokenSave


class LoginAction(ActionBase):

    def __init__(self, message):
        super().__init__(message)

    def get_action_number(self):
        return MESSAGE_ACTION_LOGIN_CODE

    def execute(self):
        login = self.msg.get_body_param(MESSAGE_ACTION_LOGIN_LOGIN)
        passwd = self.msg.get_body_param(MESSAGE_ACTION_LOGIN_PASSWORD)

        # Get hash of password to compare it with DataBase
        passwd = self._get_user_password_hash(passwd)
        with self.db_connect as cursor:

            try:
                result = self._get_user_data_from_db(login, cursor)
            except InvalidLoginData as e:
                self.set_error_with_status(e.message)
                return

            # empty means no such a user in DB
            # hashes are not equals means incorrect password
            if not result or result[1] != passwd:
                # send the same info in two cases so as no to say if such a user exists
                self.set_error_with_status("Invalid username or password.")
                return

            token = str(uuid4())
            try:
                self._add_user_token_to_db(result[0], token)
            except InvalidTokenSave as e:
                self.set_error_with_status(e.message)
                return

        self.result.add_body_param(MESSAGE_ACTION_LOGIN_TOKEN, token)
        self.set_status_ok()

    def _get_user_password_hash(self, password):
        hash_alg = hashlib.sha3_256()
        hash_alg.update(password.encode())
        return hash_alg.hexdigest()

    def _get_user_data_from_db(self, login, cursor):
        query = "SELECT `username`, `password` FROM `users_user` WHERE `username` = %s"

        # return None if user not found
        cursor.execute(query, (login,))
        return cursor.fetchone()

    def _add_user_token_to_db(self, username, user_token,cursor):
        sql_query_add_token = "UPDATE users_user SET token = '{}' WHERE username = '{}'"

        cursor.execute(sql_query_add_token.format(user_token, username))
        cursor.connection.commit()
