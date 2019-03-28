
''' References:
Getting started with Authentication (GCP)
https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python
Set path
https://stackoverflow.com/questions/45501082/set-google-application-credentials-in-python-project-to-use-google-api
'''

import dialogflow
#import pyautogui
import os



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



def demo():

    text = 'Send reminder email to the supplier'


    # GCP Authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vw-2019-cse498-dfea7d9a65a3.json'

    #jokes agent on dialog flow
    project_id = 'vw-2019-cse498'

    # (random) Any string. Specifies conversation
    session_id = 'mock-session'
    language_code = 'en'

    response = detect_intent_texts(project_id, session_id, text, language_code)
    print(response)

demo()