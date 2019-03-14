
#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-26
#####################

##########
# imports
##########

import typing
from .logpyautogui import log
import pyautogui


############
# functions
############


def repeated_press(key: str, times: int) -> None:
    pyautogui.PAUSE = .1
    for i in range(times):
        log(pyautogui.press, key)


