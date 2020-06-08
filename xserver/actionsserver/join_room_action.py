import logging

from xserver.actionsserver.action_base import ActionBase

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_JOIN_ROOM_CODE, MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME
from xserver.actionsserver.decorators import login_required
from xserver.actionsserver.exceptions import InvalidRoom, ChangeRoomException

logger = logging.getLogger("JoinRoomAction")


class JoinRoomAction(ActionBase):

    def get_action_number(self):
        return MESSAGE_ACTION_JOIN_ROOM_CODE

    @login_required
    def execute(self):
        logger.debug("(userID={})Executing action JOIN_ROOM started.".format(self.user))
        with self.db_connect as cursor:
            try:
                room_name = self.msg.get_body_param(MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME)
                room_id = self._get_room_id_from_name(room_name, cursor)
            except InvalidRoom as e:
                self.set_error_with_status(e.message)
                logger.debug("(userID={}) Room not found. Problem with getting room id.".format(self.user))
                return
            try:
                self._update_user_room(self.user, room_id[0], cursor)
            except (ChangeRoomException, KeyError) as e:
                self.set_error_with_status(e.message)
                return

            self.result.add_body_param(MESSAGE_ACTION_JOIN_ROOM_ROOM_NAME, room_name)
            self.set_status_ok()
            logger.debug("(userID={})Executing action JOIN_ROOM finished SUCCESSFULLY.".format(self.user))

    def _get_room_id_from_name(self, room_name, cursor):
        if not room_name:
            return
        query = "SELECT id FROM chats_room where name='{}'"

        logger.debug(
            "(userID={})Executing query: ".format(self.user) + query + "\n\twith params: " + str((room_name,)))

        cursor.execute(query.format(room_name))
        result = cursor.fetchone()
        if not result:
            raise InvalidRoom
        logger.debug("(userID={})Query result: ".format(self.user) + str(result))
        return result

    def _update_user_room(self, user_id, room_id, cursor):
        query = "UPDATE users_user SET room_id_id = {} WHERE id = {}"

        logger.debug(
            "(userID={})Executing query: ".format(self.user) + query + "\n\twith params: " + str((room_id, user_id)))

        cursor.execute(query.format(room_id, user_id))
        self.db_connect.connection.commit()
        logger.debug("(userID={})Execution successful.".format(self.user))
