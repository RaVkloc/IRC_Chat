from xserver.actionsserver.action_base import ActionBase

from xcomm.xcomm_moduledefs import MESSAGE_ACTION, MESSAGE_STATUS


class UnsupportedAction(ActionBase):

    def get_action_number(self):
        return self.msg.get_header_param(MESSAGE_ACTION)

    def execute(self):
        status_descr = "Unsupported or unimplemented action has been chosen."
        self.result.add_body_param(MESSAGE_STATUS, status_descr)
