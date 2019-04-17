#####################
# Kevin Gu
# gukailia@msu.edu
# 2018-4-15
#####################


##################
# import
##################

import sys

sys.path.append('../')
from int_api import *
import pyautogui


###############
# function defs
###############

""""Given Company's name, return the partID they provide """


def __main__():
    open_file_on_desktop('wifi_password')
    pyautogui.PAUSE = 0.1


    pyautogui.hotkey('ctrl', 'f')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    pyautogui.press('esc')

    pyautogui.press('right')

    read_cell()


__main__()