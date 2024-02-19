# coding: utf-8
from reach4me.emailing import EmailAlertingTool
import pytest
import smtplib


@pytest.fixture(scope="function")
def helper():
    helper = EmailAlertingTool(sender="test@test.com", smtp_host="localhost", smtp_port=2525)
    yield helper

def test_parse_recipient_str():
    result = EmailAlertingTool._parse_recipient("test@test.com")
    assert result == ["test@test.com"]

def test_parse_recipient_list():
    result = EmailAlertingTool._parse_recipient(["test1@test.com", "test2@test.com"])
    assert result == ["test1@test.com", "test2@test.com"]

def test_parse_recipient_error():
    with pytest.raises(ValueError, match="recipient should be a string or a list of string"):
        EmailAlertingTool._parse_recipient([1, 2])

def test_validate_recipient():
    result = EmailAlertingTool._validate_recipient("test@test.com")
    assert result == None

def test_validate_recipient_ko():
    with pytest.raises(ValueError, match="Invalid email : "):
        result = EmailAlertingTool._validate_recipient("+33123456789")

def test_send_message(mocker, helper):

    # mock the smtplib.SMTP object
    mock_SMTP = mocker.MagicMock(name="reach4me.emailing.smtplib.SMTP")
    mocker.patch("reach4me.emailing.smtplib.SMTP", new=mock_SMTP)

    helper.send_message(to="recipient@test.com", msg="Hello World", subject= "You've got a mail" )

    assert mock_SMTP.return_value.__enter__.return_value.sendmail.call_count == 1

def test_send_message_fail(mocker, helper):
    # mock the smtplib.SMTP object
    mock_SMTP = mocker.MagicMock(name="reach4me.emailing.smtplib.SMTP")
    mocker.patch("reach4me.emailing.smtplib.SMTP", new=mock_SMTP)
    # mock STMPException error
    mock_SMTP.side_effect = smtplib.SMTPException

    with pytest.raises(smtplib.SMTPException):
        helper.send_message(to="recipient@test.com", msg="Hello World", subject= "You've got a mail" )
