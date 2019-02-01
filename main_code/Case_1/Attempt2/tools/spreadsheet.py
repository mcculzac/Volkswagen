#####################
# Zachary McCullough
# mccul157@msu.edu
# 2018-1-23
#####################

# This will hold spreadsheet based api tools


##########
# import
##########

from .logpyautogui import log
import pyautogui
from .generic import grab_clipboard
import typing as t
import pywintypes

###########
# functions
###########

def get__spreadsheet_data() -> t.List[str]:
    """
    gathers all data in the spreadsheet as strings
    :return: list of strings, where each entry is an entire sheet
    """

    data = []
    count = 0
    while True:
        # get spreadsheet data
        pyautogui.PAUSE = .3
        log(pyautogui.hotkey, 'ctrl', 'a')
        log(pyautogui.hotkey, 'ctrl', 'c')
        temp = log(grab_clipboard)
        if temp not in data:  # if not in data yet
            data.append(temp)  # add it
        else:  # data is in list so
            break
        # go to next sheet upwards
        log(pyautogui.hotkey, 'ctrl', 'fn', 'pageup')
        count += 1

    # reset to the 'next' empty sheet
    for i in range(count):
        log(pyautogui.hotkey, 'ctrl', 'fn', 'pagedown')

    while True:
        # get spreadsheet data
        log(pyautogui.hotkey, 'ctrl', 'a')
        log(pyautogui.hotkey, 'ctrl', 'c')
        temp = log(grab_clipboard)
        if temp not in data:  # if not in data yet
            data.append(temp)  # add it
        else:  # we've reached end of all sheets
            break
        # go to next sheet downwards
        log(pyautogui.hotkey, 'ctrl', 'fn', 'pagedown')
    return data


def reset() -> None:
    pyautogui.PAUSE = .4
    log(pyautogui.hotkey, 'ctrl', 'g')
    log(pyautogui.typewrite, 'A1', interval=.1)
    log(pyautogui.press, 'enter')


def goto_cell(col: str, row: int) -> None:
    log(pyautogui.hotkey, 'ctrl', 'g')
    log(pyautogui.typewrite, col + str(row))
    log(pyautogui.press, 'enter')


def goto_sheet(sheet_name: str, col: str = 'A', row: int = 1) -> None:
    pyautogui.PAUSE = .4
    log(pyautogui.hotkey, 'ctrl', 'g')
    log(pyautogui.typewrite, '%s!%s%d' % (sheet_name, col, row), interval=.1)
    log(pyautogui.press, 'enter')


def find_val(value:str) -> None:
    pyautogui.PAUSE = .4
    log(pyautogui.hotkey, 'ctrl', 'f')
    log(pyautogui.typewrite, value, interval=.1)
    log(pyautogui.press, 'enter')


def create_sheet(name_of_sheet: str) -> None:
    pyautogui.PAUSE = .4
    log(pyautogui.hotkey, 'ctrl', 'fn', 'f11')
    log(pyautogui.hotkey, 'alt', 'h')
    log(pyautogui.press, 'o')
    log(pyautogui.press, 'r')
    log(pyautogui.typewrite, name_of_sheet, interval=.1)
    log(pyautogui.press, 'enter')


def read_cell() -> str:
    pyautogui.PAUSE = .1
    log(pyautogui.hotkey, 'ctrl', 'c')
    log(pyautogui.hotkey, 'ctrl', 'f')
    log(pyautogui.hotkey, 'ctrl', 'v')
    log(pyautogui.hotkey, 'ctrl', 'shift', 'left')
    log(pyautogui.hotkey, 'ctrl', 'c')
    log(pyautogui.press, 'esc')
    result = None
    while result is None:
        try:
            result = grab_clipboard()
        except Exception as e:
            pass
    return result


def get_col_len(column:str, cell_col:str, cell_row:int) -> int:
    pyautogui.PAUSE = .1
    goto_cell(cell_col, cell_row)
    log(pyautogui.typewrite, '=LEN({c}1:{c}10000'.format(c=column))
    log(pyautogui.press, 'up')
    return int(grab_clipboard())


def update_formulas() -> None:
    pyautogui.PAUSE = .1

    log(pyautogui.hotkey, 'ctrl', 'h')  # open replace box
    log(pyautogui.hotkey, 'shift', 'tab')  # go up one value
    log(pyautogui.press, '=')  # insert = to find
    log(pyautogui.press, 'tab')  # go down
    log(pyautogui.press, '=')  # insert = to replace
    log(pyautogui.press, 'tab')  # go to dialogue boxes
    log(pyautogui.press, 'a')  # shortcut to replace all
    log(pyautogui.press, 'enter')  # accept replaced values
    log(pyautogui.press, 'esc')  # close replace box


def delete_cur_col() -> None:
    pyautogui.PAUSE = .1

    log(pyautogui.press, 'alt')  # menu nav by key
    log(pyautogui.press, 'h')  # goto home
    log(pyautogui.press, 'd')  # delete
    log(pyautogui.press, 'c')  # column


def goto_term(term: str) -> None:
    pyautogui.PAUSE = .3
    log(pyautogui.hotkey, 'ctrl', 'f')
    log(pyautogui.typewrite, term, interval=.1)
    log(pyautogui.press, 'enter')
    log(pyautogui.press, 'esc')


def delete_cols(list_of_headers: t.List[str]) -> None:
    for header in list_of_headers:
        goto_term(header)
        delete_cur_col()


