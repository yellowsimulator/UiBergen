"""
This is a test
"""

from glob import glob
import pandas as pd


def get_dates(path_to_folder):
    """
    This function get data
    """
    files = glob("{}/*".format(path_to_folder))
    dates = list(map(lambda f: str(f.split("/")[-1]), files))
    return dates


def get_data(date,k,root):
    """
    argument
    date: file name
    k: bearing number
    """
    path = "{}/{}".format(root,date)
    data_frame = pd.read_csv(path, header=None, delim_whitespace=True)
    try:
        return data_frame[k].values
    except IndexError:
        pass


def get_training_test_data():
    pass



if __name__ == '__main__':
    path_to_folder = "../data/2nd_test"
    dates = get_dates(path_to_folder)
    print(dates)
