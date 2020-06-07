class UniqueUsernameException(Exception):
    message = "Given username is already taken. Please try another one."


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


class ValidationPasswordException(Exception):
    message = "To weak password. Minimum length = 6."


class UniqueRoomException(Exception):
    message = "A room with the same name already exists. Try another name."


class NoActiveRoomException(Exception):
    message = "No room is active."
