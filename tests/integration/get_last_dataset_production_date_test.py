from ronal.core import _create_production_period
from ronal.core import ProductionPeriod
import pytest


@pytest.fixture(scope="module")
def datasets():
    import json
    with open('./tests/fixtures/datasets/NAN-datasets.json', 'r') as f:
        return json.load(f)


@pytest.fixture(scope="module")
def no_datasets():
    import json
    with open('./tests/fixtures/datasets/NAN-no-datasets.json', 'r') as f:
        return json.load(f)


@pytest.fixture(scope="module")
def empty_datasets():
    import json
    with open('./tests/fixtures/datasets/NAN-empty-datasets.json', 'r') as f:
        return json.load(f)


def test_get_last_dataset_production_date(datasets, no_datasets, empty_datasets):
    """
    Test fetching from navitia the last dataset production period
    """

    last_production_date = _create_production_period(datasets)

    assert isinstance(last_production_date, ProductionPeriod)
    assert last_production_date.start_validation_date.strftime('%Y%m%dT%H%M%S') == '20150114T010000'
    assert last_production_date.end_validation_date.strftime('%Y%m%dT%H%M%S') == '20150701T020000'

    with pytest.raises(Exception) as exception_info:
        _create_production_period(no_datasets)

    with pytest.raises(Exception) as exception_info:
        _create_production_period(empty_datasets)
