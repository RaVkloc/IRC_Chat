import logging

from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LOGOUT_CODE


class LogoutAction(ActionBase):
    def get_action_number(self):
        return MESSAGE_ACTION_LOGOUT_CODE

    @login_required
    def execute(self):
        with self.db_connect as cursor:
            self._logout_user_in_db(self.user, cursor)

            self.set_status_ok()

    def _logout_user_in_db(self, user_id, cursor):
        logger = logging.getLogger("LogoutAction")
        query = "UPDATE users_user SET token = null, room_id_id = null WHERE id = {}"

        logger.debug("Executing query: " + query + "\n\twith params: " + str(self.user))

        cursor.execute(query.format(user_id))
        self.db_connect.connection.commit()
