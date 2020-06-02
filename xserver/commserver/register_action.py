import hashlib

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_REGISTER_CODE, MESSAGE_ACTION_REGISTER_LOGIN, \
    MESSAGE_ACTION_REGISTER_PASSWORD

from xserver.commserver.databaseconnection import DatabaseConnection
from xserver.commserver.action_base import ActionBase


class RegisterAction(ActionBase):

    def __init__(self, message):
        super().__init__(message)

    def get_action_number(self):
        return MESSAGE_ACTION_REGISTER_CODE

    def execute(self):
        username = self.msg.get_body_param(MESSAGE_ACTION_REGISTER_LOGIN)
        password = self.msg.get_body_param(MESSAGE_ACTION_REGISTER_PASSWORD)

        # Check if user with such nick does not already exists
        try:
            if not self.__is_username_unique(username):
                self.set_error_with_status("Given username is already taken. Please try another one.")
                return
        except:
            self.set_error_with_status("Unable to check username's uniqueness. Try again later.")

        if not self.__validate_password(password):
            self.set_error_with_status("To weak password. Minimum length = 6.")
            return

        try:
            self.__insert_new_user_to_db(username, password)
        except:
            self.set_error_with_status("Unable to save new user. Try again later.")

        self.set_status_ok()

    def __is_username_unique(self, username):
        db_conn = DatabaseConnection()
        query = f"SELECT * FROM users_user WHERE username='{username}'"

        db_conn.cursor.cursor.execute(query)
        return db_conn.cursor.cursor.fetchone() is None

    def __validate_password(self, passwd):
        if len(passwd) > 5:
            return True
        else:
            return False

    def __get_user_password_hash(self, password):
        hash_alg = hashlib.sha3_256()
        hash_alg.update(password.encode())
        return hash_alg.hexdigest()

    def __insert_new_user_to_db(self, username, password):
        db_conn = DatabaseConnection()
        query = "INSERT INTO users_user (username, password) VALUES ('{}', '{}')"

        hash_pass = self.__get_user_password_hash(password)

        db_conn.cursor.cursor.execute(query.format(username, hash_pass))
        db_conn.cursor.connection.commit()
