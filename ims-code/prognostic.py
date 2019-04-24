"""
Compute some important stuff here
"""
from multiprocessing import Pool
from etl import *

print("ok")
#get_all_dates(exp_numb)
exp_numb = 1
channel = 0

all_dates = get_all_dates(exp_numb)
all_files = get_experiment_data(exp_numb)
for file in all_files:
    data = get_dataframe
with Pool() as p:
    data = p.map(get_bearing_data, all_files)
    iqrs = p.map(get_iqr, data)
    df = pd.DataFrame({"timestamp": all_dates,"iqr": iqrs})
    df.to_csv("test.csv")
    #print(data)
#print(all_files)
#for k, file in enumerate(all_files):
    #print("processing file {}".format(k+1))
    #time_series = get_bearing_data(file,channel)
    #print(time_series)
    #iqr = get_iqr(time_series)
    #print(iqr)
