#####################
# Kevin Gu
# gukailia@msu.edu
# 2018-4-2
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

""""Given Sheet's name, delete it"""


def __main__():
    open_file_on_desktop('ex_1')
    pyautogui.PAUSE = 0.1

    pyautogui.hotkey('ctrl', 'g')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.typewrite('!A1')
    pyautogui.press('enter')

    pyautogui.press('alt')
    pyautogui.press('e')
    pyautogui.press('l')
    pyautogui.press('enter')


__main__()