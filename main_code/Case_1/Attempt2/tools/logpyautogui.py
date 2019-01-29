
#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-18
#####################

"""The idea of this file is to for almost very pyautogui command, log what it does into our file, and then return/
run it normally. Note that some functions have outputs and some do not."""

##########
# imports
##########

import logging
from .generic import now


###########
# functions
###########

def log(func, *args, **kwargs):
    temp = func(*args, **kwargs)
    arg_list = []
    for arg in kwargs.keys():
        arg_list.append((arg, str(kwargs[arg])))
    arg_list.extend(args)
    if temp is None:
        logging.info(now() + ',' + func.__name__ + ',' + str(arg_list))
    else:
        logging.info(now() + ',' + func.__name__ + ',' + str(arg_list) + ',' + str(temp))
    return temp


