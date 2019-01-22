#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-18
#####################

<<<<<<< HEAD
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
=======
# holds generic api tools

# imports

import platform
import time

# functions


def get_os():
>>>>>>> 0175285c77db5401156883bd6e631440b26aca37
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


<<<<<<< HEAD
def now() -> str:
    """
    Returns the current Hour:Minute:Second
    :return: current time string
    """
    return time.strftime("%H:%M:%S", time.gmtime())

=======
def now():

    return time.strftime("%H:%M:%S", time.gmtime())
>>>>>>> 0175285c77db5401156883bd6e631440b26aca37
