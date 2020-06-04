from xserver.actionsserver.action_base import ActionBase

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_JOIN_ROOM_CODE, MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME
from xserver.actionsserver.decorators import login_required
from xserver.actionsserver.exceptions import InvalidRoom, ChangeRoomException


class JoinRoomAction(ActionBase):

    def get_action_number(self):
        return MESSAGE_ACTION_JOIN_ROOM_CODE

    @login_required
    def execute(self):
        with self.db_connect as cursor:
            try:
                room_name = self.msg.get_body_param(MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME)
                room_id = self._get_room_id_from_name(room_name, cursor)
            except InvalidRoom as e:
                self.set_error_with_status(e.message)
                return
            if not room_id:
                self.set_error_with_status("Invalid room's name.")
                return
            try:
                self._update_user_room(self.user, room_id[0], cursor)
            except (ChangeRoomException, KeyError) as e:
                self.set_error_with_status(e.message)
                return

            self.set_status_ok()

    def _get_room_id_from_name(self, room_name, cursor):
        if not room_name:
            return
        query = "SELECT id FROM chats_room where name='{}'"

        cursor.execute(query.format(room_name))
        return cursor.fetchone()

    def _update_user_room(self, user_id, room_id, cursor):
        query = "UPDATE users_user SET room_id_id = {} WHERE id = {}"

        cursor.execute(query.format(room_id, user_id))
        self.db_connect.connection.commit()
