from xserver.commserver.action_base import ActionBase
from xserver.commserver.databaseconnection import DatabaseConnection

from xcomm.xcomm_moduledefs import MESSAGE_ACTION_NEW_ROOM_CODE, MESSAGE_ACTION_NEW_ROOM_ROOM_NAME, \
    MESSAGE_ACTION_NEW_ROOM_USER_TOKEN
from xserver.commserver.decorators import login_required


class NewRoomAction(ActionBase):

    def get_action_number(self):
        return MESSAGE_ACTION_NEW_ROOM_CODE

    @login_required
    def execute(self):
        room_name = self.msg.get_body_param(MESSAGE_ACTION_NEW_ROOM_ROOM_NAME)

        try:
            user_id = self.__get_user_id_from_token(self.msg.get_body_param(MESSAGE_ACTION_NEW_ROOM_USER_TOKEN))
            if not user_id:
                self.set_error_with_status("Invalid user token.")
                return
        except:
            self.set_error_with_status("Unable to verify user token. Please try again.")
            return

        try:
            if self.__check_if_room_exists(room_name):
                self.set_error_with_status("A room with the same name already exists. Try another name.")
                return
        except:
            self.set_error_with_status("Can not check uniqueness of room's name.")
            return

        try:
            self.__add_room_to_db(room_name, user_id)
        except:
            self.set_error_with_status("Unable to save changes.")
            return

        self.set_status_ok()

    def __check_if_room_exists(self, name):
        db_connect = DatabaseConnection()
        query = "SELECT * FROM chats_room WHERE name = '{}'"

        db_connect.cursor.cursor.execute(query.format(name))
        result = db_connect.cursor.cursor.fetchall()

        return False if len(result) == 0 else True

    def __get_user_id_from_token(self, token):
        if not token:
            return

        db_connect = DatabaseConnection()
        query = "SELECT id FROM users_user WHERE token = '{}'"

        db_connect.cursor.cursor.execute(query.format(token))
        return db_connect.cursor.cursor.fetchone()[0]

    def __add_room_to_db(self, name, owner_id):
        db_conect = DatabaseConnection()
        query = "INSERT INTO chats_room (name, owner_id)  VALUES ('{}', {})"

        db_conect.cursor.cursor.execute(query.format(name, owner_id))
        db_conect.cursor.connection.commit()
