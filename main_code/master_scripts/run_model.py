###################
# Zac McCullough
# mccul157@msu.edu
# 4/10
###################

"""Given saved H5 runs it until model spits out a ctrl+v"""

#########
# imports
#########

import sys
sys.path.append('../')
from pywinauto.win32_hooks import Hook, KeyboardEvent, MouseEvent
import keras
from typing import List, Dict
import pyautogui
import numpy as np
from int_api import convert_pywinauto_pyautogui

###############
# function defs
###############


def load_model(model_name: str):
    # print('load model!')
    loc = '../ML/' + model_name + '.h5'
    return keras.models.load_model(loc)


def convert_num_to_key(dict_converter: Dict[str, int], num: float):
    # print('convert!, num: %f' % num)
    # print('dict_converter: ' + str(dict_converter))
    for k, v in dict_converter.items():
        if num == v:
            return k
    raise ValueError('Passed key to convert that could not be found in dict!')


def execute(key: str, dict_converter: Dict[str, int], hist: List[float], length: int) -> List[float]:
    """
    Will need to modify as am currently just hard coding ctrl, alt etc. Best solution probably is for
    multi-stroke keys to be encoded as singular key in data.
    :param key: string of key to press
    :param dict_converter: dict converter loaded in
    :param hist: history of keys
    :param length: length of history to keep for model
    :return: history
    """
    print('dict_converter: ', dict_converter)
    int_form = dict_converter[key]  # get int form of key for model
    scaled_int = int_form/float(len(dict_converter))  # get scaled form
    if len(hist) > length-1:
        hist = hist[1:]
    if len(hist) > 0:
        prev_key = convert_num_to_key(dict_converter, hist[-1]*float(len(dict_converter)))
    else:
        prev_key = ''

    pyautogui.PAUSE = 1
    print('hist: ', hist)
    if prev_key.lower() in ['lcontrol', 'lshift', 'lalt', 'lwin']:
        key = convert_pywinauto_pyautogui(key).lower()
        prev_key = convert_pywinauto_pyautogui(prev_key).lower()
        print('hotkey!: %s %s' % (prev_key, key))
        pyautogui.hotkey(prev_key, key)
    else:
        print('key: %s' % key.lower())
        pyautogui.press(key.lower())
    hist.append(scaled_int)

    return hist


def run_starter(starter: List[str], dict_converter: Dict[str, int], length: int) -> List[float]:
    # print('starter!')
    hist = []
    for key in starter:
        hist = execute(key, dict_converter, hist, length)
        if len(hist) >= 3 and hist[-3:] == ['Lcontrol', 'C', 'Escape']:
            raise StopIteration('Found escape sequence!')
    return hist


def run(starter: List[str], file):
    print('run!')
    model = load_model(file)
    keys = np.loadtxt('../ML/' + file + '_k.txt', dtype='<U9')
    values = np.loadtxt('../ML/' + file + '_v.txt')
    dict_convert = dict(zip(keys, values))
    x_train = np.loadtxt('../data/ml_data/' + file + '_xtr.csv', delimiter=',')
    length = len(x_train[0])
    hist = run_starter(starter, dict_convert, length)
    while len(hist) >= 3 and hist[-3:] != ['Lcontrol', 'C', 'Escape']:
        key_float = model.predict(hist)
        key = convert_num_to_key(num=key_float, dict_converter=dict_convert)
        hist = execute(key, dict_convert, hist, length)


def __main__():
    starter = ['Lwin', 'E', 'Lcontrol', 'F', 'Tab', 'Down', 'Tab', 'Lcontrol', 'F',
               'E', 'X', 'Lshift', 'Oem_Minus', '1', 'Tab', 'Tab', 'Space', 'Enter']
    file = 'auto_check_open'
    run(starter, file)


__main__()

