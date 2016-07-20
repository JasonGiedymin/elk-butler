from butler import tools

from datetime import datetime
from os import environ


def test_get_current_date():
    # produces: datetime.datetime(2016, 4, 11, 10, 50, 21, 308771)
    base_timestamp = 1460386068.594937

    # use this specific time index
    curr_date = datetime.fromtimestamp(base_timestamp)

    assert tools.get_current_date(curr_date) == "2016.04.11"
    assert len(tools.get_current_date(None)) == 10


def test_get_disk_remaining():
    space = tools.get_disk_remaining()
    assert space is not None
    assert space >= 0.0
    assert space <= 1.0


def test_es_disk_trigger():
    """
    This test will specificaly set the disk trigger.
    Will not go lower than 1%.
    :return:
    """
    # track the original value in case other tests rely on
    # it
    has_orig = 'ES_DISK_TRIGGER' in environ
    orig_value = environ.get('ES_DISK_TRIGGER', '')

    # now set to something lower than remaining so that
    # the trigger will be hit
    # note that the env flag is a fraction of 100
    r_miss = float(tools.get_disk_remaining() * 100) - 1
    environ['ES_DISK_TRIGGER'] = str(r_miss)
    assert tools.has_es_disk_trigger_hit() is False

    # now set to something higher than remaining so that
    # the trigger will be hit
    # note that the env flag is a fraction of 100
    r_hit = float(tools.get_disk_remaining() * 100) + 1
    environ['ES_DISK_TRIGGER'] = str(r_hit)
    assert tools.has_es_disk_trigger_hit() is True

    if has_orig:
        environ['ES_DISK_TRIGGER'] = orig_value


def test_is_date_index():
    # dates should be YYYY-MM-DD not MM-DD-YYYY
    bad_order = tools.is_date_index("01.01.2000")
    assert bad_order is False

    # month and day should be zero padded for single digits
    d1 = tools.is_date_index("2000.1.1")
    assert d1 is False

    #
    d2 = tools.is_date_index("2000.01.01")
    assert d2 is False

    with_prefix = tools.is_date_index("sometext-2000.01.01")
    assert with_prefix is True


def test_get_date_from_index():
    assert (tools.get_date_from_index("sometext-2000.01.01")) == "2000.01.01"
    assert (tools.get_date_from_index("2000.01.01")) == "2000.01.01"
    assert (tools.get_date_from_index("1224-2000.01.01")) == "2000.01.01"
    assert (tools.get_date_from_index("1224-2000.01.01--blahblah")) == "2000.01.01"
    assert (tools.get_date_from_index("12242000.01.01blahblah")) == "2000.01.01"
    assert (tools.get_date_from_index("1224.2000.01.01blahblah")) == "2000.01.01"
    assert (tools.get_date_from_index("1224.2000.01.01blah.blah")) == "2000.01.01"
    assert (tools.get_date_from_index("1224.2000.01.01.11.1234.blah.blah")) == "2000.01.01"


def test_process_indices():
    mock_indices_from_server = [
        "sometext1-2000.01.01",
        "sometext2-2000.01.01",
        "sometext3-2000.01.01",
        "sometext-other-2000.01.02"
    ]

    # rename to index dict
    index_dict = tools.index_dict_by_date(mock_indices_from_server)
    assert len(index_dict) is 2

    assert len(index_dict[20000101]) is 3
    assert len(index_dict[20000102]) is 1
