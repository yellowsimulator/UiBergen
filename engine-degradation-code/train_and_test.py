"""
train and select a best model
"""
import warnings
import sklearn
warnings.filterwarnings("ignore")
from sklearn import preprocessing
import numpy as np
#from sklearn.linear_model import LinearRegression,Ridge
from sklearn import linear_model
from glob import glob
import pandas as pd
from numpy.linalg import norm
np.random.seed(10)
#1) check which normalisation method is good for each method
normalisation_score = {}
temp_dict = {}
temp_list = []



def train_predict_score(regressor,X_train,X_test,y_train):
    reg = regressor.fit(X_train, y_train)
    score = reg.score(X_train,y_train)
    pred = reg.predict(X_test)
    return pred, score




def get_cross_validation_data(X_train):
    pass


def cross_validation(X_train):
    pass





def get_all_files(path):
    files = glob("{}/*".format(path))
    return files

def load_test_data():
    train_path = "../data/Engine-degradation/CMAPSSData/train"


def get_datafram(task,file_k,engine_k):
    file = "../data/Engine-degradation/CMAPSSData/{}/{}_FD00{}.txt".format(task,task,file_k)
    df = pd.read_csv(file,delimiter=" ", header=None)
    del df[26]; del df[27]
    df_engine_k = df[df[0]==engine_k]
    return df_engine_k


def load_X_y_data(task,file_k,engine_k):
    """
    engine_k: 0 to 99
    task: 'train' or 'test'
    """
    df_engine_k = get_datafram(task,file_k,engine_k)
    X = df_engine_k.loc[:,2:].values
    y = df_engine_k.loc[:,1:1].values
    X_scale = preprocessing.scale(X)
    return X_scale, y


def error(y_test,y_true,norm_typ='None'):
    """
    norm_typ: 'l1', 'max', None for l2
    """
    diff = abs(y_test-y_true)
    if norm_typ == 'l1':
        norm_val = norm(diff,1)
    elif norm_typ == 'max':
        norm_val = norm(diff,inf)
    else:
        norm_val = norm(diff,inf)
    return norm_val


def get_validation_data(file_k):
    file = "../data/Engine-degradation/CMAPSSData/validation/RUL_FD00{}.txt".format(file_k)
    print(file)
    y = pd.read_csv(file,delimiter=" ", header=None)[0].values
    return y.reshape(-1,1)







import time
if __name__ == '__main__':

    train_path = "../data/Engine-degradation/CMAPSSData/train"
    engine_k = 1
    file_k = 1
    #for engine_k in range(1,100):

    y_true = get_validation_data(file_k)
    task = 'train'
    regressors = [linear_model.LinearRegression(), linear_model.Ridge(alpha=.5),
                    linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0], cv=3),
                    linear_model.Lasso(alpha=0.1),linear_model.LassoLars(alpha=.1),
                    linear_model.BayesianRidge()
                ]
    regressor = regressors[5]
    X_train, y_train = load_X_y_data('train',file_k,engine_k)
    X_test, y_test = load_X_y_data('test',file_k,engine_k)
    print(X_test.shape)
    print(X_train.shape)

    pred, score = train_predict_score(regressor,X_train,X_test,y_train)
    print(score)










#
