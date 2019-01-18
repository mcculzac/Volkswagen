
#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-18
#####################

"""The idea of this file is to for almost very pyautogui command, log what it does into our file, and then return/
run it normally. Note that some functions have outputs and some do not."""

import sys
sys.path.insert(1, "/Users/zam/PycharmProjects/Volkswagen_git/main_code/Case_1/Attempt2/tools")
import pyautogui
import logging
import generic
# functions


def log(func, *args, **kwargs):
    temp = func(*args, **kwargs)
    if temp is None:
        logging.info(generic.now() + ',' + func.__name__ + ',')
    else:
        logging.info(generic.now() + ',' + func.__name__ + ','+str(temp))
#
# def position():
#     """
#     Logs and runs pyautogui position
#     :return: pyautogui.position()
#     """
#
#     temp = pyautogui.position()
#     logging.info(generic.now() + ',get_cursor_pos,' + str(temp))
#     return temp
#
# def keyDown():
#     pass
#
# def keyup():
#     pass
#
logging.basicConfig(filename='bot.log', level=logging.DEBUG)
log(pyautogui.position)
log(pyautogui.moveTo, 100, 100, duration=1)