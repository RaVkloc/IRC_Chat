from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_ACTIONLOGIN_Code
from xserver.commserver.actions import LoginAction


class ActionProvider:
    action_dict = {MESSAGE_ACTIONLOGIN_Code: LoginAction}

    @staticmethod
    def get_action_for(message):
        value = message.get_header_param(MESSAGE_ACTION)

        if value:
            return ActionProvider.action_dict[value](message)
        else:
            return None
