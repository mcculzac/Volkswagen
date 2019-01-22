#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-18
#####################

##########
# imports
##########

from .logpyautogui import log
import pyautogui


########################
# function definitions
########################

def open_file_on_desktop(filename: str) -> None:
    """
    opens a file that lives on the desktop
    :param filename:
    :return:
    """

    pyautogui.PAUSE = .5
    log(pyautogui.hotkey, 'win', 'e')
    log(pyautogui.hotkey, 'ctrl', 'f')
    log(pyautogui.press, 'tab')
    log(pyautogui.press, 'down')
    log(pyautogui.press, 'enter')
    log(pyautogui.press, 'tab')
    log(pyautogui.hotkey, 'ctrl', 'f')
    pyautogui.PAUSE = 2
    log(pyautogui.typewrite, filename, interval=.25)
    pyautogui.PAUSE = .25
    log(pyautogui.press, 'tab')
    log(pyautogui.press, 'tab')
    log(pyautogui.press, 'space')
    pyautogui.PAUSE = 5
    log(pyautogui.press, 'enter')



