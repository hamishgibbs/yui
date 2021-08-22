import pytest
from yui.tasks import (add_task,
                   sprint_task,
                   complete_task,
                   delete_task,
                   unsprint_task)


@pytest.fixture()
def yui():

    return {"tasks": [{"task": "test", "ctime": 0}]}


def test_add_task():

    yui = {"tasks": []}

    add_task(yui, "test")

    assert len(yui["tasks"]) == 1
    assert yui["tasks"][0]["task"] == "test"


def test_sprint_task(yui):

    sprint_task(yui["tasks"][0])

    assert "stime" in yui["tasks"][0].keys()


def test_complete_task(yui):

    complete_task(yui["tasks"][0])

    assert "xtime" in yui["tasks"][0].keys()


def test_delete_task(yui):

    delete_task(yui["tasks"][0])

    assert "otime" in yui["tasks"][0].keys()


def test_unsprint_task(yui):

    sprint_task(yui["tasks"][0])

    assert "stime" in yui["tasks"][0].keys()

    unsprint_task(yui["tasks"][0])

    assert "stime" not in yui["tasks"][0].keys()
