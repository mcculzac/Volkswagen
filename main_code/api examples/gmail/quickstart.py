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

    print( 'Message snippet: %s' % message['snippet'])
    # print ( 'headers %s' % message['payload']['headers'])


    # attempt at sender email
    emailline = str(message['payload']['headers'])
    match = re.findall(r'[\w\.-]+@[\w\.-]+', emailline)
    print(match[1])


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

    print ('Message snippet: %s' % message['snippet'])

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


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

    # print only one id at index 0 of the emails in the inbox
    # print(service.users().messages().list(userId='me').execute()['messages'][0]['id'] , "here is one id")

    # run through amount of emails in inbox
    for id in range(amountofemails):
        emailidnum = service.users().messages().list(userId='me').execute()['messages'][id]['id']
        GetMessage(service, 'me', emailidnum)
    #     messages = service.users().messages().list(userId='me').execute()['messages']
    # messages = service.users().messages().list(userId='me', id='').execute()
    # print(messages)

    # GetMessage(service, 'me', '169a239282c01488')
    # GetMessage(service, 'me', '169a5b7c69c6b1f9')

    # mess age = service.users().messages().get( id='169a239282c01488').execute()

    # pr int('Message snippet: %s' % message['snippet'])

    # messages.get(format='metadata')

    # message = service.users().messages().get(userId=user_id, id='169a239282c01488').execute()

    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])

if __name__ == '__main__':
    main()