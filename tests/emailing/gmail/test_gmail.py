# coding: utf-8
from reach4me.emailing.gmail import GmailHelper
import pytest


@pytest.fixture(scope="function")
def helper():
    helper = GmailHelper(sender="test", password="pwd")
    yield helper


def test_creation(helper):

    assert helper.smtp_host == "smtp.gmail.com"
    assert helper.smtp_port == 587


def test_send_message(mocker, helper):

    # mock the smtplib.SMTP object
    mock_SMTP = mocker.MagicMock(name="reach4me.emailing.smtplib.SMTP")
    mocker.patch("reach4me.emailing.smtplib.SMTP", new=mock_SMTP)

    helper.send_message(
        to="recipient@test.com", msg="Hello World", subject="You've got a mail"
    )

    print(f"DEBUG: {mock_SMTP.return_value.__enter__.return_value.sendmail.call_count}")
    assert mock_SMTP.return_value.__enter__.return_value.sendmail.call_count == 1
