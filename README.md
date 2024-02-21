![Tests](https://ndelepine.github.io/reach4me/badges/tests.svg)
[![Coverage Status](https://ndelepine.github.io/reach4me/badges/coverage.svg)](https://ndelepine.github.io/reach4me/coverage_report/)
[![Flake8](https://ndelepine.github.io/reach4me/badges/flake8.svg)](https://ndelepine.github.io/reach4me/flake8/)


# reach4me

reach4me is a messaging Python library that combine different alerting tools to send messages with text.

It currently support sending emails through SMTP, and SMS through Twilio & Octopush.

It was design to be able to quickly send simple messages with different technologies, without having to implement tool-dedicated code.

## Table of contents
* [Installation](#installation)
* [Features](#features)
* [Usage](#usage)
   * [SMS](#sms)
      * [Twilio](#twilio)
      * [Octopush](#octopush)
   * [Email](#email)
      * [Gmail](#gmail)
* [Examples](#examples)
* [Caveats / FYI](#fyi)


## Installation <a name="installation"></a>
The library can be installed via pip:

> <code>pip install reach4me</code>: Standard installation, supporting Emails and Octopush SMS<br>
> <code>pip install reach4me[twilio]</code>: For usage with Twilio<br>

## Features <a name="features"></a>

* Generic classes for Email and SMS, so the user can implement his own connector if needed.
* Logging of sent messages and intermediary steps.
* Recipient validation : For each class, check that the recipient is provided in the expected format.
* Gmail : GmailHelper class to avoid setting the smtp host and port.
* Octopush: check if there is enough credits before sending the sms. Raise an InsufisantBalanceException otherwise.

## Usage <a name="usage"></a>

### SMS <a name="sms"></a>

Given that there is no standard way of sending sms, the generic class by itself cannot send SMS. 
<br>The user will have to either use the provided classes, or implement an inherited class on his own. 

The mandatory parameter is the sender of the message.

The generic class will automatically check that the recipient, or the list of recipients have a valid phone number format.
Otherwise, a ValueError exception will be raised.
</br>
<details>
<summary>Octopush<a name="octopush"></a></summary>
<br>

Uses the python `requests` library to perform calls on the official Octopush REST API. Needs a login and a token provided by Octopush when registering.
</details>

<details>
<summary>Twilio<a name="twilio"></a></summary>
<br>

Uses the official python `twilio` library to perform sms sending using the Twilio API. Needs an SID and a token provided by Twilio when registering.
</details>

---

### Email <a name="email"></a>

The generic class uses the python `smtp` library to send emails.

The mandatory parameters are the SMTP host and port, and the sender of the message.
The user can add a login and password if needed.

The generic class will automatically check that the recipient, or the list of recipients have a valid email format.
Otherwise, a ValueError exception will be raised.
</br>
<details>
<summary>Gmail<a name="gmail"></a></summary>
<br>

Uses the host `smtp.gmail.com` and the port `587` to send email. Since 30 may 2022, for the authentication to work, the user needs to generate and prodive an app password provided by Google. 
[Here](https://support.google.com/accounts/answer/185833?hl=en) is the official documentation on how to create an app password.
</details>

## Examples <a name="examples"></a>

An `examples` folder with examples is available :
<ul>
<li>
<a href="/examples/emailing/gmail.ipynb" target="_self">Gmail</a>: generic Gmail usage, importing the library, configuring the logger to write to the <cite>stdout</cite> and using environment variables via <cite>dotenv</cite> to instantiate the GmailHelper and send the mail.
</li>
<li>
<a href="/examples/sms/twilio.ipynb" target="_self">Twilio</a>: generic Twilio usage, importing the library, configuring the logger to write to the <cite>stdout</cite> and using environment variables via <cite>dotenv</cite> to instantiate the TwilioHelper and send the SMS.

The response of the API call is printed.
</li>
<li>
<a href="/examples/sms/octopush.ipynb" target="_self">Octopush</a>: generic Octopush usage, importing the library, configuring the logger to write to the <cite>stdout</cite> and using environment variables via <cite>dotenv</cite> to instantiate the OctopushHelper and send the SMS.

The response of the API call is printed, containing the remaining balance on the account.
</li>
</ul>

## Caveats / FYI <a name="fyi"></a>

<ul>
<li>
The <cite>send</cite> function returns the response returned after the message has been sent. Given that each messaging tool has it own response type and format, the handling of those responses is at the hand of the user for the moment.
The next version will implement the handling of those responses to handle any issue.
</li>
<br>
<li>
"Message-queue" tools like Kafka or RabbitMQ are intended to be integrated to this library in the future.
</li>
</ul>