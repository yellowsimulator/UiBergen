"""
Exploratory data analysis
"""
import os
import warnings
import numpy as np
import pandas as pd
from glob import glob
import pyarrow.parquet as pq
import multiprocessing as mp
import matplotlib.pyplot as plt
from multiprocessing import Pool

warnings.filterwarnings("ignore")



def get_all_files(path):
    """
    get all files from a given directory
    """
    files = glob("{}/*".format(path))
    return files


def get_file_size(path):
    """
    Returns the size of a file
    in Mb
    """
    size = os.stat(path).st_size/1e6
    return size


def from_parquet_to_dataframe(parquet_file):
    """
    This function Reads a parquet file and returns
    a pandas dataframe.
    Argument:
        parquet_file: a valid parquet file
    Return:
        df: a pandas dataframe
    """
    df = pq.read_pandas(parquet_file).to_pandas()
    return df


def save_dataframe_to_parquet(df, output_file):
    """
    save a dataframe as parquet file.
    The parquet file is highly compressed
    as opposed to csv.
    Argument:
        file_name: name of file including the path
        Example: file_name = 'my_folder/my_file',
        to save my_file.snappy.parquet to folder,
        my_folder.
    """
    try:
        df.to_parquet(output_file, engine='auto', compression='snappy')
    except Exception as e:
        print("---------------------------------------------------------")
        print("An error occurred: ", e,".")
        print("Change your dataframe columns to string and try again :)")
        print("---------------------------------------------------------")


def get_dataframe(path):
    """
    This function return a dataframe.
    It replaces numerical columns with
    corresponding attribute (string) name.
    Argument:
        path: its the path to the csv file
    Return:
        df: A pandas dataframe
    """
    df = pd.read_csv(path,delimiter=" ", header=None)
    del df[26]
    del df[27]
    col1 = ['engine', 'cycle', 'setting1', 'setting2', 'setting3']
    col2 = ["sensor{}".format(k) for k in range(1,22)]
    new_columns = col1+col2
    df.columns = new_columns
    return df


def worker(folder):
    path = "../data/Engine-degradation/CMAPSSData/{}".format(folder)
    all_files = get_all_files(path)
    for k, file in enumerate(all_files):
        abs_name = file.split("/")[-1].split(".")[0]
        df = get_dataframe(file)
        output_file = "data/{}/{}.snappy.parquet".format(folder,abs_name)
        try:
            save_dataframe_to_parquet(df,output_file)
            print("{} saved successfuly".format(output_file))
        except Exception as e:
            print("An error occured: ", e)


def run(): 
    with Pool() as p:
        p.map(worker, ['train', 'test'])



if __name__ == '__main__':
    folders = ["train","test"]
    run()
    #worker(folder)
    #exit()
    #path = "train_FD001.snappy.parquet"
    #df = from_parquet_to_dataframe(path)
    #print(df)
    #size = get_file_size(path)
    #print(size)
    #exit()






    #save_dataframe_to_parquet(file_name)
    #df_train.to_parquet("{}_FD00{}.snappy.parquet".format('train',file_k), engine='auto',compression='snappy')











    #df1 = df[df[0]==1]
