#################
# Zac McCullough
# Created: 2/01
#################

"""Train model based on data in data.csv"""

# sauce: https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html

#########
# imports
#########

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from sklearn.svm import SVC
from typing import List, Tuple, Any
from random import randint


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

def pre_process(file_name) -> Tuple[Any, Any, Any, Any]:
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
    return x_train, x_test, y_train, y_test


def __main__():
    x_train, x_test, y_train, y_test = pre_process(READ_CSV_FROM)

    regr = SVC(gamma='auto') # Support Vector Classification (SVM)
    regr.fit(x_train, y_train) # Training
    y_pred = regr.predict(x_test) # Predict test y, output is continuous (real)
    temp = []
    for val in y_pred:
        temp.append(round(val))  # round to intd - discrete values
    y_pred = temp

    #################################
    # MSE, Variance, & Accuracy
    # Metrics to measure the model
    ##################################

    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(y_test, y_pred))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(y_test, y_pred))
    print('Accuracy Score: ' + str(100*accuracy_score(y_test, y_pred)) + '%')


__main__()
