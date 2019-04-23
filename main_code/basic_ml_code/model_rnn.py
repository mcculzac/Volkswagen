#################
# Kevin Gu
# Created: 2/13/2019
#################

"""Train an RNN with any input data and output an model"""

# sauce:
# https://machinelearningmastery.com/understanding-stateful-lstm-recurrent-neural-networks-python-keras/
# https://keras.io/getting-started/sequential-model-guide/


#########
# imports
#########


import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.utils import np_utils
from keras.preprocessing.sequence import pad_sequences
from typing import List, Tuple, Any
from random import randint
from sklearn.model_selection import train_test_split
import os
import math

###################
# Global variables
###################

READ_CSV_FROM = 'data.csv'
KEY_TO_NUMBER = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
                 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18,
                 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, 'lmenu': 26, 'tab': 27, 'lcontrol': 28,
                 'oem_period': 29, 'escape': 30, 'lwin': 31, 'left': 32, 'right': 33, 'up': 34, 'down': 35, 'lshift': 36,
                 'oem_minus': 37, 'oem_plus': 38, '0': 39, '1': 40, '2': 41, '3': 42, '4': 43, '5': 44, '6': 45, '7': 46,
                 '8': 47,'9': 48, 'space': 49, 'f1': 50, 'f2': 51, 'f3': 52, 'f4': 53, 'f5': 54, 'f6': 55, 'f7': 56,
                 'f8': 57, 'f9': 58, 'f10': 59, 'f11': 60, 'f12': 61, 'delete': 62, 'oem_1': 63, 'oem_2': 64,
                 'oem_3': 65}
LENGTH_OF_X = 3
NUMBER_OF_LSTM = 40


######################
# function definitions
######################

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

    better_data = []
    # convert characters to numbers
    for line in data:
        temp = []
        for char in line:
            if char != '':
                temp.append(KEY_TO_NUMBER[char.lower()])
        better_data.append(temp)
    data = better_data

    # get x, y values
    x = []
    y = []
    for line in data:
        if len(line) >= length + 1:
            num_guesses = len(line) // length
            if num_guesses == 0:
                num_guesses = 1
            for i in range(num_guesses):
                start = randint(0, len(line) - length - 1)
                x.append(line[start:start + length])  # get subset of length 3
                y.append(line[start + length])  # get the item after the length 3 subset

    # split for training
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=123, shuffle=True, test_size=0.2)

    # reshape training and testing data
    x_train = numpy.reshape(x_train, (len(x_train), length, 1))
    x_train = x_train / float(len(KEY_TO_NUMBER))

    y_train = np_utils.to_categorical(y_train)

    x_test = numpy.reshape(x_test, (len(x_test), length, 1))
    x_test = x_test / float(len(KEY_TO_NUMBER))

    y_test = np_utils.to_categorical(y_test)

    return x_train, x_test, y_train, y_test


# stateful LSTM still in progress
def train_model_stateful(batch_size, epos, x_train, y_train, x_test, y_test):
    model = Sequential()
    model.add(LSTM(32, return_sequences=True, stateful=True,
                   batch_input_shape=(batch_size, x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(32, return_sequences=True, stateful=True))
    model.add(LSTM(32, stateful=True))
    model.add(Dense(y_train.shape[1], activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epos, shuffle=False, verbose=2)

    scores = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=0)
    print("Model Accuracy:%.2f%%" % (scores[1] * 100))
    return model


# simple LSTM implementation
def train_model_normal(batch_size, epos, x_train, y_train, x_test, y_test, lstm_nodes=32):
    # create and initialize a model
    model = Sequential()

    # construct the layer
    model.add(LSTM(lstm_nodes, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dense(y_train.shape[1], activation='softmax'))

    # training the data
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=epos, verbose=2)

    # compare the model with test data set
    scores = model.evaluate(x_test, y_test, verbose=0)
    print("Model Accuracy:%.2f%%" % (scores[1] * 100))
    return model


def num_distinct_keys(x_train, y_train):

    unique_keys_feature = []
    for row in x_train:
        for val in row:
            if val not in unique_keys_feature:
                unique_keys_feature.append(val)
    print('Example x train row: ' + str(x_train[0]))
    print('Example y train value: ' + str(y_train[0]))
    print('There are {f} unique keys of input and {o} unique keys of output.'.format(f=len(unique_keys_feature), o=len(y_train[0])))
    print('The train size is {tr} and the test size is {t}.'.format(tr=len(x_train), t=math.floor(len(x_train) * .25)))


def __main__():
    x_train, x_test, y_train, y_test = pre_process_file(READ_CSV_FROM, LENGTH_OF_X)

    # get batch size and epochs
    print("Indicate the batch_size and the epochs with space between them: ")
    batch_size, epochs = list(map(int, input().split()))

    num_distinct_keys(x_train, y_train)

    # train the model use the training data
    model = train_model_normal(batch_size, epochs, x_train, y_train, x_train, y_train, NUMBER_OF_LSTM)
    model.save("rnnModel5-2.h5")


__main__()
