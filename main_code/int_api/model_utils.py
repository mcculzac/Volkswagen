#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-3-22
#####################

"""
This contains various functions that are useful for model generation and data manipulation
"""

##########
# imports
##########

from .logpyautogui import log
import typing as t

########################
# function definitions
########################


def generate_char_to_int_dict(data: t.List[str]) -> t.Dict[str, int]:
    """
    Takes in the data and provide a dictionary that maps all strings in it to an int
    :param data: List[str] that is the data
    :return: Dict[int] that maps strings to ints
    """
    temp = set(data)
    return {x: i for i, x in enumerate(temp)}


def convert_pywinauto_pyautogui(key: str) -> str:
    """
    Takes in a pywinauto key and converts it to a pyautogui key
    :param key: string
    :return: string
    """
    replaces = [('Lwin', 'win'), ('Lalt', 'alt'), ('Rwin', 'win'), ('Oem_Minus', '-'), ('Lcontrol', 'ctrl'),
                ('Rcontrol', 'ctrl'), ('Lshift', 'shift')]
    for char in replaces:
        if char[0] == key:
            return char[1]
    return key
