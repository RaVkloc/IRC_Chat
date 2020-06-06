import logging

from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required
from xserver.actionsserver.exceptions import NoActiveRoomException

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_SENDMESSAGE_CODE

logger = logging.getLogger("SendMessageAction")


class SendMessageAction(ActionBase):
    def get_action_number(self):
        return MESSAGE_ACTION_SENDMESSAGE_CODE

    @login_required
    def execute(self, *args, **kwargs):
        logger.debug("(userID={})Executing SEND_MESSAGE action started.".format(self.user))
        with self.db_connect as cursor:
            try:
                room = self._get_room_by_user(self.user, cursor)
                users = self._get_list_users_in_room(room, cursor)
                clients = self.get_client_list(users)
                self.send_message(clients)
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
        logger.debug("(userID={})Query result: ".format(self.user) + str(result))

        return result

    def get_client_list(self, users):
        from xserver.coreserver.server_core import CoreServer
        client_list = CoreServer.__instance.clients
        clients = list(filter(lambda client: client.user in users, client_list))
        logger.debug("(userID={})Users selected to send message to: ".format(self.user) + str(clients))

        return clients

    def send_message(self, client_list):
        message = self.msg.convert_message_to_bytes()
        for client in client_list:
            client.client_socket.send_message(message)
