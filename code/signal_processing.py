import numpy as np
from scipy.signal import butter, lfilter, freqz
import pandas as pd
from scipy.fftpack import fft,ifft, hilbert
import time
from datetime import datetime, date
import math
from scipy.signal import find_peaks
import scipy
from scipy.integrate import simps
import difflib
from scipy.integrate import simps
#import matplotlib.pyplot as plt
from sklearn import preprocessing
from peak_detect import *
from get_data import *
from data_processing import *
def butter_bandpass(lowcut, highcut, sampling_freq, order=5):
	"""
	Band pass filter parameters:
	-lowcut: Low cutoff frequency
	-highcut: High cutoff frequency
	-fs: sampling frequency, Hz
	-order: order of fitler
	"""
	nyq = 0.5 * sampling_freq
	low = lowcut / nyq
	high = highcut / nyq
	b, a = butter(order, [low, high], btype='band')
	return b, a

def butter_bandpass_filter(data, lowcut, highcut, sampling_freq, order=5):
	"""
	Filter data along one-dimension with a bandpass filter:
	-data: data to be analysed
	-lowcut: Low cutoff frequency
	-highcut: High cutoff frequency
	-fs: sampling frequency, Hz
	-order: order of fitler
	"""

	b, a = butter_bandpass(lowcut, highcut, sampling_freq, order=order)
	y = lfilter(b, a, data)
	return y

## Low pass filter:
def butter_lowpass(cut, fs, order=5):
	"""
	Low pass filter parameters:
	-lowcut: Low cutoff frequency
	-fs: sampling frequency, Hz
	-order: order of fitler
	"""
	nyq = 0.5 * fs
	high = cut / nyq
	b, a = butter(order,  high, btype='low')
	return b, a

def butter_lowpass_filter(data, cut, fs, order=5):
	"""
	Filter data along one-dimension with a lowpass filter:
	-data: data to be analysed
	-lowcut: Low cutoff frequency
	-fs: sampling frequency, Hz
	-order: order of fitler
	"""
	b, a = butter_lowpass(cut, fs, order=order)
	y = lfilter(b, a, data)
	return y

## Envelop detection
def get_envelop(data):
	"""
	using Hilbert for envelop detection:
	data: data to be analysed
	"""
	hilbert_transform = hilbert(data)
	envelop = np.sqrt(data**2 + hilbert_transform**2)
	return envelop



def get_fft(signal,period,sampling_interval):
    signal_length = len(signal)
    sampling_freq = signal_length/period
    k = np.arange(signal_length)
    two_side_freq = k/period
    one_side_freq = two_side_freq[range(int(signal_length/2))]
    yf = fft(signal)
    freq = np.linspace(0.0, 1.0/(2.0*sampling_interval), signal_length/2)
    amplitude = 2.0/signal_length * np.abs(yf[:signal_length//2])/9.8
    amplitude[0] = 0
    return freq,amplitude




def get_envelop_spectrum(accelaration):
    lowcut = 2000
    highcut = 9990
    # sampling_freq = 9600
    # period = 2999.895996/1000
    # sampling_interval = 0.104166/1000
    sampling_freq = 20000
    period = 1
    sampling_interval = 1./20480
    y = butter_bandpass_filter(accelaration,lowcut,highcut,sampling_freq,order=5)
    envelop = get_envelop(y)
    low_pass = butter_lowpass_filter(envelop,2000,sampling_freq,order=5)
    freq, amplitude = get_fft(low_pass,period,sampling_interval)
    return freq, amplitude





def get_peaks(data):
	#data = get_data(date,k)
	freq, amp = get_envelop_spectrum(data)
	peaks_index = detect_peaks(amp[:500])
	freq_peaks = freq[peaks_index]
	amp_peaks = amp[peaks_index]
	return freq_peaks,amp_peaks,freq,amp


def BPFO(date,k):
	faults = {"BPFO":236.}
	freq_peaks,amp_peaks,freq,amp = get_peaks(data,k)
	bpfo = list(filter(lambda f: round(f,0)==faults["BPFO"] ,freq_peaks))
	bpfo_amp = []
	if len(bpfo) == 1:
		idx = list(freq).index(bpfo[0])
		bpfo_amp = [amp[idx]]
	return bpfo, bpfo_amp


def get_bpfo(data):
	"""
	this is the dupicate of the function
	BPFO. Used for testing.
	"""
	faults = {"BPFO":236.4}
	freq_peaks,amp_peaks,freq,amp = get_peaks(data)
	bpfo = list(filter(lambda f: round(f,0)==round(faults["BPFO"],0) ,freq_peaks))
	bpfo_amp = []
	if len(bpfo) == 1:
		idx = list(freq).index(bpfo[0])
		bpfo_amp = [amp[idx]]
		return bpfo, bpfo_amp
	else:
		return None, None


def get_fault_frequency(data,fault_freq):
	"""
	This function returns the bpfi frequency
	and the corresponding amplitude.

	Arguments:
	----------
	data:
	array containing the vibration time signal.

	fault_freq:
	fault frequency in HERTZ (cycle per second)

	Returns:
	--------
	None or fault frequency and amplitude
	"""
	freq_peaks,amp_peaks,freq,amp = get_peaks(data)
	bpfi = list(filter(lambda f: round(f,0) == round(fault_freq,0) ,freq_peaks))
	bpfi_amp = []
	if len(bpfi) == 1:
		idx = list(freq).index(bpfi[0])
		bpfi_amp = [amp[idx]]
		return bpfi, bpfi_amp
	else:
		return None, None



def get_harmonics(harmonics_name,date,k):
	names = {"BPFO":236.}
	freq_peaks,amp_peaks,freq,amp = get_peaks(date,k)
	harmonics = list(filter(lambda f: round(f,0)%names[harmonics_name] == 0.
	,freq_peaks))
	amplitude = []
	if len(harmonics) >= 1:
		indexes = list(map(lambda f: list(freq).index(f), harmonics))
		amplitude = list(map(lambda k: amp[k], indexes))
	return harmonics,amplitude



def get_rms(k):
	# k = 0 # first bearing
	dates = get_dates()[:-9]
	RMS = list(map(lambda date: rms(get_data(date,k)), dates))
	return RMS, dates




def rms(data):
	m = len(data)
	return np.sqrt(sum(data**2)/m)



def save_data(k):
	bpfo,amp = get_bpfo_amplitude(k)
	d1 = {'amplitude':amp}
	d2 = {'amplitude':amp, 'bpfo':bpfo}

	df1 = pd.DataFrame.from_dict(d1)
	df2 = pd.DataFrame.from_dict(d2)
	path1 = "../data/2nd_test/bearing{}_amp.csv".format(k+1)
	path2 = "../data/2nd_test/bearing{}_bpfo_amp.csv".format(k+1)
	df1.to_csv(path1,index=False)
	df2.to_csv(path2,index=False)


def get_overall_accel(k):
	path = "../data/2nd_test/bearing{}.csv".format(k+1)
	df = pd.read_csv(path)
	dates,values = list(df["date"]),df["rms"].values
	return dates,values



def get_bpfo_amplitude(k):
	dates = get_dates()[:-9]
	bpfo_list = list(map(lambda date: BPFO(date,k),dates))
	new_list = list(filter(lambda data: len(data[0])==1, bpfo_list))
	bpfo = list(map(lambda data: data[0][0], new_list))
	amp = list(map(lambda data: data[1][0], new_list))
	return bpfo,amp


def get_bpfo_amps(k):
	"""
	This function is maybe not neccessary
	"""
	path = "../data/2nd_test/bearing{}_amp.csv".format(k+1)
	values = pd.read_csv(path)["amplitude"].values
	return values



def get_imfs(data):
	pass




if __name__ == '__main__':
	path_to_files = "../data/3rd_test"
	files = get_all_files(path_to_files,type=None)
	fault_freqs = {"bpfo":236.4, "bpfi":296.8, "rdf":280.4}
	indexes = list(fault_freqs.keys())
	temp_container = []
	json_data = {}
	file_name = "3rd_test_len2.json"
	#get bearing number k
	for k in [0,1,2,3]:
		key = "bearing{}".format(k+1)
		value = {}
		for fault_name in fault_freqs:
			fault_freq = fault_freqs[fault_name]
			for path in files:
				print("processing {} for {}".format(path,key))
				data = get_data(path,k)
				#data = scale_data(data)
				bpfi, amplitude = get_fault_frequency(data,fault_freq)
				if amplitude is not None:
					temp_container.append(amplitude[0])
			averge_amp = len(temp_container)
			value[fault_name] = averge_amp
			temp_container = []
		json_data[key] = value
	print("saving data to json file")
	create_json_data(json_data,file_name)









	#
