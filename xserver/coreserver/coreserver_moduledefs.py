def find_unique_filename():
    import os
    num = 1
    while os.path.isfile(SERVER_LOG_FILENAME.format(num)):
        num += 1
    return SERVER_LOG_FILENAME.format(num)


SERVER_ADDRESS = "51.38.191.101"
SERVER_PORT = 6111
SERVER_MAX_CONNECTION = 5

SERVER_LOG_FILENAME = "../../logs/server.log{}"
SERVER_LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s]: %(message)s"
SERVER_LOG_DATEFORMAT = "%H:%M:%S %m/%d/%Y"

SERVER_LOG_CONFIG = {"filename": find_unique_filename(),
                     "filemode": "w+",
                     "format": SERVER_LOG_FORMAT,
                     "datefmt": SERVER_LOG_DATEFORMAT,
                     "level": "DEBUG"
                     }

SERVER_CERT = 'server.cert'
SERVER_KEY = 'server.key'
TLS = True
SERVER_HOSTNAME = 'localhost'
