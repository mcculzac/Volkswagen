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
1. Parsing the email will Dialogflow.

        python3.6 whatever file does it
2. Identify the task ID and extract the useful information.
3. Input the task ID and with necessary information to the python script. 
4. The bot will apply different models to work on the different tasks.
        
        python3.6 whatever file does it
.....

## How Dialogflow works
Dialogflow is a Google service.

## Training the model
Currently we are automating some simple tasks to generate the data for training the model. All the automation samples are located in the *automations* folder.

By running the script generate_ml_data, every click will be recorded and store in a cvs file.

    python3.6 main_code/ML_Train+Gen_Data/generate_ml_data
       
*Need explain how we use the data we recorded to train the modle* 


## Authors
* [Amelia Wilson](https://github.com/ameliawilson) - *NPL* 
* [Fynn Reckhorn]() - *GmailAPI*
* [Kevin Gu](https://github.com/KailiangGu) - *Data*
* [Maryam Irannejad Najafabadi](https://github.com/Irannejad) - *NPL*
* [Zachary McCullough](https://github.com/mcculzac) - *ML Model*




## Acknowledgments 

