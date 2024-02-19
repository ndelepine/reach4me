# coding: utf-8
from reach4me.emailing import EmailAlertingTool
import logging

logger = logging.getLogger('Alerting')


class GmailHelper(EmailAlertingTool):

    def __init__(self, sender: str, password: str, smtp_host: str = 'smtp.gmail.com', smtp_port:int = 587):
        """
        Creation of the login and password parameters to create the client property
        Args:
            login (str): The Gmail account
            password (str): The Gmail password
        """
        login = sender
        super().__init__(sender=sender, password= password, smtp_host=smtp_host, smtp_port=smtp_port, login=login)


