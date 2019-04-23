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
import csv


###############
# function defs
###############

# pre_process data function written by Zac
def pre_process_file(list_files: Any, length, file_o='data', split=True) -> None:
    """
    this takes the data in from a csv format and converts into xtrain through y test in numerical data
    NOTE: This function is very ad hoc and attempts to process data: really should be changed into a
    better rendition of sliding window or whatever your preferred schema is.

    """

    # load files and then convert them into one massive list
    if list_files is None:
        list_files = os.listdir('../data/clean_data/')
    data = []
    for file in list_files:
        with open('../data/clean_data/' + file, 'r') as f:
            string_data = f.read()
        temp = string_data.replace('\n', 'Enter,')
    data = temp
    # generates the appropriate string to int conversion
    dict_converter = int_api.generate_char_to_int_dict(data)

    temp = []
    # convert characters to numbers
    for char in data:
        if char != '':
            temp.append(dict_converter[char])

    data = temp

    # get x, y values
    x = []
    y = []

    if len(data) >= length+1:
        num_guesses = 2*len(data)  # modify to change # of data points to be generated from line
        for i in range(num_guesses):
            start = randint(0, len(data)-length-1)
            x.append(data[start:start+length])  # get subset of length n
            y.append(data[start+length])  # get the item after the length n subset
    else:
        raise ValueError('Unable to make divisions of length %d when total data length is %d' % (length, len(data)))

    # split for training
    if split:
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=123, shuffle=True, test_size=0.2)
    else:  # if for some reason we don't want to split
        x_train, x_test = x, x
        y_train, y_test = y, y

    # print(len(x_train[0]), len(x_test[0]), len(y_train[0]), len(y_test[0]))

    # reshape training and testing data
    # x_train = np.reshape(x_train, (len(x_train), length, 1))
    x_train = np.array(x_train)
    x_train = [[x/float(len(dict_converter)) for x in row] for row in x_train]
    # x_train = x_train / float(len(dict_converter))

    y_train = np_utils.to_categorical(y_train, num_classes=len(dict_converter))

    # x_test = np.reshape(x_test, (len(x_test), length, 1))
    x_test = [[x/float(len(dict_converter)) for x in row] for row in x_test]
    # x_test = x_test / float(len(dict_converter))

    y_test = np_utils.to_categorical(y_test, num_classes=len(dict_converter))

    output_file = '../data/ml_data/' + file_o

    # write xtrain, xtest, ytrain, ytest into files
    np.savetxt(output_file + '_xtr.csv', x_train, delimiter=',')
    np.savetxt(output_file + '_xte.csv', x_test, delimiter=',')
    np.savetxt(output_file + '_ytr.csv', y_train, delimiter=',')
    np.savetxt(output_file + '_yte.csv', y_test, delimiter=',')
    keys = np.array(list(dict_converter.keys()))
    values = np.array(list(dict_converter.values()))
    np.savetxt('../ML/' + file_o + '_k.txt', keys, delimiter=',', fmt='%s')
    np.savetxt('../ML/' + file_o + '_v.txt', values, delimiter=',', fmt='%d')


def __main__():
    pre_process_file(['auto_check_open.csv'], 10, 'auto_check_open', split=False)


__main__()

