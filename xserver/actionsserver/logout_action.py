import logging

from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LOGOUT_CODE

logger = logging.getLogger("LogoutAction")


class LogoutAction(ActionBase):
    def get_action_number(self):
        return MESSAGE_ACTION_LOGOUT_CODE

    @login_required
    def execute(self):
        with self.db_connect as cursor:
            self.logout_user_in_db(self.user, cursor)

            self.set_status_ok()
            logger.debug("(userID={}Executing action LOGOUT finished SUCCESSFULLY.".format(self.user))

    @classmethod
    def logout_user_in_db(cls, user_id, cursor):
        query = "UPDATE users_user SET token = null, room_id_id = null WHERE id = {}"

        logger.debug("(userID={})Executing query: ".format(user_id) + query + "\n\twith params: " + str(user_id))

        cursor.execute(query.format(user_id))
        cursor.connection.commit()
        logger.debug("(userID={})Query executed successfully.".format(user_id))
