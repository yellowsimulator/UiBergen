import numpy as np
from sklearn import preprocessing
import scipy.stats as stat
from scipy.stats import ks_2samp
from get_data import *

def ks_test():
    k = 0
    alpha = 0.01
    dates = get_dates()
    # ref = preprocessing.scale(get_data(dates[0],k))
    for j,date in enumerate(dates):
        ref = preprocessing.scale(get_data(dates[k],k))
        data =  preprocessing.scale(get_data(dates[j+10],k))
        statvalue, pvalue = ks_2samp(ref,data)

        if pvalue > alpha:
            print(pvalue)
            print("cannot reject H0 for {}".format(date))




if __name__ == '__main__':
    ks_test()
