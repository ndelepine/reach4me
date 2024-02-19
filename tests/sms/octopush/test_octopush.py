# coding: utf-8
from reach4me.sms.octopush import OctopushHelper, InsuffisantBalanceException
import pytest
from requests import HTTPError

@pytest.fixture(scope="function")
def helper():
    helper = OctopushHelper(sender="test", login="test", token="123")
    yield helper

def test_creation(helper):

    assert isinstance(helper.client, dict)
    assert helper.client["api-login"] == "test"
    assert helper.client["api-key"] == "123"

def test_parse_recipient_str(helper):
    result = helper._parse_recipient(recipient="+33123456789")
    assert result == [{"phone_number" : "+33123456789"}]

def test_parse_recipient_list(helper):
    result = helper._parse_recipient(recipient=["+33123456789", "+33987654321"])
    assert result == [{"phone_number" : "+33123456789"}, {"phone_number" : "+33987654321"}]

def test_parse_recipient_ko(helper):
    result = helper._parse_recipient(recipient=["+33123456789", "+33987654321"])
    assert result == [{"phone_number" : "+33123456789"}, {"phone_number" : "+33987654321"}]

def test_parse_recipient_error(helper):
    with pytest.raises(ValueError, match="recipient should be a string or a list of string"):
        helper._parse_recipient([1, 2])

def test_get_balance(mocker, helper):
    # mock the requests object
    mock_requests = mocker.MagicMock(name="reach4me.sms.octopush.requests")
    mocker.patch("reach4me.sms.octopush.requests", new=mock_requests)

    helper._get_balance()

    assert mock_requests.get.call_count == 1

def test_get_balance_ko(mocker, helper):
    # mock the requests.get function
    mock_requests_get = mocker.MagicMock(name="reach4me.sms.octopush.requests.get")
    mocker.patch("reach4me.sms.octopush.requests.get", new=mock_requests_get)

    # mock HTTPError error
    mock_requests_get.side_effect = HTTPError

    with pytest.raises(HTTPError):
        helper._get_balance()
    

def test_send_message_insuffisant_balance(mocker, helper):

    # mock the _get_balance value
    mocker.patch("reach4me.sms.octopush.OctopushHelper._get_balance", return_value=0)

    with pytest.raises(InsuffisantBalanceException):
        helper.send_message(to="recipient@test.com",  msg="Hellow world!")


def test_send_message(mocker, helper):

    # mock the _get_balance value
    mocker.patch("reach4me.sms.octopush.OctopushHelper._get_balance", return_value=11)
    # mock the requests object
    mock_requests = mocker.MagicMock(name="reach4me.sms.octopush.requests")
    mocker.patch("reach4me.sms.octopush.requests", new=mock_requests)

    helper.send_message(to="recipient@test.com",  msg="Hellow world!")

    assert mock_requests.post.call_count == 1

def test_send_error(mocker, helper):

    # mock the _get_balance value
    mocker.patch("reach4me.sms.octopush.OctopushHelper._get_balance", return_value=11)
    # mock the requests.post function
    mock_requests_post = mocker.MagicMock(name="reach4me.sms.octopush.requests.post")
    mocker.patch("reach4me.sms.octopush.requests.post", new=mock_requests_post)

    # mock HTTPError error
    mock_requests_post.side_effect = HTTPError

    with pytest.raises(HTTPError):
        helper.send_message(to="recipient@test.com",  msg="Hellow world!")
