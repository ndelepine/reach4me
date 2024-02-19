# coding: utf-8

from typing import List
from reach4me import AlertingTool
import re

class SmsAlertingTool(AlertingTool):

    @classmethod
    def _validate_recipient(self, recipient: str | List[str]):
        """
        Function that verifies if the recipient of the SmsAlertingTool is of the right format

        Args:
            recipient (str | List[str]): The recipient to send the alert to

        Raises:
            ValueError: Raises an error if the value of the recipien is incorrect
        """
        rule = re.compile(r'\+[0-9]{11}')

        if isinstance(recipient,list) and all(isinstance(r, str) for r in recipient):
            for number in recipient:
                if not rule.search(number):
                    msg = f"Invalid mobile number : {number}"
                    raise ValueError(msg)
        elif isinstance(recipient, str):
            if not rule.search(recipient):
                msg = f"Invalid mobile number : {recipient}"
                raise ValueError(msg)
        else:
            raise ValueError("recipient should be a string of a list of string")
        
