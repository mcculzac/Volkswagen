#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-18
#####################

"""holds generic api tools"""

##########
# imports
##########

import platform
import time
import typing


############
# functions
############

def get_os() -> str:
    """
    Gets the OS and returns 'windows' 'mac' or 'linux'
    :return:
    """
    os = platform.system()
    if os == 'Windows':
        return 'windows'
    elif os == 'Linux':
        return 'linux'
    elif os == 'Darwin':
        return 'mac'


def now() -> str:
    """
    Returns the current Hour:Minute:Second
    :return: current time string
    """
    return time.strftime("%H:%M:%S", time.gmtime())

