import hashlib
import logging
from collections import namedtuple
from uuid import uuid4

from xserver.actionsserver.action_base import ActionBase
from xcomm.xcomm_moduledefs import *
from xserver.actionsserver.exceptions import InvalidLoginData, InvalidTokenSave

logger = logging.getLogger("LoginAction")


class LoginAction(ActionBase):

    def __init__(self, message):
        super().__init__(message)

    def get_action_number(self):
        return MESSAGE_ACTION_LOGIN_CODE

    def execute(self, client=None, server=None):
        logger.debug("Starting executing LOGIN action.")
        login = self.msg.get_body_param(MESSAGE_ACTION_LOGIN_LOGIN)
        passwd = self.msg.get_body_param(MESSAGE_ACTION_LOGIN_PASSWORD)

        # Get hash of password to compare it with DataBase
        passwd = self._get_user_password_hash(passwd)
        with self.db_connect as cursor:

            try:
                result = self._get_user_data_from_db(login, cursor)
            except InvalidLoginData as e:
                self.set_error_with_status(e.message)
                logger.error(e.message)
                return

            # empty means no such a user in DB
            # hashes are not equals means incorrect password
            if not result or result.password != passwd:
                # send the same info in two cases so as no to say if such a user exists
                self.set_error_with_status("Invalid username or password.")
                logger.error("No user found or password does not match its hash.")
                return

            token = str(uuid4())
            logger.debug("Generated token: " + token)
            self.clear_room(result.id, self.db_connect)
            try:
                self._add_user_token_to_db(result.username, token, cursor)
            except InvalidTokenSave as e:
                self.set_error_with_status(e.message)
                logger.error(e.message)
                return

        self.result.add_body_param(MESSAGE_TOKEN, token)
        client.user = result.id
        self.set_status_ok()
        logger.debug("Action LOGIN executed SUCCESSFULLY.")

    def _get_user_password_hash(self, password):
        hash_alg = hashlib.sha3_256()
        hash_alg.update(password.encode())
        return hash_alg.hexdigest()

    def _get_user_data_from_db(self, login, cursor):
        query = "SELECT id, username, password FROM users_user WHERE username = '{}'"

        logger.debug("Executing query: " + query + "\n\twith params: " + str((login,)))

        # return None if user not found
        cursor.execute(query.format(login))
        result = cursor.fetchone()
        if not result:
            raise InvalidLoginData()
        Credential = namedtuple('Credential', 'id username password')
        result = Credential(id=result[0], username=result[1], password=result[2])
        logger.debug("Query result: " + str(result))
        return result

    def _add_user_token_to_db(self, username, user_token, cursor):
        query = "UPDATE users_user SET token = '{}' WHERE username = '{}'"

        logger.debug("Executing query: " + query + "\n\twith params: " + str((username, user_token)))

        cursor.execute(query.format(user_token, username))
        self.db_connect.connection.commit()
        logger.debug("Query executed successfully.")

    def clear_room(self, user_id, conn):
        cursor = conn.cursor
        query = "UPDATE users_user SET room_id_id = null WHERE id = {}"
        cursor.execute(query.format(user_id))
        conn.connection.commit()
