# coding: utf-8
from typing import List
from reach4me.sms import SmsAlertingTool
import requests
import json
import logging
from math import ceil

logger = logging.getLogger('Octopush')

API_ROOT = "https://api.octopush.com/v1/public/"
BALANCE_PATH = "wallet/check-balance"
SMS_PATH = "multi-channel/send"

SMS_DEFAULT_PRICE_CENTS = 10

class InsuffisantBalanceException(Exception):
    pass

class OctopushHelper(SmsAlertingTool):

    
    def __init__(self, sender: str, login: str, token: str, sms_price_cents: int = SMS_DEFAULT_PRICE_CENTS):
        """
        Creation of the sid and token parameters to create the client property
        Args:
            sid (str): The SID of the Twilio account
            token (str): The secret token of the Twilio account
        """
        super().__init__(sender=sender)
        self.login = login
        self.token = token
        self.sms_price_cents = sms_price_cents

    @property
    def client(self) -> dict:
        """
        Property that return the Octopush Client

        Returns:
            Client: The Octopush Client
        """
        return {
            "Content-Type": "application/json",
            "api-login": self.login,
            "api-key": self.token
        }
    
    def _get_balance(self) -> float:
        """
        Function that returns the Octopush account balance

        Raises:
            Exception: Error message

        Returns:
            float: The account balance
        """        

        try:
            balance = requests.get(API_ROOT + BALANCE_PATH, headers=self.client)
            balance.raise_for_status()
            return balance.json()["amount"]*100
        
        except requests.HTTPError as e:
            raise e
        
    @classmethod
    def _parse_recipient(cls, recipient: str | List[str]) -> list:
        """
        Function that parses the recipient into a list of dict expected by Octopush API

        Args:
            recipient (str | List[str]): The recipients of the SMS

        Raises:
            ValueError: Check if the recipient is a str or a list of str

        Returns:
            list: The list of dict of the recipients
        """        
        if isinstance(recipient, str):
            return [{"phone_number" : recipient}]
        elif isinstance(recipient,list) and all(isinstance(r, str) for r in recipient):
            return [{"phone_number": number} for number in recipient]
        else:
            raise ValueError("recipient should be a string or a list of string")
            
    def send_message(self, to: str | List[str], msg: str) -> requests.Response:
        """
        Method that send a message using the Octopush Client

        Args:
            to (str | List[str]): Recipients of the message
            msg (str): Body of the message
        """        
        
        # Check if the balance allows to send an sms :
        remaining_credit = self._get_balance()
        logger.info(f"You balance is of {remaining_credit} cents")
        
        msg_price = ceil(len(msg)/160)* self.sms_price_cents
        logger.info(f"The sms will cost {msg_price:.2f} cents")

        if remaining_credit<=msg_price:
            raise InsuffisantBalanceException(f"No enough credit : your balance is {remaining_credit:.2f}cts, and the sms will cost {msg_price:.2f}cts")

        try:
            data = {
                "channel": "sms",
                "recipients": self._parse_recipient(to),
                "text": msg,
                "metadata": {
                    "type": "sms_premium",
                    "sender": self.sender,
                    "purpose": "alert"
                }
            }

            response = requests.post(API_ROOT + SMS_PATH, headers=self.client, data=json.dumps(data))

            return response
        
        except requests.HTTPError as e:
            raise(e)