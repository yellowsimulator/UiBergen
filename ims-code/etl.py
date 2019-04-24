"""
Extract data, Transform data and Load
data if neccessary
"""
import pandas as pd
from glob import glob
import scipy.stats
from multiprocessing import Pool


def get_date_from_file(file):
    """
    return the date extension from a
    file.
    Argument:
        file: a file.
    Return:
        datetime of the form yyyy-mm-dd hh:mm:ss
    """
    try:
        datetime = file.split("/")[-1]
        hour = ":".join(datetime.split(".")[3:])
        date = "-".join(datetime.split(".")[:3])
        new_date = "{} {}".format(date,hour)
        return new_date
    except Exception as e:
        print("Error function 'get_date_from_file': ", e)
        return "error"


def get_all_dates(exp_numb):
    """
    Return all dates from a file.
    Argument:
        exp_numb: the experiment number.
    """
    all_files = get_experiment_data(exp_numb)
    with Pool() as p:
        datetime = p.map(get_date_from_file, all_files)
        return datetime


def get_all_data(exp_numb):
    all_files = get_experiment_data(exp_numb)
    with Pool() as p:
        data = p.map(get_dataframe,all_files)
        return data


def get_all_iqrs(files):
    all_data = []
    with Pool() as p:
        iqrs = p.map(get_iqr, all_data)


def get_iqr(time_series):
    """
    Return the inter quantile range.
    If an error occurs, the string
    "erro will be return".
    Argument:
        time_series: the time series data
    Return:
        iqr
    """
    try:
        iqr = scipy.stats.iqr(time_series)
        return iqr
    except Exception as e:
        print("Error in function 'get_iqr': ", e)
        return "error"


def health_index(faults_amps, iqr):
    """
    This function return the health index.
    If an error occured, the string "error"
    will be return
    Arguments:
        faults_amps: a dictionary of bearing faults
                     amplitude of the form {"bpfo":0.4,
                     "bpfi":2., ...}
        iqr: the inter quantile range of a time series
    Return:
        H: the health index of a time series.
    """
    try:
        H = iqr*sum(faults_amps.values())
        return H
    except Exception as e:
        priint("Error in function 'health_index': ", e)
        return "error"


def get_all_files(path):
    """
    This function retirns all files from
    a directory specified by a path.
    If an erro occurred the string "error"
    will be return and an error will be printed.
    Argument:
        path: directory path
    Return:
        files: all files in the directory
        specified by path argument.
    """
    try:
        files = glob("{}/*".format(path))
        return files
    except Exception as e:
        print("Error in function 'get_all_files': ", e)
        return "error"


def get_dataframe(path):
    """
    Return a dataframe from.
    If an erro occurs return the
    string "error".
    Argument:
        path: file path
    Return:
        dataframe: a pandas dataframe
    """
    try:
        dataframe = pd.read_csv(path,header=None,delim_whitespace=True)
        return dataframe
    except Exception as e:
        print("Error in function 'get_dataframe': ", e)
        return "error"


def get_experiment_data(exp_numb):
    """
    Return all file for a given experiment.
    Arguments:
        exp_numb: experiment number: 1,2 or 3
    Return:
        all_files: all files
    """
    experiments = {"1": "1st_test",
                   "2": "2nd_test",
                   "3": "3rd_test"}
    experiment = experiments["{}".format(exp_numb)]
    main_path = "../data/IMS/{}".format(experiment)
    try:
        all_files = get_all_files(main_path)
        return all_files
    except Exception as e:
        print("Error in function 'get_experiment_data': ", e)
        return "error"


def get_bearing_data(file):
    """
    Return data for a bearing.
    channel = 0,1,3,4 for bearing 1,2,3,4
    or channel = 0,1 bearing 1 axial and radial
       channel = 2,3, bearing 2 axial and radial
    similarly for bearing 3 and 4.
    Argument
        file: path to file
        channel: channel number
    """
    channel = 0
    data_frame = get_dataframe(file)
    try:
        return data_frame[channel].values
    except Exception as e:
        print("Error in function 'get_bearing_data': ", e)
        return "error"


def main():
    print("ok")



if __name__ == '__main__':
    main()
