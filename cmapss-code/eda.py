"""
Exploratory data analysis
"""
import os
import warnings
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")


def get_all_files(path):
    files = glob("{}/*".format(path))
    return files





def get_data(path):
    df = pd.read_csv(path,delimiter=" ", header=None)
    del df[26]
    del df[27]
    #df.drop('27',1)
    return df


if __name__ == '__main__':

    train_path = "../data/Engine-degradation/CMAPSSData/train"
    all_train_files = get_all_files(train_path)
    file_path = all_train_files[0]
    df = get_data(file_path)
    df1 = df[df[0]==1]
    print(df1)
