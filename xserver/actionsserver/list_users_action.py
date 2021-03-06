import logging

from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required
from xserver.actionsserver.exceptions import NoActiveRoomException

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LISTUSERS_LIST, \
    MESSAGE_ACTION_LISTUSERS_CODE

logger = logging.getLogger("ListUserAction")


class ListUsersAction(ActionBase):
    def get_action_number(self):
        return MESSAGE_ACTION_LISTUSERS_CODE

    @login_required
    def execute(self):
        logger.debug("(userID={})Executing LIST_USER action started.".format(str(self.user)))
        with self.db_connect as cursor:
            try:
                users = self.get_users_in_room_from_database(cursor)
                self.result.add_body_param(MESSAGE_ACTION_LISTUSERS_LIST, users)
                self.set_status_ok()
                logger.debug("(userID={})Executing LIST_USER finished SUCCESSFULLY.".format(str(self.user)))
            except NoActiveRoomException as e:
                self.set_error_with_status(e.message)
                logger.debug("(userID={})User not in room. Problem with getting room id.".format(self.user))

    def get_users_in_room_from_database(self, cursor):
        query = "SELECT username FROM users_user WHERE room_id_id = '{}'"

        room_id = self._get_user_room_id(cursor)
        logger.debug(
            "(userID={})Executing query: ".format(str(self.user)) + query + "\n\twith params: " + str((room_id[0],)))

        cursor.execute(query.format(room_id[0]))

        result = cursor.fetchall()
        logger.debug("(userID={})Query result: ".format(str(self.user)) + str(result))

        return self._convert_to_string(result)

    def _get_user_room_id(self, cursor):
        query = "SELECT room_id_id FROM users_user where id = {}"

        logger.debug(
            "(userID={})Executing query: ".format(str(self.user)) + query + "\n\twith params: " + str((self.user,)))

        cursor.execute(query.format(self.user))
        result = cursor.fetchone()

        logger.debug("(userID={})Query result: ".format(str(self.user)) + str(result))

        if not result[0]:
            raise NoActiveRoomException

        return result

    def _convert_to_string(self, users_list):
        return ",".join(elem[0] for elem in users_list)
