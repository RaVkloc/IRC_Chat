import logging

from xserver.actionsserver.action_base import ActionBase

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_NEW_ROOM_CODE, MESSAGE_ACTION_NEW_ROOM_ROOM_NAME
from xserver.actionsserver.decorators import login_required
from xserver.actionsserver.exceptions import UniqueRoomException

logger = logging.getLogger("NewRoomAction")


class NewRoomAction(ActionBase):

    def get_action_number(self):
        return MESSAGE_ACTION_NEW_ROOM_CODE

    @login_required
    def execute(self):
        logger.debug("(userID={})Executing action NEW_ROOM started.".format(self.user))
        room_name = self.msg.get_body_param(MESSAGE_ACTION_NEW_ROOM_ROOM_NAME)
        with self.db_connect as cursor:
            try:
                self._check_if_room_exists(room_name, cursor)
                self._add_room_to_db(room_name, self.user, cursor)
            except UniqueRoomException as e:
                self.set_error_with_status(e.message)
                return

        self.set_status_ok()
        logger.debug("(userID={})Executing action NEW_ROOM finished SUCCESSFULLY.".format(self.user))

    def _check_if_room_exists(self, name, cursor):
        query = "SELECT * FROM chats_room WHERE name = '{}'"

        logger.debug("(userID={})Executing guery: ".format(self.user) + query + "\n\twith params: " + str(name, ))

        cursor.execute(query.format(name))
        result = cursor.fetchall()
        logger.debug("(userID={})Query result: ".format(self.user) + str(result))
        if result:
            logger.debug("(userID={})Such a room exists already.".format(self.user))
            raise UniqueRoomException()
        return

    def _add_room_to_db(self, name, owner_id, cursor):
        query = "INSERT INTO chats_room (name, owner_id)  VALUES ('{}', {})"

        logger.debug(
            "(userID={})Executing query: ".format(self.user) + query + "\n\twith params: " + str((name, owner_id)))

        cursor.execute(query.format(name, owner_id))
        self.db_connect.connection.commit()
        logger.debug("(userID={})Query executed successfully.".format(self.user))
