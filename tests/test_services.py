import pytest
from services import get_active_indices, format_text


@pytest.fixture()
def yui_sprinted():

    return {"tasks": [{"task": "test1", "ctime": 0},
                      {"task": "test2", "ctime": 0, "stime": 0}]}


@pytest.fixture()
def state_sprinted():

    return {"sprinted_only": True,
            "active_index": 0}


@pytest.fixture()
def state_unsprinted():

    return {"sprinted_only": False,
            "active_index": 0}


def test_get_active_indices_unsprinted(yui_sprinted, state_unsprinted):

    res = get_active_indices(yui_sprinted["tasks"], state_unsprinted)

    assert res[0] == 0


def test_get_active_indices_sprinted(yui_sprinted, state_sprinted):

    res = get_active_indices(yui_sprinted["tasks"], state_sprinted)

    assert res[0] == 1


def test_format_text_unsprinted(yui_sprinted, state_unsprinted):

    res = format_text(yui_sprinted["tasks"], state_unsprinted)

    assert "test1" in res
    assert "test2" in res
    assert "All Tasks" in res


def test_format_text_sprinted(yui_sprinted, state_sprinted):

    res = format_text(yui_sprinted["tasks"], state_sprinted)

    assert "test1" not in res
    assert "test2" in res
    assert "Sprint Tasks" in res


def test_format_text_unsprinted_exception(yui_sprinted, state_unsprinted):

    state_unsprinted["active_index"] = 3

    res = format_text(yui_sprinted["tasks"], state_unsprinted)

    assert state_unsprinted["active_index"] == 0
    assert "test1" in res
