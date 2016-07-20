#
# ELK Cleaner
#
#
# -> Run
#   -> if system disk trigger hits
#     -> start cleaning
#       -> get all (date) indexes
#       -> if an index is a date index, keep track of it
#          in a sorted list [oldest -> newest]
#       -> go through ordered (date) index list (index 0... onward)
#         -> remove each index until disk trigger is satisified

from butler import tools


def clean(batch=True):
    indicies = tools.get_indices_by_date()
    keys = sorted(indicies)
    removed = []

    for k in keys:
        for index in indicies[k]:
            if tools.delete_index(index):
                removed.append(index)

            # if batch is false check if we're done
            # batch mode gets rid of entire index list within a dict key
            if not batch and not tools.has_es_disk_trigger_hit():
                # enough disk exists, stop
                return removed

        # index gone, check disk, if good, stop, else move on to next key
        if not tools.has_es_disk_trigger_hit():
            return removed


def run():
    if tools.has_es_disk_trigger_hit():
        clean()

    return False
