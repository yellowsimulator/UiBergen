import json
import pandas as pd
from glob import glob
from sklearn import preprocessing


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





if __name__ == '__main__':
    input_folder = "../data/1st_test"
    output_folder = "../data/bpfi_data"
    data = {
            "bearing1":{"bpfo":0.1,"bpfo":0.001,"rdf":0.0003},
            "bearing2":{"bpfo":0.143,"bpfo":0.101,"rdf":2.0003},
            "bearing3":{"bpfo":2.1,"bpfo":3.001,"rdf":10.0003},
            "bearing4":{"bpfo":20.1,"bpfo":30.001,"rdf":40.0003},

    }
    path_to_json = "3rd_test_len2.json"
    d = read_json_data(path_to_json)
    print("bearing 1",d["bearing1"])
    print("bearing 2",d["bearing2"])
    print("bearing 3",d["bearing3"])
    print("bearing 4",d["bearing4"])
    #print(d["bearing1"]["bpfo"])
    #create_json_data(data)
