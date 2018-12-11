from signal_processing import *
from data_processing import *
from plots import *


amplitudes = []
path_to_files = "../data/bpfo_data"
dates_files = get_all_files(path_to_files,type=None)
column_name = "bpfo"
for path in dates_files:
    data = get_one_column_data(path,column_name)
    bpfo, bpfo_amp = get_bpfo(data)
    if bpfo_amp is not None:
        amplitudes.append(bpfo_amp[0])
        print(bpfo, bpfo_amp)

simple_plot(amplitudes,title="bpfo amplitude",
            xlabel="index",ylabel="amplitude")
