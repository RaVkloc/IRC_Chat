from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_ACTION_LOGIN_CODE, MESSAGE_ACTION_REGISTER_CODE, \
    MESSAGE_ACTION_NEW_ROOM_CODE, MESSAGE_ACTION_JOIN_ROOM_CODE
from xserver.commserver.login_action import LoginAction
from xserver.commserver.register_action import RegisterAction
from xserver.commserver.new_room_action import NewRoomAction
from xserver.commserver.join_room_action import JoinRoomAction
from xserver.commserver.unsupported_action import UnsupportedAction


class ActionProvider:
    action_dict = {MESSAGE_ACTION_LOGIN_CODE: LoginAction,
                   MESSAGE_ACTION_REGISTER_CODE: RegisterAction,
                   MESSAGE_ACTION_NEW_ROOM_CODE: NewRoomAction,
                   MESSAGE_ACTION_JOIN_ROOM_CODE: JoinRoomAction}

    @staticmethod
    def get_action_for(message):
        value = message.get_header_param(MESSAGE_ACTION)
        action = ActionProvider.action_dict.get(value, None)

        if action:
            return action(message)
        else:
            return UnsupportedAction(message)
