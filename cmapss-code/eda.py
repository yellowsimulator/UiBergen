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
    task = 'train'; file_k = 1
    file_train = "../data/Engine-degradation/CMAPSSData/{}/{}_FD00{}.txt".format('train','train',file_k)
    file_test = "../data/Engine-degradation/CMAPSSData/{}/{}_FD00{}.txt".format('test','test',file_k)
    #train_path = "../data/Engine-degradation/CMAPSSData/train"
    df_train = get_data(file_train)
    df_test = get_data(file_test)
    #df1 = df[df[0]==1]
    print(df_test)
    print(df_train)
