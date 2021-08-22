import pytest
from yui.file import filter_active, filter_inactive


@pytest.fixture()
def tasks():

    return [
        {"otime": 1},
        {"xtime": 1},
        {"stime": 1}
    ]


def test_filter_active(tasks):

    res = filter_active(tasks)

    assert len(res) == 1


def test_filter_inactive(tasks):

    res = filter_inactive(tasks)

    assert len(res) == 2
