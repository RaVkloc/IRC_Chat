import logging

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LEAVEROOM_CODE
from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required

logger = logging.getLogger("LeaveRoomAction")


class LeaveRoomAction(ActionBase):

    def get_action_number(self):
        return MESSAGE_ACTION_LEAVEROOM_CODE

    @login_required
    def execute(self):
        logger.debug("(userID={})Starting executing LEAVE_ROOM action.".format(self.user))
        with self.db_connect as cursor:
            self._remove_user_from_room(cursor)

            self.set_status_ok()
            logger.debug("(userID={})Executing action LOGOUT finished successfully.".format(self.user))

    def _remove_user_from_room(self, cursor):
        query = "UPDATE users_user SET room_id_id = null WHERE id = {}"

        logger.debug("(userID={})Executing query: ".format(self.user) + query + "\n\twith params: " + str((self.user,)))

        cursor.execute(query.format(self.user))
        self.db_connect.connection.commit()
        logger.debug("(userID={})Query executed successfully.".format(self.user))
