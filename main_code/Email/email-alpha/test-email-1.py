''' References:
Getting started with Authentication (GCP)
https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python

Set path
https://stackoverflow.com/questions/45501082/set-google-application-credentials-in-python-project-to-use-google-api
'''

import dialogflow
import pyautogui
import os

# set google authentication path (local to my machine currently!)
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'capstone-email-80a1e6748b8c.json'

# Specific name created on GCP
#project_id = 'capstone-email-231916'

#############################################
#
# Variables specifc for demo
#
#############################################
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'jokes-2a795-fce255f4dea7.json'
# filename = 'raw-text.txt'
# # ** test ** jokes agent on dialog flow
# project_id = 'jokes-2a795'
# # (random) Any string. Specifies conversation
# session_id = 'mock-session'
#
# # Agent input
# # text = "tell me a joke" #### getting this from text file instead
# language_code = 'en'

def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(response.query_result.intent.display_name, \
                                                          response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))
    return '{}\n'.format(response.query_result.fulfillment_text)


def get_text(filename):
    '''open a text file,
    get line of text and return it'''
    fp = open(filename)
    line = fp.readline().strip()
    return line

def open_word(response):
    '''uses pyautogui '''
    pyautogui.hotkey('command', 'space')
    pyautogui.typewrite('word')
    pyautogui.PAUSE = 2.5
    pyautogui.keyDown('enter')
    pyautogui.keyDown('enter')
    # pyautogui.typewrite('hello_world')
    pyautogui.typewrite(response)


def demo():
    # text file representing email
    filename = 'raw-text.txt'
    text = get_text(filename)

    # GCP Authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'jokes-2a795-fce255f4dea7.json'
    #jokes agent on dialog flow
    project_id = 'jokes-2a795'
    # (random) Any string. Specifies conversation
    session_id = 'mock-session'
    language_code = 'en'

    response = detect_intent_texts(project_id, session_id, text, language_code)
    open_word(response)

demo()


