
###################
# Zac McCullough
# mccul157@msu.edu
# 1/28
###################

"""Read emails from account on outlook"""

##########
# imports
##########

from typing import List
import win32com.client


######################
# function definitions
######################

def connect_to_outlook() -> None:
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")


def get_all_emails_from(outlook, list_senders) -> List:
    inbox = outlook.GetDefaultFolder(6)
    messages = inbox.Items
    result = []
    for message in messages:
        sender = None
        try:
            sender = message.SenderEmailAddress
        except AttributeError as e:
            pass
        if sender is not None and sender.lower() in list_senders:
            result.append(message)
    return result


def __main__() -> None:
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    emails = get_all_emails_from(outlook, ['zam.mccullough@gmail.com'])
    print(len(emails))
    print(emails[0].body)


__main__()

