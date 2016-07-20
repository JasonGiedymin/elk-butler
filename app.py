#
# Elk Butler
#

from butler import cleaner
from butler import logger

import signal
import sys
import time
from os import environ


def signal_handler(signal, frame):
    logger.info("Shutting down")
    sys.exit(0)


def signal_timeout(alarm, frame):
    logger.error("Failed to run clean within the 30 second window.")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGALRM, signal_timeout)

#
# Flow:
#  - get timeout
#  - start timeout alarm
#  - clean
#  - sleep for the interval
#  - exit if task takes longer than timeout
#  - reset alarm
#  - repeat
while True:
    # allows live modification to timeout
    try:
        int(environ.get('ELK_BUTLER_TIMEOUT', '60'))
    except:
        msg = "The timeout supplied for 'ELK_BUTLER_TIMEOUT'" + \
              "is not an integer (representing seconds): {0}" \
                  .format(environ.get('ELK_BUTLER_TIMEOUT'))
        logger.error(msg)
        raise Exception(msg)

    timeout = int(environ.get('ELK_BUTLER_TIMEOUT', '30'))
    signal.alarm(timeout)

    cleaner.run()

    # allows live modification to interval
    try:
        int(environ.get('ELK_BUTLER_INTERVAL', '60'))
        seconds = int(environ.get('ELK_BUTLER_INTERVAL', '60'))
    except:
        msg = "The interval supplied for 'ELK_BUTLER_INTERVAL'" + \
              "is not an integer (representing seconds): {0}"\
                  .format(environ.get('ELK_BUTLER_INTERVAL'))

        logger.error(msg)
        raise Exception(msg)

    signal.alarm(0)
    logger.info("Sleeping {0} seconds...".format(seconds))
    time.sleep(seconds)

