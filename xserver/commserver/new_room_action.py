from xserver.commserver.action_base import ActionBase
from xserver.commserver.databaseconnection import DatabaseConnection

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_NEW_ROOM_CODE, MESSAGE_ACTION_NEW_ROOM_ROOM_NAME, \
    MESSAGE_ACTION_NEW_ROOM_USER_TOKEN
from xserver.commserver.decorators import login_required
from xserver.commserver.exceptions import UniqueRoomException


class NewRoomAction(ActionBase):

    def get_action_number(self):
        return MESSAGE_ACTION_NEW_ROOM_CODE

    @login_required
    def execute(self):
        room_name = self.msg.get_body_param(MESSAGE_ACTION_NEW_ROOM_ROOM_NAME)
        with self.db_connect as cursor:
            try:
                self._check_if_room_exists(room_name,cursor)
                self._add_room_to_db(room_name, self.user, cursor)
            except UniqueRoomException as e:
                self.set_error_with_status(e.message)
                return
        self.set_status_ok()

    def _check_if_room_exists(self, name,cursor):
        query = "SELECT * FROM chats_room WHERE name = '{}'"

        cursor.execute(query.format(name))
        result = cursor.fetchall()
        if result:
            raise UniqueRoomException()
        return

    def _add_room_to_db(self, name, owner_id,cursor):
        query = "INSERT INTO chats_room (name, owner_id)  VALUES ('{}', {})"

        cursor.execute(query.format(name, owner_id))
        self.db_connect.connection.commit()
