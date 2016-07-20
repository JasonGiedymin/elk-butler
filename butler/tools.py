#
# Elasticsearch Tools
#

from butler import clients
from butler import logger
from datetime import datetime
from os import environ, statvfs
import re
import string


def get_current_date(now):
    """
    Returns the current date time as a string in the format of
    'YYYY.MM.DD'. For example: '2000.01.01'.

    The method will use now unless given a datetime to use.

    :param now: datetime object which to convert
    :return: string representation as 'YYYY.MM.DD'
    """
    if now is None:
        now = datetime.now()

    return now.strftime('%Y.%m.%d')


def get_disk_remaining(path="/"):
    """
    Returns the amount of disk space remaining as a percentage for
    the user specified path. 0 for zero percent, 1 for 100 percent.

    :param path: user specified path otherwise the root path '/' is assumed
    :return: a float representing the amount of disk space remaining as a
             fraction of 1
    """
    st = statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    # used = (st.f_blocks - st.f_bfree) * st.f_frsize

    pct_remaining = float(free) / float(total)
    logger.debug("disk remaining for {0}: {1}".format(path, pct_remaining))
    return pct_remaining


def has_es_disk_trigger_hit(override_path=''):
    """
    Returns True or False based on if the remaining disk space at the user
    defined path is lower than the trigger. The defined path is obtained
    from the OS environment variable 'ELK_DISK_MOUNT'. An `override_path`
    may be supplied.

    The trigger is obtained from the OS environment variable 'ES_DISK_TRIGGER'.

    :param override_path: user defined path to obtain remaining disk space,
     defaults to root '/' eventually when lokoing for `ELK_DISK_MOUNT`
    :return: True if trigger has been met, False otherwise
    """
    path = '/'

    # no override specified, get from env, but default to root if not exist
    if len(override_path) == 0:
        path = environ.get('ELK_DISK_MOUNT', '/')
    else:
        path = override_path

    r = get_disk_remaining(path)
    es_disk_trigger = environ.get('ES_DISK_TRIGGER', '20')
    trigger = r <= float(float(es_disk_trigger)/100)

    logger.debug("Trigger: {0}, Hit: {1}".format(es_disk_trigger, trigger))

    return trigger


def is_date_index(index):
    """
    Checks whether the index is of the agreed upon date format.
    In this case YYYY.MM.DD. This is a very 'EU' centric date.
    Would have preferred YYYY-MM-DD which is more ISO, however
    there are dates which exist in the 'EU' format already (topbeat).

    Note that match is very fast. It is faster than doing search and
    pulling groups. Using this method helps decouple using a single
    regex pattern for all things. While using this method along with
    get_date_from_index() below is 2n, we can ensure cognitive load
    is low - which is a secondary goal of this repo.

    :param index:
    :return:
    """
    date_pattern = '.*?-\d{4}[-/:.]\d{2}[-/:.]\d{2}'
    match = re.match(date_pattern, index)
    if match is not None:
        return True

    return False


def get_date_from_index(index_name):
    date_pattern = '(\d{4}[-/:.]\d{2}[-/:.]\d{2})'
    match = re.search(date_pattern, index_name)

    if match is not None:
        return match.groups()[0]

    return None


def index_dict_by_date(indices):
    output_dict = {}

    for i in indices:
        if is_date_index(i):
            key = date_to_int(get_date_from_index(i))

            if key in output_dict:
                output_dict[key].append(i)
            else:
                output_dict[key] = [i]

    return output_dict


def get_raw_indices():
    es = clients.create()

    # TODO: make index a type, with health
    # health = es.cluster.health(level='indices')
    # i_key = 'indices'
    # indices = health[i_key]
    #
    # if i_key in health and len(indices) > 0:
    #     return indices
    # else:
    #     return []

    indicies = es.indices.get("*")
    if len(indicies) > 0:
        return indicies
    else:
        return []


def get_indices_by_date(sorted=True):
    return index_dict_by_date(get_raw_indices())


def date_to_int(date_string):
    return int(string.replace(date_string, ".", ""))


def delete_index(index_name):
    es = clients.create()
    res = es.indices.delete(index=index_name)
    acknowledged = res['acknowledged']

    logger.debug("Index deleted: {0}, acknowledged: {1}".format(index_name, acknowledged))

    return acknowledged
