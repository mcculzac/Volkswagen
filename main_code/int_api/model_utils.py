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


