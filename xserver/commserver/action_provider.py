from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_ACTIONLOGIN_Code, MESSAGE_ACTIONREGISTER_Code, \
    MESSAGE_ACTIONNEWROOM_Code
from xserver.commserver.login_action import LoginAction
from xserver.commserver.register_action import RegisterAction
from xserver.commserver.new_room_action import NewRoomAction
from xserver.commserver.unsupported_action import UnsupportedAction


class ActionProvider:
    action_dict = {MESSAGE_ACTIONLOGIN_Code: LoginAction,
                   MESSAGE_ACTIONREGISTER_Code: RegisterAction,
                   MESSAGE_ACTIONNEWROOM_Code: NewRoomAction}

    @staticmethod
    def get_action_for(message):
        value = message.get_header_param(MESSAGE_ACTION)
        action = ActionProvider.action_dict.get(value, None)

        if action:
            return action(message)
        else:
            return UnsupportedAction(message)
