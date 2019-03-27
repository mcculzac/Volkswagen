###################
# Zac McCullough
# mccul157@msu.edu
# 3/13
###################

"""
This will attempt to take all data in unclean data, clean it, and put it into cleaned data.  This will be able to handle
parameters for creating different kinds of data e.g. 5 x, 1 y, 12 x, 5 y.  Sliding window and shit.
"""

#########
# imports
#########

import os
import sys
sys.path.append('../')
import int_api
# from int_api import *
from typing import Tuple, List, Any
import numpy as np
from random import randint
from sklearn.model_selection import train_test_split
from keras.utils import np_utils


###############
# function defs
###############

# pre_process data function written by Zac
def pre_process_file(file_name, length) -> Tuple[Any, Any, Any, Any]:
    """
    this takes the data in from a csv format and converts into xtrain through y test in numerical data
    :param file_name: file name
    :return: our xtrain, xtest, ytrain, ytest
    """

    # convert csv to two dimensional list
    data = []
    with open(file_name, 'r') as f:
        string_data = f.read()
    temp = string_data.split('\n')
    for line in temp:
        data.append(line.split(','))

    # generates the appropriate string to int conversion
    dict_converter = int_api.generate_char_to_int_dict(data[0])

    better_data = []
    # convert characters to numbers
    for line in data:
        temp = []
        for char in line:
            if char != '':
                temp.append(dict_converter[char])
        better_data.append(temp)
    data = better_data

    # get x, y values
    x = []
    y = []
    for line in data:
        if len(line) >= 4:
            num_guesses = len(line) // 6
            if num_guesses == 0:
                num_guesses = 1
            for i in range(num_guesses):
                start = randint(0, len(line)-4)
                x.append(line[start:start+3])  # get subset of length 3
                y.append(line[start+3])  # get the item after the length 3 subset

    # split for training
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=123, shuffle=True, test_size=0.2)

    # reshape training and testing data
    x_train = np.reshape(x_train, (len(x_train), length, 1))
    x_train = x_train / float(len(dict_converter))

    y_train = np_utils.to_categorical(y_train)

    x_test = np.reshape(x_test, (len(x_test), length, 1))
    x_test = x_test / float(len(dict_converter))

    y_test = np_utils.to_categorical(y_test)

    return x_train, x_test, y_train, y_test


def __main__():

    print(pre_process_file(int_api.__main_code_path__ + 'hand-generated-1.csv', 3))


__main__()






