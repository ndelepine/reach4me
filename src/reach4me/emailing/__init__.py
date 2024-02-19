# coding: utf-8

from reach4me import AlertingTool
import re
from typing import List
import smtplib
from email.mime.text import MIMEText
import logging

logger = logging.getLogger('Alerting')


class EmailAlertingTool(AlertingTool):
    """
    Generic class of the email alerting tool
    """    
    
    def __init__(self, sender: str, smtp_host: str, smtp_port:int, login:str = None, password: str = None) -> None:
        super().__init__(sender=sender)
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.login = login
        self.password = password

    @classmethod
    def _parse_recipient(self, recipient: str | List[str]) -> None:
        """
        Function that parses the recipient into a list of dict expected by Gmail

        Args:
            recipient (str | List[str]): The recipients of the Email

        Raises :
            ValueError: Check if the recipient is a str of a list of str

        Returns:
            list: The list of dict of the recipients
        """        
        if isinstance(recipient, str):
            return [recipient]
        elif isinstance(recipient,list) and all(isinstance(r, str) for r in recipient):
            return recipient
        else:
            raise ValueError("recipient should be a string of a list of string")

    @classmethod  
    def _validate_recipient(self, recipient: str | List[str]):
        """
        Function that verifies if the recipient of the EmailAlertingTool is of the right format

        Args:
            recipient (str | List[str]): The recipient to send the alert to

        Raises:
            ValueError: Raises an error if the value of the recipien is incorrect
        """

        rule = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

        recipient = self._parse_recipient(recipient)

        for recipient in recipient:
            if not rule.search(recipient):
                msg = f"Invalid email : {recipient}"
                raise ValueError(msg)
        
    @property
    def client(self) -> dict:
        """
        Property that return the Gmail SMTP client

        Returns:
            Client: The Gmail Client
        """
        return {
            "login": self.login,
            "password": self.password
        }

            
    def send_message(self, to: str | List[str], msg: str, subject: str) -> None:
        """
        Method that send a message using the Gmail SMTP server

        Args:
            to (str | List[str]): Recipients of the message
            msg (str): Body of the message
        """        
        
        login = self.client["login"]
        password = self.client["password"]
        recipients = self._parse_recipient(to)

        msg = MIMEText(msg)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(recipients)
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp_server:
                smtp_server.starttls()
                if (login and password):
                    smtp_server.login(login, password)
                response = smtp_server.sendmail(self.sender, recipients, msg.as_string())
                # smtp_server.quit()
        except smtplib.SMTPException as e:
            logger.error("SMTP Exception. Email failed to send")
            raise(e)
        
        return response
