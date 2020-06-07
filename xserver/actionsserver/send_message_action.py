from xcomm.xcomm_moduledefs import MESSAGE_ACTION_SENDMESSAGE_CODE
from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required
from xserver.actionsserver.exceptions import NoActiveRoomException


class SendMessageAction(ActionBase):
    def get_action_number(self):
        return MESSAGE_ACTION_SENDMESSAGE_CODE

    @login_required
    def execute(self, server=None):
        with self.db_connect as cursor:
            try:
                room = self._get_room_by_user(self.user, cursor)
                users = self._get_list_users_in_room(room, cursor)
                clients = self.get_client_list(users, server)
                self.send_message(clients)
            except NoActiveRoomException as e:
                self.set_error_with_status(e.message)
                return
            self.set_status_ok()

    def _get_room_by_user(self, user_id, cursor):
        query = 'SELECT room_id_id FROM users_user WHERE id ={}'
        cursor.execute(query.format(user_id))
        result = cursor.fetchone()
        if not result:
            raise NoActiveRoomException()
        return result[0]

    def _get_list_users_in_room(self, room_id, cursor):
        query = 'SELECT id FROM users_user WHERE room_id_id={}'
        cursor.execute(query.format(room_id))
        result = cursor.fetchall()
        return list(map(lambda user: user[0], result))

    def get_client_list(self, users, server):
        return filter(lambda client: client.user in users, server.clients)

    def send_message(self, client_list):
        message = self.msg.convert_message_to_bytes()
        for client in client_list:
            client.client_socket.sendall(message)
