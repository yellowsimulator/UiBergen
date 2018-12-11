import pandas as pd
from glob import glob
from get_data import *

def get_all_files(path_to_files,type=None):
    """
    get all files from a path_to_folderself.
    If type is not none return only the files
    type. Example type=csv
    """
    if type == "csv":
        files = glob("{}/**.csv".format(path_to_files))
    elif type == "h5":
        files = "h5 files" #to be implemented
    elif type == None:
        files = glob("{}/*".format(path_to_files))
    return files


def create_hdf_file(origine,dest,name):
    df = pd.read_csv(origine)
    df.to_hdf(dest,key=name,mode="a")


def read_hdf(path,name):
    df = pd.read_hdf(path,key=name)
    return df


def read_data(path):
    df = pd.read_csv(path,header=None,delim_whitespace=True)
    return df


def get_one_column_data(path,column_name):
    return pd.read_csv(path)[column_name].values


def create_bpfo_data(path_to_folder):
    dates = get_dates(path_to_folder)
    created_date_files = list(map(lambda date: date.replace(".", "_"),
     dates))
    k = 0
    for date, output_file in zip(dates,created_date_files):
        root = "../data/2nd_test"
        column = get_data(date,k,root)
        d = {"bpfo":column}
        df = pd.DataFrame(d)
        df.to_csv("../data/bpfo_data/{}.csv".format(output_file))
        print("{} data saved to csv".format(date))


def create_healthy_data(path_to_folder):
    healthy_columns = [1,2,3]
    dates = get_dates(path_to_folder)
    created_date_files = list(map(lambda date: date.replace(".", "_"), dates))
    for k in healthy_columns:
        for date, output_file in zip(dates,created_date_files):
            root = "../data/2nd_test"
            column = get_data(date,k,root)
            d = {"no_defect":column}
            df = pd.DataFrame(d)
            df.to_csv("../data/healthy_data/{}.csv".format(output_file))
            print("{} data saved to csv".format(date))


def create_bpfi_data():
    pass



if __name__ == '__main__':
    path_to_folder = "../data/2nd_test"
    create_bpfo_data(path_to_folder)
