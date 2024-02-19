# coding: utf-8
from typing import List
from reach4me.sms import SmsAlertingTool
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.rest.api.v2010.account.message import MessageInstance


class TwilioHelper(SmsAlertingTool):

    def __init__(self, sender: str, sid: str, token: str):
        """
        Creation of the sid and token parameters to create the client property
        Args:
            sid (str): The SID of the Twilio account
            token (str): The secret token of the Twilio account
        """
        super().__init__(sender=sender)
        self.sid = sid
        self.token = token

    @property
    def client(self) -> Client:
        """
        Property that return the Twilio Client

        Returns:
            Client: The Twilio Client
        """
        return Client(self.sid, self.token)

    def send_message(self, to: str | List[str], msg: str) -> MessageInstance:
        """
        Method that send a message using the Twilio Client

        Args:
            to (str | List[str]): Recipients of the message
            msg (str): Body of the message
        """

        try:
            # Send the message
            response = self.client.messages \
                .create(
                    body=msg,
                    from_=self.sender,
                    to=to
                )
            return response

        except TwilioRestException as e:
            raise e
