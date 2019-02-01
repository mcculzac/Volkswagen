#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-25
#####################

"""This is an attempt on the first task given"""

##########
# imports
##########

from tools import open_file_on_desktop
from tools import get__spreadsheet_data
from tools import windows_email
from tools import goto_cell, goto_sheet, create_sheet, delete_cols, goto_term, read_cell
from tools import log, repeated_press
from typing import List, Any
import datetime
from dateutil import parser
import pandas as pd
import pyautogui
import logging


##################
# global variables
##################

NAME_OF_FILE_TO_OPEN = 'ex_1.xlsx'
NAME_OF_LOG_FILE = 'bot.log'


####################
# class definitions
####################


######################
# function definitions
######################

def create_date_col() -> None:
    pyautogui.PAUSE = .11
    goto_term('date')
    log(pyautogui.hotkey, 'ctrl', 'space')
    log(pyautogui.hotkey, 'ctrl', 'c')
    goto_cell('a', 1)
    log(pyautogui.hotkey, 'ctrl', 'v')
    log(pyautogui.press, 'up')
    log(pyautogui.press, 'del')
    log(pyautogui.typewrite, 'cust_date')
    log(pyautogui.press, 'enter')
    log(pyautogui.hotkey, 'ctrl', '`')


def item_count() -> None:
    pyautogui.PAUSE = .1
    goto_cell('d', 1)
    log(pyautogui.typewrite, '=COUNTA(A2:A10000)', interval=.1)
    log(pyautogui.press, 'enter')


def create_today_col() -> None:
    pyautogui.PAUSE = .1
    goto_cell('c', 1)
    log(pyautogui.typewrite, 'today', interval=.1)
    log(pyautogui.press, 'enter')
    goto_cell('d', 1)
    num_items = int(read_cell())
    goto_cell('c', 2)
    # insert today's date and go down a lot
    for i in range(num_items):
        log(pyautogui.hotkey, 'ctrl', ';')
        log(pyautogui.press, 'enter')


def create_date_dif_col() -> None:
    pyautogui.PAUSE = .1
    goto_cell('b', 1)
    log(pyautogui.typewrite, 'date_dif', interval=.1)
    log(pyautogui.press, 'enter')
    goto_cell('d', 1)
    num_items = int(read_cell())
    goto_cell('b', 2)
    # get date difference
    for i in range(num_items):
        log(pyautogui.typewrite, '=A{i}-C{i}'.format(i=i+1))
        log(pyautogui.press, 'enter')


def get_data() -> List[str]:
    """
    Gets data from spreadsheet and returns in list format
    :return: data = [part_id, date, amount, open]
    """

    data = []
    data.append(read_cell())
    log(pyautogui.press, ('right'))
    data.append(read_cell())
    log(pyautogui.press, ('right'))
    data.append(read_cell())
    log(pyautogui.press, ('right'))
    data.append(read_cell())
    return data


def send_email(data_list: List[str], email_to: str) -> None:
    subject = 'AUTOMATED: Order Not In Yet!'
    static_email_text = '''
            Hello,
            \tThis is an automated email reminder about ordering part {part_id}.  At this time only {amount} parts have\
             been recieved and {open} parts are currently on route.  \
             The deadline is {date}.'''.format(open=data_list[3],
                                               part_id=data_list[0], amount=data_list[2], date=data_list[1])
    windows_email(static_email_text, email_to, subject)
    pyautogui.PAUSE = 2
    log(pyautogui.hotkey, 'alt', 'tab')


def get_email_address(part_id: str) -> str:
    goto_term(part_id)
    repeated_press('right', 4)
    return read_cell()


def process()->int:
    date_dif = read_cell()
    temp = None
    try:
        temp = int(date_dif)
    except Exception as e:
        return -1
    if type(temp) is int:
        if temp < 5:
            repeated_press('right', 8)
            open_val = read_cell()
            open_int = None
            try:
                open_int = int(open_val)
            except Exception as e:
                return -1
            if type(open_int) is int:
                if open_int >= 0:
                    repeated_press('left', 5)
                    log(pyautogui.typewrite, ('cur'))
                    repeated_press('right', 2)
                    data = get_data()
                    if int(data[3]) > 0:
                        goto_sheet('Contact')
                        email = get_email_address(data[0])
                        goto_sheet('calcs')
                        send_email(data, email)  # NEED TO CHANGE FROM DEFAULT EMAIL
                    goto_term('cur')
                    log(pyautogui.press, 'del')
                    repeated_press('left', 3)
    return 0


def main_logic() -> None:

    pyautogui.PAUSE = .3
    create_sheet('calcs')
    goto_sheet('Warehouse')
    goto_term('Part')
    log(pyautogui.hotkey, 'ctrl', 'a')
    log(pyautogui.hotkey, 'ctrl', 'c')
    goto_sheet('calcs', 'g', 1)
    log(pyautogui.hotkey, 'ctrl', 'v')
    log(pyautogui.press, 'up')
    delete_cols(['Name1', 'Dis', 'Tab', 'VPA'])
    create_date_col()
    item_count()
    create_today_col()
    create_date_dif_col()
    goto_cell('D', 1)
    iters = None
    try:
        iters = int(read_cell())
    except Exception as e:
        print('''Couldn't read spreadsheet length!''')
        raise
    goto_cell('b', 2)
    for i in range(iters):
        process()
        log(pyautogui.press, 'down')


def __main__() -> None:
    logging.basicConfig(filename=NAME_OF_LOG_FILE, level=logging.DEBUG)
    open_file_on_desktop(NAME_OF_FILE_TO_OPEN)
    main_logic()



__main__()
