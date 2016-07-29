from ronal.core import Handler
import pytest

@pytest.fixture(scope="module")
def datasets():
    import json
    with open('./tests/fixtures/datasets/NAN-datasets.json', 'r') as f:
        return json.load(f)

def test_get_last_dataset_production_date(datasets):
    """
    Test fetching from navitia the last dataset production period
    """
    expected_last_production_date = {
         'end_validation_date': '20150701T020000',
         'start_validation_date': '20150114T010000'
    }

    handler = Handler({})
    last_production_date = handler.get_last_dataset_production_date(datasets)

    assert last_production_date == expected_last_production_date

