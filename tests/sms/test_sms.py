# coding: utf-8
from reach4me.sms import SmsAlertingTool
import pytest


@pytest.fixture(scope="function")
def helper():
    helper = SmsAlertingTool(sender="sender")
    yield helper


def test_validate_recipient_str():
    result = SmsAlertingTool._validate_recipient(recipient="+33123456789")
    assert result == None


def test_validate_recipient_list():
    result = SmsAlertingTool._validate_recipient(recipient=["+33123456789"])
    assert result == None


def test_validate_recipient_str_ko():
    with pytest.raises(ValueError, match="Invalid mobile number : "):
        SmsAlertingTool._validate_recipient("test@test.com")


def test_validate_recipient_list_ko():
    with pytest.raises(ValueError, match="Invalid mobile number : "):
        SmsAlertingTool._validate_recipient(["test1@test.com", "test2@test.com"])


def test_validate_recipient_error():
    with pytest.raises(
        ValueError, match="recipient should be a string or a list of string"
    ):
        SmsAlertingTool._validate_recipient([1, 2])
