'''
Two credential files required. For dialogflow & Gmail

References:
Getting started with Authentication (GCP)
https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python

Set path
https://stackoverflow.com/questions/45501082/set-google-application-credentials-in-python-project-to-use-google-api

Gmail API SCOPES https://developers.google.com/gmail/api/auth/scopes
'''

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


import base64
import email
import re
from apiclient import errors
from email.mime.text import MIMEText

import win32clipboard
import dialogflow
import os
import sys
sys.path.append('../automations')


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/'] # full access to the email account


def test_automations():
    '''This function is for testing automations. No input; no return.

    Choose task string from exmaple_task. This represents a mock response from dialogflow
    The value from the spreadsheet is placed in the clipboard

    PartNameFromCompany   Given the company name, return the part name their provided    auto_get_part_name_2.py
    GetContactEmail       Given the partID, return the email of the supplier    auto_get_email.py
    PartNameFromId        Given the partID, return the part name    auto_get_part_name_1.py
    PartIdFromCompany     Given Company's name, return the partID they provide    auto_get_partID.py

    '''
    example_tasks = ["PartNameFromCompany A++","GetContactEmail GERTB125", "PartNameFromId 0988FHG2", "PartIdFromCompany RocketScience"]
    expected_values_from_spreadsheet = ["Haltegriff Pl", "wils1170@msu.edu", "Gear", "GERTB125"]

    action = get_action(example_tasks[3])
    print(action)
    take_action(action)


def ModifyMessage(service, user_id, msg_id, msg_labels):
  """Modify the Labels on the given Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The id of the message required.
    msg_labels: The change in labels.

  Returns:
    Modified message, containing updated labelIds, id and threadId.
  """
  try:
    message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                body=msg_labels).execute()

    label_ids = message['labelIds']

    print( 'Message ID: %s - With Label IDs %s' % (msg_id, label_ids))
    return message
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message. the sender email
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    print( message['snippet'])



    # attempt at sender email
    emailline = str(message['payload']['headers'])
    match = re.findall(r'[\w\.-]+@[\w\.-]+', emailline)
    print("Message sender: " , match[1])
    print("Message Id : ", message['id'])

    return message['snippet'], match[1], message['id']
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()


    print(message['snippet'])

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


def detect_intent_texts(project_id, session_id, text, language_code = 'en'):
    """
    project_id (string): agent specific ID
    session_id (string): any string. indicates same conversation
    text (string): text to process
    language_code (string): english by default

    Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return '{}\n'.format(response.query_result.fulfillment_text)


def dialogflow_response(text):
    '''text (string): message from email body
    return (string): dialogflow response, detected task name'''

    # GCP Authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vw-2019-cse498-dfea7d9a65a3.json'

    #agent on dialog flow
    project_id = 'vw-2019-cse498'

    # session_id can be any string. Specifies conversation
    session_id = 'mock-session'
    language_code = 'en'

    response = detect_intent_texts(project_id, session_id, text, language_code)
    return response


def put_value_in_clipboard(value):
    '''value (string)
    parameter identified for task
    no return. Copy value to clipboard'''
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(value)
    win32clipboard.CloseClipboard()


def get_value_from_clipboard():
    '''returns string
    paste from clipboard'''
    win32clipboard.OpenClipboard()
    v = win32clipboard.GetClipboardData()
    return v


def take_action(action):
    '''execute task
    return label for email

    UnknownTask -> HumanAction
    All other tasks -> BotAction'''
    label = "BotAction"
    if action == "CheckOpenAmount":
        # this automation doesn't work import auto_check_open
        label = "HumanAction"
    elif action == "PartNameFromCompany":
        import auto_get_part_name_2
    elif action == "GetContactEmail":
        import auto_get_email
    elif action == "PartNameFromId":
        import auto_get_part_name_1
    elif action == "PartIdFromCompany":
        import auto_get_partID
    else:
        label = "HumanAction"

    return label


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_action_and_value(task):
    '''
    task (string): response from dialogflow. Extract the task name and value
    returns action identified
    put parameter in clipboard if applicable'''

    param = False
    value = ''
    task_information = task.split()
    action = task_information[0]
    if len(task_information) > 1:
        param = True
        if len(task_information) == 2:
            value = task_information[1]
        else:
            value = " ".join(task_information[1:])

    if param:
        put_value_in_clipboard(value)

    return action, value


def generate_message(task_name, value, return_value):
    '''returns task specific email body for reply email.
    if task is not known, return the value from the excell sheet'''
    message = return_value

    if task_name == "PartNameFromCompany":
        message = "The company {} provides the {} part.".format(value, return_value)
    if task_name == "GetContactEmail":
        message = "The supplier that provides part # {}, has the email {}.".format(value, return_value)
    if task_name == "PartNameFromId":
        message = "The part # {} is named {}.".format(value, return_value)
    if task_name == "PartIdFromCompany":
        message = "The company {} provides the part # {}.".format(value, return_value)

    return message

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is created
    # automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    # grab number of emails in inbox
    amountofemails = len(service.users().messages().list(userId='me', labelIds ='INBOX').execute()['messages'])
    # run through amount of emails in inbox
    for id in range(amountofemails):

        emailidnum = service.users().messages().list(userId='me', labelIds='INBOX').execute()['messages'][id]['id']
        # returns dictionary. key = 'snippet'; vlaue = message
        message, SenderEmail, ID = GetMessage(service, 'me', emailidnum)#['snippet']

        label = ''
        if message:
            task_name = dialogflow_response(message).strip()
            print("Dialogflow Response:", task_name)
            if task_name:
                action, original_value = get_action_and_value(task_name)              # action: string. example PartNameFromCompany
                print("action:", action)
                label = take_action(action)                 # label: string. Either "BotAction" or "HumanAction"
            else:
                label = "HumanAction"
                print("No response detected from dialogflow")
            print("Label:", label)


        if label == "HumanAction":
            ModifyMessage(service, 'me', ID, {'removeLabelIds': [], 'addLabelIds': ['UNREAD', 'Label_4305813264263189376']})

        elif label == "BotAction":
            BotEmail = 'wvcapstone2019@gmail.com'
            clipboard_value = get_value_from_clipboard()
            message_text = generate_message(action, original_value, clipboard_value)
            subject = task_name
            # An object containing a base64url encoded email object.
            # create_message(sender, to, subject, message_text)
            new_email_object = create_message(BotEmail, SenderEmail, subject, message_text)
            send_message(service, 'me', new_email_object)
            ModifyMessage(service, 'me', ID, {'removeLabelIds': ['UNREAD'], 'addLabelIds': ['Label_719760134209923963']})

        print()


if __name__ == '__main__':
    main()
    #test_automations()