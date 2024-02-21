from reach4me import AlertingTool
from reach4me.emailing import EmailAlertingTool
from typing import List


def alert(client: AlertingTool, to: str | List[str]):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)

            # Add metadata to the message
            if isinstance(client, EmailAlertingTool):
                msg = f"{result}"
                subject = (
                    f"Automatic mail from func {function.__class__}.{function.__name__}"
                )
                client.send(msg=msg, to=to, subject=subject)
            else:
                msg = f"Automatic sms from func {function.__module__}.{function.__name__} : {result}"
                client.send(msg=msg, to=to)

            return result

        return wrapper

    return decorator
