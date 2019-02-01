###################
# Zac McCullough
# mccul157@msu.edu
# 2/01
###################

"""Log inputs"""

##########
# imports
##########

from typing import List
from pywinauto.win32_hooks import Hook, KeyboardEvent, MouseEvent
import logging


###################
# Global Variables
###################

NAME_OF_LOG_FILE = 'inputs.log'


######################
# function definitions
######################

def on_event(args) -> None:
    """
    Event handler that is called every time an event occurs (SLOW!)
    :param args: our events
    :return: none
    """
    if isinstance(args, KeyboardEvent):
        logging.info("Key Pressed: " + str(args.current_key))
        if args.current_key == 'Escape':
            hook.unhook_mouse()
            hook.unhook_keyboard()
    elif isinstance(args, MouseEvent):
        logging.info("Mouse: " + str(args.current_key) + " at x: " + str(args.mouse_x) + " y: " + str(args.mouse_y))


def __main__() -> None:
    logging.basicConfig(filename=NAME_OF_LOG_FILE, level=logging.DEBUG)
    hook = Hook()
    hook.handler = on_event
    hook.hook(keyboard=True, mouse=True)
    hook.listen()


__main__()



