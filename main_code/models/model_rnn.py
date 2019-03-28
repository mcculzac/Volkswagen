#################
# Zac McCullough
# 3/13/2019
#################

"""
RNN Model capable of taking in parameters of training parameters
"""


#########
# imports
#########


import numpy as np
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
import numpy as np
import csv

###################
# Global variables
###################


####################
# function definitions
####################


# simple LSTM implementation
def train_model_normal(batch_size, epos, x_train, y_train, x_test, y_test):
    # create and initialize a model
    model = Sequential()

    # construct the layer
    model.add(LSTM(32, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dense(y_train.shape[1], activation='softmax'))

    # training the data
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epos, verbose=2)

    # compare the model with test data set
    scores = model.evaluate(x_test, y_test, verbose=0)
    print("Model Accuracy:%.2f%%" % (scores[1] * 100))
    return model


def __main__():

    data_input = 'data'
    data_input = '../data/ml_data/' + data_input

    x_train = np.loadtxt(data_input + '_xtr.csv', delimiter=',')
    y_train = np.loadtxt(data_input + '_ytr.csv', delimiter=',')
    x_test = np.loadtxt(data_input + '_xte.csv', delimiter=',')
    y_test = np.loadtxt(data_input + '_yte.csv', delimiter=',')

    # load data in
    # with open(data_input+'_xtr.csv', 'r') as f:
    #     r = csv.reader(f, delimiter=',')
    #     x_train = [row for row in r]
    # with open(data_input+'_xte.csv', 'r') as f:
    #     r = csv.reader(f, delimiter=',')
    #     x_test = [row for row in r]
    # with open(data_input+'_ytr.csv', 'r') as f:
    #     r = csv.reader(f, delimiter=',')
    #     y_train = [row for row in r]
    # with open(data_input+'_yte.csv', 'r') as f:
    #     r = csv.reader(f, delimiter=',')
    #     y_test = [row for row in r]

    x_train, x_test, y_train, y_test = np.array(x_train), np.array(x_test), np.array(y_train), np.array(y_test)
    x_train = np.reshape(x_train, (len(x_train), len(x_train[0]), 1))
    x_test = np.reshape(x_test, (len(x_test), len(x_test[0]), 1))

    print(x_train)

    batch_size = len(x_train)
    epochs = 10000

    # train the model use the training data
    model = train_model_normal(batch_size, epochs, x_train, y_train, x_train, y_train)
    model.save("../ML/rnnModel.h5")


__main__()
