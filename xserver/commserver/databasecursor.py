import mysql.connector as connector

from xserver.commserver.commserver_moduledefs import DATABASE_CREDENTIAL


class DatabaseCursor:
    def __init__(self):
        self.driver = connector
        self.connection = self.driver.connect(**DATABASE_CREDENTIAL)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def __iter__(self):
        for item in self.cursor:
            yield item

    # def test(self):
    #     self.cursor.execute("SHOW columns FROM users_token")
    #     # self.cursor.execute("SHOW tables")
    #     # self.cursor.execute("SELECT * FROM users_user")
    #     # self.cursor.execute('INSERT INTO users_user VALUES (122, "abcde", "22223")')
    #     # self.connection.commit()
    #     print(self.cursor.fetchall())
