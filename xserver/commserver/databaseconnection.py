import xserver.commserver.databasecursor as dbcursor


class DatabaseConnection:
    def __init__(self):
        self.cursor = dbcursor.DatabaseCursor()
