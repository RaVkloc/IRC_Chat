import logging

from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LISTROOMS_CODE, MESSAGE_ACTION_LISTROOMS_LIST

logger = logging.getLogger("ListRoomAction")


class ListRoomsAction(ActionBase):

    def get_action_number(self):
        return MESSAGE_ACTION_LISTROOMS_CODE

    @login_required
    def execute(self):
        logger.debug("(userID={})Executing LISTROOM action started.".format(str(self.user)))
        with self.db_connect as cursor:
            rooms = self._get_rooms_from_db(cursor)
            self.result.add_body_param(MESSAGE_ACTION_LISTROOMS_LIST, rooms)

            self.set_status_ok()
            logger.debug("(userID={})Executing LISTROOM finished SUCCESSFULLY.".format(str(self.user)))

    def _get_rooms_from_db(self, cursor):
        query = "SELECT name FROM chats_room"

        logger.debug("(userID={})Executing query: ".format(str(self.user)) + query)

        cursor.execute(query)
        # it return list of tuples like [("a",), ("b",), ...]
        result = cursor.fetchall()
        logger.debug("(userID={})Query result: ".format(str(self.user)) + str(result))
        return self._convert_to_string(result)

    def _convert_to_string(self, rooms_list):
        return ",".join(elem[0] for elem in rooms_list)
