#####################
# Kevin Gu
# gukailia@msu.edu
# 2018-3-21
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

"""Given an partID, return the open amount"""

def __main__():

    open_file_on_desktop('ex_1')
    pyautogui.PAUSE = 0.1

    pyautogui.hotkey('ctrl', 'f')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    pyautogui.press('esc')

    repeated_press('right', 7)

    read_cell()


__main__()