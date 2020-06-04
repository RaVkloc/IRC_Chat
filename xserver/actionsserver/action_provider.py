from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_ACTION_LOGIN_CODE, MESSAGE_ACTION_REGISTER_CODE, \
    MESSAGE_ACTION_NEW_ROOM_CODE, MESSAGE_ACTION_JOIN_ROOM_CODE, MESSAGE_ACTION_LISTROOMS_CODE, \
    MESSAGE_ACTION_LEAVEROOM_CODE, MESSAGE_ACTION_LOGOUT_CODE
from xserver.actionsserver.login_action import LoginAction
from xserver.actionsserver.register_action import RegisterAction
from xserver.actionsserver.new_room_action import NewRoomAction
from xserver.actionsserver.join_room_action import JoinRoomAction
from xserver.actionsserver.list_rooms_action import ListRoomsAction
from xserver.actionsserver.leave_room_action import LeaveRoomAction
from xserver.actionsserver.logout_action import LogoutAction
from xserver.actionsserver.unsupported_action import UnsupportedAction


class ActionProvider:
    action_dict = {MESSAGE_ACTION_LOGIN_CODE: LoginAction,
                   MESSAGE_ACTION_REGISTER_CODE: RegisterAction,
                   MESSAGE_ACTION_NEW_ROOM_CODE: NewRoomAction,
                   MESSAGE_ACTION_JOIN_ROOM_CODE: JoinRoomAction,
                   MESSAGE_ACTION_LISTROOMS_CODE: ListRoomsAction,
                   MESSAGE_ACTION_LEAVEROOM_CODE: LeaveRoomAction,
                   MESSAGE_ACTION_LOGOUT_CODE: LogoutAction}

    @staticmethod
    def get_action_for(message):
        value = message.get_header_param(MESSAGE_ACTION)
        action = ActionProvider.action_dict.get(value, None)

        if action:
            return action(message)
        else:
            return UnsupportedAction(message)
