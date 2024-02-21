# coding: utf-8
from reach4me import AlertingTool
import pytest


@pytest.fixture
def client(mocker):

    # mock the requests.get function
    mocker.patch("reach4me.AlertingTool.__abstractmethods__", new=set())

    client = AlertingTool(sender="sender")
    return client


def test_send(client):
    client.send(to="recipient", msg="Hello World!")
