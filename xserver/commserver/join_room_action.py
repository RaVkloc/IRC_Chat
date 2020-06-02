from xcomm.message import Message
from xserver.commserver.action_base import ActionBase
from xserver.commserver.databaseconnection import DatabaseConnection

from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_STATUS, MESSAGE_STATUS_OK
from xcomm.xcomm_moduledefs import MESSAGE_ACTIONJOINROOM_Code, MESSAGE_ACTIONJOINROOM_RoomName, \
    MESSAGE_ACTIONJOINROOM_UserToken


class JoinRoomAction(ActionBase):
    def __init__(self, message):
        super().__init__(message)

    def get_action_number(self):
        return MESSAGE_ACTIONJOINROOM_Code

    def execute(self):
        self.result = Message()
        self.result.add_header_param(MESSAGE_ACTION, MESSAGE_ACTIONJOINROOM_Code)
        token = self.msg.get_body_param(MESSAGE_ACTIONJOINROOM_UserToken)

        try:
            user_id = self.__get_user_id_from_token(token)
            if not user_id:
                self.set_error_with_status("Invalid user token.")
                return
        except:
            self.set_error_with_status("Unable to verify user token. Please try again.")
            return

        try:
            room_name = self.msg.get_body_param(MESSAGE_ACTIONJOINROOM_RoomName)
            room_id = self.__get_room_id_from_name(room_name)
        except:
            self.set_error_with_status("Unable to get room's id. Try again later.")
            return

        if not room_id:
            self.set_error_with_status("Invalid room's name.")
            return
        try:
            self.__update_user_room(user_id, room_id)
        except:
            self.set_error_with_status("Unable to change room. Try again later.")
            return

        self.result.get_body_param(MESSAGE_STATUS, MESSAGE_STATUS_OK)

    def __get_user_id_from_token(self, token):
        if not token:
            return

        db_connect = DatabaseConnection()
        query = "SELECT id FROM users_user WHERE token = '{}'"

        db_connect.cursor.cursor.execute(query.format(token))
        result = db_connect.cursor.cursor.fetchone()
        if len(result) != 0:
            return result[0]
        else:
            return None

    def __get_room_id_from_name(self, room_name):
        if not room_name:
            return

        db_connect = DatabaseConnection()
        query = "SELECT id FROM chats_room where name='{}'"

        db_connect.cursor.cursor.execute(query.format(room_name))
        result = db_connect.cursor.cursor.fetchone()
        if len(result) != 0:
            return result[0]
        else:
            return None

    def __update_user_room(self, user_id, room_id):
        db_conn = DatabaseConnection()
        query = "UPDATE users_user SET room_id_id = {} WHERE id = {}"

        db_conn.cursor.cursor.execute(query.format(room_id, user_id))
        db_conn.cursor.connection.commit()
