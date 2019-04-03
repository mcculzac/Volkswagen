from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


import base64
import email
import re
import dialogflow
import os


import clipboard as clip

from apiclient import errors




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

    # print( message['snippet'])


    # attempt at sender email
    emailline = str(message['payload']['headers'])
    match = re.findall(r'[\w\.-]+@[\w\.-]+', emailline)



    return message['snippet']
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


def detect_intent_texts(project_id, session_id, text_str, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)


    text_input = dialogflow.types.TextInput(text=text_str, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return '{}\n'.format(response.query_result.fulfillment_text)

##############################################

# Incomplete
def put_value_in_clipboard(value):
    '''parameter identified for task
    no return. Put value in clipboard'''

    # copy value to the clipboard
    # os.system("echo '%s' | pbcopy" % value)

    clip.copy(value)  # now the clipboard content will be the string value
    text = clip.paste()  # text will have the content of clipboard


    pass


# Incomplete
def take_action(action):
    '''execute task
    label (move) email upon task completion
    UnknownTask -> HumanAction
    All other tasks -> BotAction'''
    pass





################################################
def main():


    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    # GCP Authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vw-2019-cse498-dfea7d9a65a3.json'

    # agent on dialog flow
    project_id = 'vw-2019-cse498'

    # (random) Any string. Specifies conversation
    session_id = 'mock-session'
    language_code = 'en'


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


    # run through amount of emails in inbox
    for id in range(amountofemails):
        emailidnum = service.users().messages().list(userId='me').execute()['messages'][id]['id']

        # assigns body of email to text
        text = GetMessage(service, 'me', emailidnum)

        # send body of email to Dialogflow
        response = detect_intent_texts(project_id, session_id, text, language_code)


        # prints Dialogflow response
        print(response)


if __name__ == '__main__':
    main()