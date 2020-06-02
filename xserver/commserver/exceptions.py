class UniqueUsername(Exception):
    message = ''


class UnavailableRoom(Exception):
    pass


class InvalidRoom(Exception):
    message = "Unable to get room's id. Try again later."


class ChangeRoomException(Exception):
    message = "Unable to change room. Try again later."


class InvalidLoginData(Exception):
    message = "Unable to read user's data. Try again later."


class InvalidTokenSave(Exception):
    message = "Unable to update user's token. Try again later."
