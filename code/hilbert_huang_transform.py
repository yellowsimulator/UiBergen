import numpy as np
import pandas as pd
from plots import *
from pyhht.emd import EMD
#from data_processing import *
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from pyhht.visualization import plot_imfs


def hilbert_huang_transform(data):
    decomposer = EMD(data)
    imfs = decomposer.decompose()
    return imfs


def instantaneous_amplitude(data):
    analytical_signal = hilbert(data)
    instantaneous_amplitude = np.abs(analytical_signal)
    return np.array(instantaneous_amplitude)


def instantaneous_frequency(data):
    fs = 1.
    analytical_signal = hilbert(data)
    instantaneous_phase = np.unwrap(np.angle(analytical_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) /(2.*np.pi)*fs)
    return instantaneous_frequency


def get_all_imfs(data):
    imfs = hilbert_huang_transform(data)
    m = len(imfs)
    return m





if __name__ == '__main__':
    path_to_files = "../data/bpfo_data"
    files = get_all_files(path_to_files,type=None)
    data = pd.read_csv(files[0])["bpfo"].values
    imfs = hilbert_huang_transform(data)
    m = get_all_imfs(data)
    print("Total imfs {}".format(m))
    k = 7
    simple_plot(imfs[k])
