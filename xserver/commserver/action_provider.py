from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_ACTIONLOGIN_Code, MESSAGE_ACTIONREGISTER_Code
from xserver.commserver.action_login import LoginAction
from xserver.commserver.action_register import ActionRegister


class ActionProvider:
    action_dict = {MESSAGE_ACTIONLOGIN_Code: LoginAction,
                   MESSAGE_ACTIONREGISTER_Code: ActionRegister}

    @staticmethod
    def get_action_for(message):
        value = message.get_header_param(MESSAGE_ACTION)

        if value:
            return ActionProvider.action_dict[value](message)
        else:
            return None
