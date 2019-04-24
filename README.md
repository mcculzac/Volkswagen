# Volkswagen Cognitive Enterprise Software Robots

Welcome to the landing page for our project.

We are applying machine learning and NLP techniques to aid in automating the business process, decreasing labor time on repetitive manual tasks, increasing productivity and boosting operational speeds.

## Project Description
The design of the cognitive enterprise software robot focuses on analyzing data of file and sending and receiving emails. This robot is able to do manual tasks that a person is performing to parse data, do simple calculation, send an email to specific people, and make decision based on the email it gets back.

## Technical Components 

Our project is built on python under windows environment. In order to run the scripts, you need to have a windows device and install python 3.6 and specific python libraries.

* Hardware
    * Windows
* Software
    * Python 3.6
* Python libraries list
    * tensorflow
    * keras
    * sklearn
    * numpy
    * pyautogui
    * pywinauto
    * pywin32
    * dialogflow
    * os
    * google-api-python-client
    * google-auth-oauthlib
    * google-auth
    

## System Arc
![alt text](https://raw.githubusercontent.com/mcculzac/Volkswagen/kg_doc/Resources/Untitled.png)






## How the process flow
1. Parsing the email with Dialogflow.

        python3.6 main_code/Parsing_email/quickstart.py
2. Identify the task ID and extract the useful information.
3. Input the task ID and with necessary information to the python script. 
4. The bot will apply different models to work on the different tasks.
        
        python3.6 main_code/Email/inbox-dialogflow.py


## How Dialogflow works
Dialogflow lets the user build conversational interfaces by providing a powerful natural language understanding (NLU) engine. In Dialogflow, a user can create agents (NLU modules) that are able to understand human language and translate it to standard and structured meaning that other apps and services can understand.

In this project, an agent is created that includes an intent for each different task related to emails in the inbox. In each intent, some examples of what an email can say are provided in order to match a particular intent. However, there is no need to define every possible example of what an email might say because of Dialogflow's built-in machine learning, which naturally expands training phrases to other similar emails. The agent parses each email and if the intent of an email matches an intent within the agent, it outputs the task related to that email and the information that the softbot will need to handle that task.


## Training the model
Currently we are automating some simple tasks to generate the data for training the model. All the automation samples are located in the *automations* folder.

By running the script gather_data, every click will be recorded and store in a cvs file.
And by running the script clean_data, it will clean up the unclean data.

    python3.6 main_code/master_scripts/gather_data.py
    python3.6 main_code/master_scripts/clean_data.py
       
Once we have clean data, then we can run the script model_rnn.py to train a model.

    python3.6 main_code/models/model_rnn.py

With the model we trained, we can run it and test it with scripts run_model.py and test_model.py.

    python3.6 main_code/models/test_model.py
    python3.6 main_code/models/run_model.py
 
 


## Authors
* [Amelia Wilson](https://github.com/ameliawilson) - *NPL* 
* [Fynn Reckhorn](https://github.com/freckhorn) - *GmailAPI*
* [Kevin Gu](https://github.com/KailiangGu) - *Data*
* [Maryam Irannejad Najafabadi](https://github.com/Irannejad) - *NPL*
* [Zachary McCullough](https://github.com/mcculzac) - *ML Model*






