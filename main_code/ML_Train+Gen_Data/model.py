#################
# Zac McCullough
# Created: 2/01
#################

"""Train model based on data in data.csv"""

# sauce: https://www.kaggle.com/nvhbk16k53/simple-rnn-with-keras

#########
# imports
#########

import numpy as np
import pandas as pd
import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import keras
import keras.backend as k
from typing import List

###################
# Global variables
###################

READ_CSV_FROM = 'data.csv'


######################
# function definitions
######################

def pre_process(file_name) -> List[List[str], str]:


def __main__():
    train_df = pd.read_csv("../input/train.csv", sep=",")
    train, dev = train_test_split(train_df, random_state=123, shuffle=True, test_size=0.1)

