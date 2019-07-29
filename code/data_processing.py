import os
import json
import matplotlib
import pandas as pd
import modin.pandas as mpd
from glob import glob
#matplotlib.use('Agg')
from sklearn import preprocessing
import matplotlib.pyplot as plt
from signal_processing import *


def scale_data(data):
    scaled_data = preprocessing.scale(data)
    return scaled_data


def get_average_amplitude():
    pass


def create_json_data(data,file_name):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def read_json_data(path_to_json):
    with open(path_to_json) as json_data:
        jsd = json.load(json_data)
        return jsd


def get_dates(path_to_folder):
    """
    This function get data
    """
    files = glob("{}/*".format(path_to_folder))
    dates = list(map(lambda f: str(f.split("/")[-1]), files))
    return dates


def get_data(date,k):
    """
    argument
    date: file name
    k: bearing number
    """
    path = "{}".format(date)
    data_frame = pd.read_csv(path, header=None, delim_whitespace=True)
    try:
        return data_frame[k].values
    except IndexError:
        pass


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
    try:
        return pd.read_csv(path)[column_name].values
    except:
        exit()


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


def get_date_files(dates):
    """
    This function transform date file from 2003.11.20.23.54.03
    to 2003_11_20_23_54_03. The result is used later to
    create output csv files

    Arguments:
    ----------
    dates:
    It is a list containing strings of the form 2003.11.20.23.54.03.

    Returns:
    --------
    A list containing strings of the form 2003_11_20_23_54_03
    """
    return list(map(lambda date: date.replace(".", "_"), dates))


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


def create_labeled_csv_files(input_folder, output_folder, data_columns,label):
    """
    Create a csv file with one column. the column is one of
    the label: "bpfi","bpfo" or "no_defect".

    Argumens:
    --------
    input_folder:
    It is either "../data/1st_test" or "../data/2nd_test" or
    "../data/3rd_test".

    output_folder:
    specify by the user. But should be in data folder.

    data_columns:
    It is a list containing the column number corresponding
    to the label.

    label:
    it is either "bpfi","bpfo" or "no_defect"
    """
    dates = get_dates(input_folder)
    date_files = get_date_files(dates)
    for k in data_columns:
        for date, output_file in zip(dates, date_files):
            column = get_data(date, k, input_folder)
            d = {label:column}
            df = pd.DataFrame(d)
            df.to_csv("{}/{}.csv".format(output_folder, output_file))
            print("{} data saved to csv".format(date))


def plot_chanels_data(chanels,test_number):
    if not os.path.exists("{}_pictures".format(test_number)):
        os.makedirs("{}_pictures".format(test_number))
    path_to_files = "../data/{}".format(test_number)
    files = get_all_files(path_to_files,type=None)
    fault_freqs = {"bpfo":236.4, "bpfi":296.8, "rdf":280.4}
    indexes = list(fault_freqs.keys())
    for k in chanels:
        if not os.path.exists("{}_pictures/{}".format(test_number,k+1)):
            os.mkdir("{}_pictures/{}".format(test_number,k+1))
        key = "chanel{}".format(k+1)
        for fault_name in fault_freqs:
            fault_freq = fault_freqs[fault_name]
            temp_container = []
            for path in files:
                print("processing {} for {}".format(path,key))
                data = get_data(path,k)
                print(data)
                exit()
                bpfi, amplitude = get_fault_frequency(data,fault_freq)
                if amplitude is not None:
                    temp_container.append(amplitude)
            print("ploting for {} chanel {}".format(fault_name,k+1))
            plt.plot(temp_container)
            plt.ylim([0,0.03])
            plt.title("amplitude for {} and {}".format(key,fault_name))
            plt.savefig("{}_pictures/{}/{}_{}.png".format(test_number,k+1,key,fault_name))
            plt.close()





if __name__ == '__main__':
    chanels = [0,1,2,3]
    test_number = "2nd_test"
    plot_chanels_data(chanels,test_number)
