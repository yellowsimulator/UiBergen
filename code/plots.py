import numpy as np
import matplotlib.pyplot as plt
#from data_processing import get_all_files,get_data
#from signal_processing import get_envelop_spectrum,get_peaks



#t = np.linspace(-6,6,10000)
#y = np.sin(t) + 3*np.cos(2*t) + 0.3*np.sin(30*t) + 0.7*np.cos(5*t)
f = [1,2,5,30]
A = [1,3,0.7,0.3]
plt.scatter(f,A)
plt.xlabel("Frequency axis")
plt.ylabel("Amplitude")
#plt.xlabel("Time axis")
#plt.ylabel("Magnitude")
#plt.title(r"$sin(t) + 3cos(2t) + 0.3sin(30t) + 0.7cos(5t)$",fontsize=16, color='gray')
#plt.show()
plt.savefig("../articles/freq.png")

'''def simple_plot(x,y,x1,y1,x2,y2,title=None,xlabel=None,ylabel=None):
    plt.plot(x,y)
    plt.plot(x1,y1)
    plt.plot(x2,y2)
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    plt.legend(["envelop spectrum", "bpfo(236.4 Hz)", "bpfo harmonics (2bpfo)"],loc='upper left')

    plt.show()


if __name__ == '__main__':
    test_number = "2nd_test"
    path_to_files = "../data/{}".format(test_number)
    files = get_all_files(path_to_files,type=None)
    path = files[0]
    chanel = 0
    accelaration = get_data(path,chanel)
    freq, amplitude = get_envelop_spectrum(accelaration)
    freq_peaks,amp_peaks,_,_ = get_peaks(accelaration)
    title="Envelop spectrum and bpfo frequency with its harmonics"
    xlabel="Frequency in Hz"
    ylabel="Amplitude"
    increment = 1./20480.
    x = np.linspace(0,1,20480)
    lim = 500

    x1 = [236.4 for _ in range(10)]
    y1 = np.linspace(0,0.052,10)
    x2 = [2*236.4 for _ in range(10)]
    y2 = np.linspace(0,0.052,10)
    simple_plot(freq[:lim],amplitude[:lim],x1,y1,x2,y2,title=title,xlabel=xlabel,ylabel=ylabel)
'''
