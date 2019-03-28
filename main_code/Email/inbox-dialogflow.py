''' References:
Getting started with Authentication (GCP)
https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python
Set path
https://stackoverflow.com/questions/45501082/set-google-application-credentials-in-python-project-to-use-google-api
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

import dialogflow
import os


# Complete in DialogFlow
"""Given an partID, return the open amount""" # CheckOpenAmount auto_check_open.py

# Tasks in Progress
"""Given the company name, return the part name their provided""" # PartNameFromCompany auto_get_part_name_2.py
"""Given the partID, return the email of the supplier""" # GetContactEmail auto_get_email.py

# Tasks to handle in DF
""""Given Company's name, return the partID they provide """ # auto_get_partID.py
"""Given the partID, return the part name""" # auto_get_part_name_1.py
"""Given company's name, return the partID""" # GetPartID auto_get_company_name.py
"""Given any column name, delete it""" # DeleteColumn auto_delete_col.py
"""Given the company name, delete everything about the company contact information""" # RemoveCompany auto_delete_company.py
"""Given the company name, delete the contact information""" # DeleteContact auto_delete_company_email.py


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    print( message['snippet'])


    # attempt at sender email
    emailline = str(message['payload']['headers'])
    match = re.findall(r'[\w\.-]+@[\w\.-]+', emailline)



    return message
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


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)


    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return '{}\n'.format(response.query_result.fulfillment_text)


def dialogflow_response(text):
    '''text: string from email body
    return: detected task name from dialog flow'''
    # GCP Authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vw-2019-cse498-dfea7d9a65a3.json'

    #jokes agent on dialog flow
    project_id = 'vw-2019-cse498'

    # (random) Any string. Specifies conversation
    session_id = 'mock-session'
    language_code = 'en'

    response = detect_intent_texts(project_id, session_id, text, language_code)
    return response


# Incomplete
def put_value_in_clipboard(value):
    '''parameter identified for task
    no return. Put value in clipboard'''
    pass


# Incomplete
def take_action(action):
    '''execute task
    label (move) email upon task completion
    UnknownTask -> HumanAction
    All other tasks -> BotAction'''
    pass


def get_action(task):
    '''returns action identified
    put parameter in clipboard if applicable'''

    param = False
    task_information = task.split()
    action = task_information[0]
    if len(task_information) > 1:
        param = True
        value = task_information[1]

    if param:
        put_value_in_clipboard(value)

    return action

# Incomplete
def add_label():
    '''label email appropriately'''
    pass
  
def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
    amountofemails = len(service.users().messages().list(userId='me').execute()['messages'])


    count = 0
    # run through amount of emails in inbox
    for id in range(amountofemails):
        count += 1
        emailidnum = service.users().messages().list(userId='me').execute()['messages'][id]['id']
        # returns dictionary. key = 'snippet'; vlaue = message
        message = GetMessage(service, 'me', emailidnum)['snippet']


        # label testing - add a label to the first messgae
        if count == 2:
            add_label()


        task_name = dialogflow_response(message).strip()
        #print(task_name)
        if task_name:
            action = get_action(task_name)
            print("action:", action)
            take_action(action)
        else:
            print("No response detected from dialogflow")

        print()

if __name__ == '__main__':
    main()
