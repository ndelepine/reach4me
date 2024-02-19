# coding: utf-8
from reach4me.sms.twilio import TwilioHelper
import pytest
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


@pytest.fixture(scope="function")
def helper():
    helper = TwilioHelper(sender="test", sid="mySid", token="123")
    yield helper

def test_creation(helper):

    assert isinstance(helper.client, Client)
    assert helper.client.username == "mySid"
    assert helper.client.password == "123"

def test_send_message(mocker, helper):

    # mock the twilio.Client object
    mock_twilio = mocker.MagicMock(name="reach4me.sms.twilio.Client")
    mocker.patch("reach4me.sms.twilio.Client", new=mock_twilio)

    helper.send_message(to="recipient@test.com",  msg="Hellow world!")

    assert mock_twilio.return_value.messages.create.call_count == 1

def test_send_messag_ko(mocker, helper):

    # mock the twilio.Client object
    mock_twilio = mocker.MagicMock(name="reach4me.sms.twilio.Client")
    mocker.patch("reach4me.sms.twilio.Client", new=mock_twilio)

    # mock TwilioRestException error
    mock_twilio.side_effect = TwilioRestException(status=1, uri="test.com")

    with pytest.raises(TwilioRestException):
        helper.send_message(to="recipient@test.com",  msg="Hellow world!")
