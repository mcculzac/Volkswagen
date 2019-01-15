

###################
# Zac McCullough
# mccul157@msu.edu
# 1/15
###################


###################
# imports
###################
import pyautogui
from typing import Tuple


###################
# function definitions
###################

def get_screen_dimensions() -> Tuple[float, float]:
    """
    get the screen dimensions
    :return: returns tuple of (width, height)
    """

    screen_width, screen_height = pyautogui.size()
    return screen_width, screen_height


def get_cursor_pos() -> Tuple[float, float]:
    """
    get current cursor position
    :return: returns tuple of (x value, y value)
    """

    cursor_x, cursor_y = pyautogui.position()
    return cursor_x, cursor_y


def check_if_cursor_pos_valid() -> bool:
    """
    check if cursor is outside of screen size
    :return: true if inside screen, false otherwise
    """

    cursor_x, cursor_y = get_cursor_pos()
    return pyautogui.onScreen(cursor_x, cursor_y)


def hello_world() -> type(None):
    """
    obv
    :return: None
    """

    pyautogui.typewrite('Hello world!', interval=0.25)


def mac_say_hello_world() -> type(None):
    """
    UNTESTED!!!
    Opens a terminal and runs the say command and then quits out
    :return: None
    """

    pyautogui.PAUSE = 1.0
    pyautogui.keyDown('command')
    pyautogui.press('space')
    pyautogui.keyUp('command')
    pyautogui.typewrite('terminal')
    pyautogui.PAUSE = 3.0
    pyautogui.press('enter')
    pyautogui.PAUSE = .5
    pyautogui.typewrite('say ', interval=.25)
    hello_world()
    pyautogui.press('enter', interval=.25)


def windows_echo_hello_world() -> type(None):
    """
    Opens a powershell, switchs to bash, then echos hello world
    :return: None
    """

    pyautogui.PAUSE = 1.0
    pyautogui.keyDown('win')
    pyautogui.press('r')
    pyautogui.keyUp('win')
    pyautogui.typewrite('powershell', interval=.25)
    pyautogui.PAUSE = 3.0
    pyautogui.press('enter')
    pyautogui.PAUSE = 1.0
    pyautogui.typewrite('bash', interval=.1)
    pyautogui.press('enter')
    pyautogui.PAUSE = .2
    pyautogui.typewrite('echo "')
    hello_world()
    pyautogui.typewrite('"')
    pyautogui.press('enter')


def __main__():
    windows_echo_hello_world()


__main__()
