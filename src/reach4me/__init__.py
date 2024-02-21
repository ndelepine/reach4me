# coding: utf-8

from abc import ABC, abstractmethod
from typing import List, Any
import logging


logger = logging.getLogger("Alerting")


class AlertingTool(ABC):

    sender: str

    def __init__(self, sender: str) -> None:
        self.sender = sender

    @abstractmethod
    def _validate_recipient(self, recipient: str | List[str]):
        """
        Function that verifies if the recipient of the AlertingTool is of the right format

        Args:
            recipient (str | List[str]): The recipient to send the alert to
        """

    @property
    @abstractmethod
    def client(self) -> Any:
        """
        Property. The client that will be used to send the message

        Returns:
            Any: The client. Could be of any kind (e.g Twilio client, dict, ...)
        """

    @abstractmethod
    def send_message(self, to: str | List[str], msg: str, *args, **kwargs) -> None:
        """
        Function that sends a message to a given recipient or list of recipients.

        Args:
            to (str | List[str]): The recipient or the list of recipients to send the message to
            msg (str): The content of the message
        """

    def send(self, to: str | List[str], msg: str, *args, **kwargs) -> Any:
        """
        Function that runs the sending process pipeline.
        It validates the reciepient, send the message and handle the response

        Args:
            to (str | List[str]): The recipient of the message
            msg (str): The message

        Returns:
            Any: The sending process response
        """
        self._validate_recipient(recipient=to)
        logger.info(f"Sending alert with {self.__class__} to {to}")
        response = self.send_message(msg=msg, to=to, *args, **kwargs)
        logger.debug(f"Message was sent with response : {response}")
        return response
