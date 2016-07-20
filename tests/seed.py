#
# Integration Testing Tools
#
# DO NOT USE THE BUTLER LIBRARY USE, RAW CLIENT CODE HERE
#

from butler import clients
from datetime import datetime


TEST_INDEX = 'data-2016.04.01'


def load_data():
    """
    Load test data for integration tests.
    """

    doc_type = 'testdata'

    doc = {
        'author': 'Test-Author',
        'text': 'ABCDEDF... 123456...',
        'timestamp': datetime.now(),
    }

    es = clients.create()

    res = es.index(index=TEST_INDEX, doc_type=doc_type, id=1, body=doc)
    print(res['created'])

    res = es.get(index=TEST_INDEX, doc_type=doc_type, id=1)
    print(res['_source'])

    es.indices.refresh(index=TEST_INDEX)

    print('Loading Complete.')

    return True


def index_count():
    es = clients.create()
    return len(es.indices.get("*"))


def cleanup():
    """
    Cleanup of Integration testing data.
    """

    es = clients.create()
    res = es.indices.delete(index=TEST_INDEX)
    acknowledged = res['acknowledged']
    if acknowledged:
        print("server acknowledged: {0}".format(acknowledged))
    else:
        raise Exception("Could not perform cleanup!")

    print("Cleanup complete.")

