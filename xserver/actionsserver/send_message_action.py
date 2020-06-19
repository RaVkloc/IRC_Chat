import logging
import datetime
import threading

from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required
from xserver.actionsserver.exceptions import NoActiveRoomException

from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_ACTION_SENDMESSAGE_CODE, MESSAGE_ACTION_RECVMESSAGE_CODE, \
    MESSAGE_ACTION_RECVMESSAGE_TIMESTAMP, MESSAGE_ACTION_RECVMESSAGE_USER

logger = logging.getLogger("SendMessageAction")


class SendMessageAction(ActionBase):
    def get_action_number(self):
        return MESSAGE_ACTION_SENDMESSAGE_CODE

    @login_required
    def execute(self, server=None):
        logger.debug("(userID={})Executing SEND_MESSAGE action started.".format(self.user))
        with self.db_connect as cursor:
            try:
                room = self._get_room_by_user(self.user, cursor)
                users = self._get_list_users_in_room(room, cursor)
                current_username = self._get_username_by_id(cursor)
                with threading.Lock():
                    clients = self.get_client_list(users, server)
                    self.send_message(clients, current_username)
            except NoActiveRoomException as e:
                self.set_error_with_status(e.message)
                return

            self.set_status_ok()
            logger.debug("(userID={})Executing SEND_MESSAGE action SUCCESSFULLY finished.".format(self.user))

    def _get_room_by_user(self, user_id, cursor):
        query = 'SELECT room_id_id FROM users_user WHERE id ={}'

        logger.debug("(userID={})Executing query: ".format(self.user) + query + "\n\twith params: " + str((user_id,)))

        cursor.execute(query.format(user_id))
        result = cursor.fetchone()
        logger.debug("(userID={})Query result: ".format(self.user) + str(result))

        if not result:
            raise NoActiveRoomException()
        return result[0]

    def _get_list_users_in_room(self, room_id, cursor):
        query = 'SELECT id FROM users_user WHERE room_id_id={}'

        logger.debug("(userID={})Executing query: ".format(self.user) + query + "\n\twith params: " + str((room_id,)))

        cursor.execute(query.format(room_id))
        result = cursor.fetchall()
        return list(map(lambda user: user[0], result))

    def get_client_list(self, users, server):
        client_list = filter(lambda client: client.user in users, server.clients)
        # logger.debug("(userID={})Users selected to send message to: ".format(self.user) + str(client_list))

        return client_list

    def send_message(self, client_list, current_username):
        from xcomm.message import Message
        message = Message(body=self.msg.body)
        message.add_header_param(MESSAGE_ACTION, MESSAGE_ACTION_RECVMESSAGE_CODE)

        # Adding info about user and current date&time
        message.add_body_param(MESSAGE_ACTION_RECVMESSAGE_USER, current_username)
        time_now = datetime.datetime.now()
        message.add_body_param(MESSAGE_ACTION_RECVMESSAGE_TIMESTAMP, time_now.timestamp())

        logger.debug("Directing message to all users in room: " + message.get_complete_message().replace('\0', '\n'))

        message = message.convert_message_to_bytes()

        for client in client_list:
            client.client_socket.sendall(message)

    def _get_username_by_id(self, cursor):
        query = "SELECT username FROM users_user WHERE id = {}"

        logger.debug("(userID={})Executing query: ".format(self.user) + query + "\n\twith params: " + str(self.user))
        cursor.execute(query.format(self.user))
        result = cursor.fetchone()

        logger.debug("(userID={})Query result: ".format(self.user) + str(result))
        return result[0]
