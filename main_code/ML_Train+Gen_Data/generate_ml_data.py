###################
# Zac McCullough
# mccul157@msu.edu
# 2/01
###################

"""generate a csv file of click streams that can be parsed for ml"""

##########
# imports
##########

from typing import List
from pywinauto.win32_hooks import Hook, KeyboardEvent, MouseEvent
import logging


###################
# Global Variables
###################

NAME_OF_CSV_FILE = 'data.csv'


######################
# function definitions
######################

def on_event(args) -> None:
    """
    Event handler that is called every time an event occurs (SLOW!)
    :param args: our events
    :return: none
    """
    with open(NAME_OF_CSV_FILE, 'a') as f:
        if isinstance(args, KeyboardEvent) and args.event_type == 'key down':
            if args.current_key.lower() == 'return':
                f.write('\n')
            else:
                f.write(str(args.current_key) + ',')


def __main__() -> None:
    hook = Hook()
    hook.handler = on_event
    hook.hook(keyboard=True, mouse=True)
    hook.listen()


__main__()



