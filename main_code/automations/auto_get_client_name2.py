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

""""Given part's name, get client's name"""


def __main__():
    open_file_on_desktop('ex_1')
    pyautogui.PAUSE = 0.1

    goto_sheet('Warehouse')

    pyautogui.hotkey('ctrl', 'f')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    pyautogui.press('esc')

    pyautogui.press('left')
    read_cell()

    goto_sheet('Contact')

    pyautogui.hotkey('ctrl', 'f')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    pyautogui.press('esc')

    repeated_press('right', 5)
    pyautogui.typewrite("=CONCATENATE(")
    repeated_press('left', 3)
    pyautogui.typewrite('," ",')
    repeated_press('left', 2)
    pyautogui.typewrite(')')
    pyautogui.press('enter')
    pyautogui.press('up')

    read_cell()




__main__()