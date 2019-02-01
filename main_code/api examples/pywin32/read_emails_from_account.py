
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


def get_all_capstone_emails(outlook) -> List:
    inbox = outlook.GetDefaultFolder(6)
    messages = inbox.Items
    result = []
    for message in messages:
        sender = None
        try:
            sender = message.SenderEmailAddress
        except AttributeError as e:
            pass
        if sender is not None and sender.lower() in ['james.mariani4@gmail.com', 'dyksen@msu.edu', 'john3842@msu.edu']:
            result.append(message)
    return result


def __main__() -> None:
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    emails = get_all_capstone_emails(outlook)
    print(len(emails))
    for email in emails:
        print(email.body[:30])
        print('********************')


__main__()

