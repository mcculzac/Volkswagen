

#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-18
#####################

# This will hold email based api tools


##########
# import
##########

from .logpyautogui import log
import pyautogui


############
# functions
############

def mac_email():
    """
    On a mac send an email using built in mail client. :)
    :return: 
    """
    pass


def windows_email(text: str, to: str, subject: str) -> None:
    """
    On a windows send an email using built in mail client. :)
    :param text: message body
    :param to: the to email address
    :param subject: email subject line
    :return: None
    """

    # get to run
    log(pyautogui.keyDown, ('win'))
    log(pyautogui.press, ('r'))
    log(pyautogui.keyUp, ('win'))

    # open outlook
    log(pyautogui.typewrite, ('outlook'))
    pyautogui.PAUSE = 7
    log(pyautogui.press, ('enter'))
    pyautogui.PAUSE = .5

    # new mail
    log(pyautogui.keyDown, ('ctrl'))
    log(pyautogui.press, ('n'))
    log(pyautogui.keyUp, ('ctrl'))

    # type in to, subject, message
    log(pyautogui.typewrite, (to))
    log(pyautogui.press, ('tab'))
    log(pyautogui.press, ('tab'))
    log(pyautogui.press, ('tab'))
    log(pyautogui.typewrite, (subject))
    log(pyautogui.press, ('tab'))
    log(pyautogui.typewrite, (text))

    # send
    log(pyautogui.keyDown, ('ctrl'))
    log(pyautogui.press, ('enter'))
    log(pyautogui.keyUp, ('ctrl'))
