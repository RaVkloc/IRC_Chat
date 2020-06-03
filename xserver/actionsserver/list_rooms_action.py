from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LISTROOMS_CODE, MESSAGE_ACTION_LISTROOMS_LIST


class ListRoomsAction(ActionBase):

    def get_action_number(self):
        return MESSAGE_ACTION_LISTROOMS_CODE

    @login_required
    def execute(self):
        with self.db_connect as cursor:
            rooms = self._get_rooms_from_db(cursor)
            self.result.add_body_param(MESSAGE_ACTION_LISTROOMS_LIST, rooms)

            self.set_status_ok()

    def _get_rooms_from_db(self, cursor):
        query = "SELECT name FROM chats_room"

        cursor.execute(query)
        # it return list of tuples like [("a",), ("b",), ...]
        return self._convert_to_string(cursor.fetchall())

    def _convert_to_string(self, rooms_list):
        return ",".join(elem[0] for elem in rooms_list)
