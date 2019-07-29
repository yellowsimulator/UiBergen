import numpy as np
import numpy
import seaborn as sns
from pyhht.emd import EMD

import statsmodels.api as sm
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
import dateutil.parser
from statsmodels.tsa.seasonal import seasonal_decompose
#import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from sklearn import preprocessing
from peak_detect import *
from get_data import *
from data_processing import *






def smooth(x,window_len=5,window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        print("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        print("Input vector needs to be bigger than window size.")


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        print("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=numpy.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='valid')
    return y


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
    amplitude = 2.0/signal_length * np.abs(yf[:signal_length//2])
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



def BPFI(date,k):
	faults = {"BPFI":236.}
	freq_peaks,amp_peaks,freq,amp = get_peaks(data,k)
	bpfi = list(filter(lambda f: round(f,0)==faults["BPFI"] ,freq_peaks))
	bpfi_amp = []
	if len(bpfi) == 1:
		idx = list(freq).index(bpfi[0])
		bpfi_amp = [amp[idx]]
	return bpfi, bpfi_amp



def RDF(date,k):
	faults = {"RDF":280.4}
	freq_peaks,amp_peaks,freq,amp = get_peaks(data,k)
	rdf = list(filter(lambda f: round(f,0)==faults["RDF"] ,freq_peaks))
	rdf_amp = []
	if len(rdf) == 1:
		idx = list(freq).index(rdf[0])
		rdf_amp = [amp[idx]]
	return rdf, rdf_amp



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
	"""
	#freq_peaks,amp_peaks,freq,amp = get_peaks(data)
	freq_peaks,amp_peaks = get_envelop_spectrum(data)
	amp = amp_peaks
	freq = freq_peaks
	bpfi = list(filter(lambda f: round(f,0) == round(fault_freq,0) ,freq_peaks))
	bpfi_amp = []
	if len(bpfi) == 1:
		idx = list(freq).index(bpfi[0])
		bpfi_amp = amp[idx]
		return bpfi[0], bpfi_amp
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



def plot_bpfo():
	test_number = "2nd_test"
	path_to_files = "../data/{}".format(test_number)
	files = get_all_files(path_to_files,type=None)
	bearing1=[];bearing2=[];bearing3=[];bearing4=[]
	bearings_list = [bearing1,bearing2,bearing3,bearing4]
	bpfo_freq = 236.4
	for bearing_number in [0,1,2,3]:
		for path in files:
			print("processing {}".format(path))
			data = get_data(path,bearing_number)
			freq, amplitude = get_fault_frequency(data,bpfo_freq)
			if amplitude is not None:
				bearings_list[bearing_number].append(amplitude)
	d = {"bearing1":bearing1, "bearing2":bearing2,
		"bearing3":bearing3, "bearing4":bearing4
		}
	df = pd.DataFrame(d)
	df.to_csv("bpfo_amp_just_envelop.csv",index=False)



def plot_rdf():
	test_number = "1st_test"
	path_to_files = "../data/{}".format(test_number)
	files = get_all_files(path_to_files,type=None)
	bearing1=[];bearing2=[];bearing3=[];bearing4=[]
	bearings_list = [bearing1,bearing2,bearing3,bearing4]
	rdf_freq = 280.4
	for k, bearing_number in enumerate([0,2,4,6]):
		for j, path in enumerate(files):
			print("bearing {} sample {} ... processing {}".format(k+1,j,path))
			data = get_data(path,bearing_number)
			freq, amplitude = get_fault_frequency(data,rdf_freq)
			if amplitude is not None:
				bearings_list[k].append(amplitude)
	d = {"bearing1":bearing1, "bearing2":bearing2,
		"bearing3":bearing3, "bearing4":bearing4
		}
	df = pd.DataFrame(d)
	df.to_csv("rdf_amp_just_envelop.csv",index=False)



def plot_bpfi():
	test_number = "1st_test"
	path_to_files = "../data/{}".format(test_number)
	files = get_all_files(path_to_files,type=None)
	bearing1=[];bearing2=[];bearing3=[];bearing4=[]
	bearings_list = [bearing1,bearing2,bearing3,bearing4]
	bpfi_freq = 296.8
	for k, bearing_number in enumerate([0,2,4,6]):
		for path in files:
			print("processing {}".format(path))
			data = get_data(path,bearing_number)
			freq, amplitude = get_fault_frequency(data,bpfi_freq)
			if amplitude is not None:
				bearings_list[k].append(amplitude)
	d = {"bearing1":bearing1, "bearing2":bearing2,
		"bearing3":bearing3, "bearing4":bearing4
		}
	df = pd.DataFrame(d)
	df.to_csv("bpfi_amp_just_envelop.csv",index=False)







def some_job():
	import matplotlib
	import os
	matplotlib.use('Agg')
	import matplotlib.pyplot as plt
	path_to_files = "../data/1st_test"
	files = get_all_files(path_to_files,type=None)
	fault_freqs = {"bpfo":236.4, "bpfi":296.8, "rdf":280.4}
	indexes = list(fault_freqs.keys())
	temp_container = []
	json_data = {}
	file_name = "labeled_data_test1.json"
	#get bearing number k
	for k in [0,2,4,6]:
		#os.mkdir("{}".format(k+1))
		key = "chanel{}".format(k+1)
		value = {}
		for fault_name in fault_freqs:
			fault_freq = fault_freqs[fault_name]
			for path in files:
				print("processing {} for {}".format(path,key))
				data = get_data(path,k)
				#data = scale_data(data)
				bpfi, amplitude = get_fault_frequency(data,fault_freq)
				if amplitude is not None:
					temp_container.append(path)
			plt.plot(temp_container)
			plt.ylim([0,0.005])
			plt.title("amplitude for {} and {}".format(key,fault_name))
			plt.savefig("{}/{}_{}.png".format(k+1,key,fault_name))
			plt.close()
			temp_container = []
			#averge_amp = np.mean(temp_container)
			value[fault_name] = temp_container
			temp_container = []
		json_data[key] = value
	print("saving data to json file")
	create_json_data(json_data,file_name)


def date_parser(t):
    timestamp = dateutil.parser.parse(t, dayfirst=True).timestamp()
    result = pd.to_datetime(timestamp,unit='s')
    return result


def plot_and_save_bearing():
    df = pd.read_csv("bpfo_amp_just_envelop.csv")
    path_to_files = "../data/2nd_test"
    files = get_all_files(path_to_files,type=None)
    dates = list(map(lambda t: " ".join(["/".join(t.split("/")[-1].split(".")[:3]),
     ":".join(t.split("/")[-1].split(".")[3:])]),
    files))
    new_date = list(map(lambda d: date_parser(d),dates))
    #t = dateutil.parser.parse(dates[0], dayfirst=True).timestamp()
    #print(new_date[0])
    #exit()
    #df["date"] = new_date
    #df.to_csv("bpfo_amp_just_envelop_date.csv")
    #df = pd.read_csv("bpfo_amp_just_envelop_date.csv",index_col=0)
    #df.set_index("date",inplace=True, drop=True)
    #print(df)
    #exit()
    #dates = list(map(lambda t: t))

    size = 1
    df["bearing1"].rolling(size).mean().plot(figsize=(20,10), linewidth=5, fontsize=20,color="red",label="bearing1 with bpfo defect")
    df["bearing2"].rolling(size).mean().plot(figsize=(20,10), linewidth=5, fontsize=20,label="bearing2")
    df["bearing3"].rolling(size).mean().plot(figsize=(20,10), linewidth=5, fontsize=20,label="bearing3")
    df["bearing4"].rolling(size).mean().plot(figsize=(20,10), linewidth=5, fontsize=20,label="bearing4")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("")
    plt.legend(loc='upper left')
    plt.show()

    exit()

    bearing1 = df["bearing1"].values
    bearing2 = df["bearing2"].values
    bearing3 = df["bearing3"].values
    bearing4 = df["bearing4"].values
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    #mx = max(bearing3[0])
    y = smooth(bearing1,window_len=11,window='hanning')

    #ax1.plot(range(len(bearing3)),[mx for _ in range(len(bearing3[0]))],c="orange",label="limit")
    plt.plot(range(len(y)),y)
    plt.show()
    '''ax1.plot(range(len(bearing2)),bearing2,c="yellow", label="bearing2")
    ax1.plot(range(len(bearing3)),bearing3,c="green",label="bearing3")
    ax1.plot(range(len(bearing4)),bearing4,c="blue",label="bearing4")
    plt.xlabel("Date index")
    plt.ylabel("Defect amplitude")
    plt.title("Ball Pass Frequency Outer race defect amplitude")

    plt.legend(loc='upper left')
    plt.savefig("bpfo_amp.png")'''

import pywt
def get_wevelets(data):
    """
    get the detailed and approximate
    wavelet coefficient
    """
    #for _ in range(nb):
    cA, cD = pywt.dwt(data, 'db20')
        #data = cA
    return cA, cD




if __name__ == '__main__':
    #plot_and_save_bearing()
    #exit()
    path_to_files = "../data/1st_test"
    files = get_all_files(path_to_files,type=None)
    colors = ["red","blue","green","yellow"]
    path = files[10]
    _, y = get_wevelets(get_data(path,0))

    decomposer = EMD(y)
    d = {}
    #imfs1 = decomposer1.decompose()
    #decomposer = EMD(imfs[0])
    imfs = decomposer.decompose()
    #print(len(imfs))
    #exit()
    for j, series in enumerate(imfs):
        d["imf{}".format(j+1)] = imfs[j]

    t = np.linspace(0,1,len(imfs[0]))
    d["Time"] = t
    df = pd.DataFrame(d)
    #df = pd.DataFrame({"Time":x,"imf1":imfs[0]})
    import seaborn as sns; sns.set()
    import matplotlib.pyplot as plt
    #fmri = sns.load_dataset("fmri")
    for name in d:
        print("plotting {}".format(name))
        sns.lineplot(x="Time", y=name, data=df)
        plt.savefig("imf/{}.png".format(name))
        plt.close()
    #sns.lineplot(x="Time", y="imf{}".format(2), data=df)
    #sns.lineplot(x="Time", y="imf{}".format(4), data=df)
    #plt.show()

    exit()
    #j = 0
    m = len(files)
    j = m-1
    path = files[j]

    for i,k in enumerate([0,2,4]):
        data = get_data(path,k)
        #nb = 1
        cA, cD = get_wevelets(data)
        #fault_freq = 236.4
        #fault_freq = 2000/60.
        #lim = 20000
        plt.scatter(cA,cD,c=colors[i],label="bearing{}".format(i+1))
    plt.legend(loc='upper left')
    plt.show()
    exit()
    bpfi, amplitude = get_fault_frequency(data,fault_freq)
    print(bpfi,amplitude)









    #




	#
