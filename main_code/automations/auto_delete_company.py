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

"""Given the company name, delete everything about the company contact information"""

def __main__():
    open_file_on_desktop('ex_1')
    pyautogui.PAUSE = 0.1

    goto_sheet('contact')

    pyautogui.hotkey('ctrl', 'f')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    pyautogui.press('esc')

    pyautogui.hotkey('ctrl', '-')
    pyautogui.press('down')
    pyautogui.press('enter')



__main__()