#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-28
# TESTING
#####################

"""Just a testing file to check various functions in api"""

##########
# imports
##########

import logging
from tools import open_file_on_desktop
from tools import windows_email
import wx
import keyboard


##############
# Function def
##############

def __main__() -> None:
    logging.basicConfig(filename='bot.log', level=logging.DEBUG)
    # open_file_on_desktop('Iron Man.m4v')
    # windows_email('this is a body', 'zam.mccullough@gmail.com', 'this is a subject')
    print(type(wx.TheClipboard))
    recorded = keyboard.record(until='esc')
    print(recorded)



__main__()
