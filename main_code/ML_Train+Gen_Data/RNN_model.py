#################
# Kevin Gu & Zachary McCullough
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

###################
# Global variables
###################

READ_CSV_FROM = 'data.csv'
KEY_TO_NUMBER = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
                 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18,
                 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, 'lmenu': 26, 'tab': 27, 'lcontrol': 28,
                 'oem_period': 29, 'escape': 30}


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
def train_model_normal(batch_size, epos, x_train, y_train, x_test, y_test):

    # create and initialize a model
    model = Sequential()

    # construct the layer
    model.add(LSTM(32,input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dense(y_train.shape[1], activation='softmax'))

    # training the data
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epos, verbose=2)

    # compare the model with test data set
    scores = model.evaluate(x_test, y_test, verbose=0)
    print("Model Accuracy:%.2f%%" % (scores[1] * 100))
    return model

def __main__():
    # print("Please input the filename that contain data: ")
    # READ_CSV_FROM = input()

    # print("Please input the length the of test case")
    # length = int(input())
    # preprocess data
    length = 3
    x_train, x_test, y_train, y_test = pre_process_file(READ_CSV_FROM, length)

    print("Indicate the batch_size and the epochs with space between them: ")
    batch_size, epochs = list(map(int,input().split()))
    # train the model use the training data
    model = train_model_normal(batch_size, epochs, x_train, y_train, x_train, y_train)
    model.save("rnnModel")

    

__main__()
