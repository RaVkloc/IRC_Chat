from xcomm.xcomm_moduledefs import MESSAGE_ACTION_LEAVEROOM_CODE
from xserver.actionsserver.action_base import ActionBase
from xserver.actionsserver.decorators import login_required


class LeaveRoomAction(ActionBase):

    def get_action_number(self):
        return MESSAGE_ACTION_LEAVEROOM_CODE

    @login_required
    def execute(self):
        with self.db_connect as cursor:
            self._remove_user_from_room(cursor)

            # TODO: In the future, when messages sending will be implemented,
            #  we need to inform server somehow that user left

            self.set_status_ok()

    def _remove_user_from_room(self, cursor):
        query = "UPDATE users_user SET room_id_id = null WHERE id = {}"

        cursor.execute(query.format(self.user))
        self.db_connect.connection.commit()
