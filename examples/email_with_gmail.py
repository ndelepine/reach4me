# coding: utf-8
from reach4me.emailing.gmail import GmailHelper
import os
from dotenv import load_dotenv
import sys
import logging


stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [stdout_handler]

logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)
    
if __name__ == "__main__":

    load_dotenv()

    # We create a GmailHelper instance with the required fields
    alerting_client = GmailHelper(sender=os.getenv("GMAIL_LOGIN", "sender@mail.com"), password=os.getenv("GMAIL_PASSWORD", "my_password"))

    # We use the helper to send an email
    alerting_client.send(to=os.getenv("GMAIL_RECIPIENT", "test-reach4me@reach4me.com"), msg="Hello World !", subject="You've got a mail")
               
    
