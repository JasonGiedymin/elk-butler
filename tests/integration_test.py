# Test requires integration to run

from butler import tools
from butler import cleaner
from tests import seed
import pytest


@pytest.fixture(scope="module")
def seeder(request):
    def fin():
        count = seed.index_count()

        if count > 0:
            print ("Cleaning up {0} indicies...".format(count))
            seed.cleanup()
        else:
            print ("Clean up not necessary. Found 0 indicies.")

        assert len(tools.get_raw_indices()) == 0

    if not seed.load_data():
        raise Exception("Seed not successful!")

    request.addfinalizer(fin)


def test_get_indices(seeder):
    indices = tools.get_raw_indices()
    assert indices is not None
    assert len(tools.get_raw_indices()) > 0


def test_clean_indices(seeder):
    cleaner.clean()  # this does not call against
