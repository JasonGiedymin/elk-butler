import logging
import string
from logging.handlers import TimedRotatingFileHandler
from os import environ, path, makedirs


def get_log_level():
    level = environ.get('ELK_BUTLER_LOGLEVEL', 'INFO').lower()

    if level == 'warning':
        return logging.WARNING
    elif level == 'debug':
        return logging.DEBUG
    elif level == 'trace':
        return logging.DEBUG
    else:
        return logging.INFO


def setup_file_handler():
    log_file = environ.get('ELK_BUTLER_LOGFILE', '/var/log/elk-butler/process.log').lower()
    log_dir = path.dirname(path.realpath(log_file))

    if not path.exists(log_dir):
        try:
            makedirs(log_dir)
        except Exception as e:
            msg = "Could not create directory {0} due to {1}".format(log_dir, e)
            print(msg)
            raise Exception(msg)

    return TimedRotatingFileHandler(log_file, when='d')


def init_logger():
    level = environ.get('ELK_BUTLER_LOGLEVEL', 'TRACE').lower()

    if level == 'trace':
        logger = logging.getLogger()
    else:
        logger = logging.getLogger("elk-butler")

    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    # Stream
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # File
    file_handler = setup_file_handler()
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(get_log_level())

    return logger


def get_logger():
    return root_logger


def debug(msg):
    return get_logger().debug(msg)


def info(msg):
    return get_logger().info(msg)


def warn(msg):
    return get_logger().warn(msg)


def error(msg):
    return get_logger().error(msg)

root_logger = init_logger()
