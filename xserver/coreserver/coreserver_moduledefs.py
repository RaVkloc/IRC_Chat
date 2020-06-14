import os

SERVER_ADDRESS = "localhost"
SERVER_PORT = 6111
SERVER_MAX_CONNECTION = 5

SERVER_LOG_FILENAME = "../../server.log"
SERVER_LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s]: %(message)s"
SERVER_LOG_DATEFORMAT = "%H:%M:%S %m/%d/%Y"
SERVER_LOG_CONFIG = {"filename": "../../server.log",
                     "filemode": "w+",
                     "format": "%(asctime)s %(levelname)s [%(name)s]: %(message)s",
                     "datefmt": "%H:%M:%S %d/%m/%Y",
                     "level": "DEBUG"
                     }

SERVER_CERT = 'server.cert'
SERVER_KEY = 'server.key'
TLS = True
