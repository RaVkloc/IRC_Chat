import logging

from xserver.commserver.databaseconnection import DatabaseConnection
from xserver.actionsserver.settings import TOKEN_KEY, AUTHENTICATION_ERROR

logger = logging.getLogger("Decorator")


def login_required(f):
    def inner(self,*args,**kwargs):
        token = self.msg.get_header_param(TOKEN_KEY)
        logger.debug("Checking if user is logged. Token=" + token)

        if not token:
            self.set_error_with_status(AUTHENTICATION_ERROR)
            return
        query = "SELECT id from users_user where token='{}'".format(token)
        logger.debug("Executing query: " + query)

        connection = DatabaseConnection()
        with connection as cursor:
            cursor.execute(query)
            user = cursor.fetchone()
            logger.debug("Query result: " + str(user))
        if not user:
            self.set_error_with_status(AUTHENTICATION_ERROR)
            logger.debug("Action not available. User not logged.")
            return
        self.user = user[0]
        logger.debug("User has been already logged.")
        return f(self,*args,**kwargs)

    return inner
