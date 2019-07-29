import numpy as np
import numpy
import pywt
from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf
from sklearn import preprocessing
import scipy.stats as stat
from scipy.linalg import sqrtm
from scipy.stats import ks_2samp,iqr, kurtosis
from scipy.spatial.distance import pdist,mahalanobis
import seaborn as sns
import matplotlib.pyplot as plt
from signal_processing import *
from data_processing import get_data, get_all_files



def smooth(x,window_len=11,window='hanning'):
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



def inv_covariance(u,v):
    U = np.array([u,v])
    cov = np.cov(U)
    return np.linalg.inv(cov)

def pdist_distance(u,v,metric):
    """
    compute the mahalonobis distance or
    the disimilarity measure between u
    and v
    """
    #print("in distance 1: metric is {}".format(metric))
    if metric == "mahalanobis":
        cov_uv = inv_covariance(u,v)
        V = np.array(list(map(lambda w: np.var(w),[u,v]))).reshape(-1,1).T
        d = np.matmul(np.matmul(V,cov_uv), V.T)
    else:
        X = np.array([u,v]).T
        d = pdist(X,metric=metric)
    return d


def normalise_min_max(X):
    min_X = np.min(X)
    max_X = np.max(X)
    Z = np.array(list(map(lambda x_i: (x_i-min_X)/(max_X-min_X), X)))
    return Z



def mahalanobis_plot():
    metric = "mahalanobis"
    test_number = "2nd_test"
    path_to_files = "../data/{}".format(test_number)
    files = get_all_files(path_to_files,type=None)
    bearing1=[];bearing2=[];bearing3=[];bearing4=[]
    bearings_list = [bearing1,bearing2,bearing3,bearing4]
    for k, bearing in enumerate(bearings_list):
        ref_data = normalise_min_max(get_data(files[0],k))
        for j, path in enumerate(files[1:]):
            print("flie {} -- Processing date {}".format(j,path))
            #data = normalise_min_max(get_data(path,k))
            dissimilarity = pdist_distance(ref_data,data,metric)
            bearing.append(dissimilarity[0][0])
    d = {"bearing1":bearing1, "bearing2":bearing2,
         "bearing3":bearing3, "bearing4":bearing4
        }
    df = pd.DataFrame(d)
    df.to_csv("dissimilarity_norm_min_max.csv",index=False)




def limit_plot(test_number,method):
    """
    use the wavelet transform to generate two new
    features and use the feature to compute the variance.
    plot the limit
    """
    stats = {"iqr":iqr,"var":np.var,"mahalanobis":mahalanobis}
    statistic = stats[method]
    path_to_files = "../data/{}".format(test_number)
    files = get_all_files(path_to_files,type=None)

    temp=[]
    bearing1=[]; bearing2=[]; bearing3=[]; bearing4=[]
    container =[bearing1,bearing2,bearing3,bearing4]
    #reference_limit_path = files[0]

    for chanel in [0,2,4,6]:
        #reference_limit_data = get_data(ref_path,chanel)
        if method == "mahalanobis":
            ref_path = files[0]
            ref_data = get_data(ref_path,chanel)
            cA_ref, cD_ref = pywt.dwt(ref_data, 'db1')
            files = files[1:]
        for path in files:
            print("processing {}".format(path))
            data = get_data(path,chanel)
            print("teste1")
            cA, cD = pywt.dwt(data, 'db1')
            print("teste2")
            if method == "mahalanobis":
                print("computing mahalanobis for {} bearing{}".format(path,chanel+1))
                result_cA = pdist_distance(cA,cA_ref,method)
                result_cD = pdist_distance(cD,cD_ref,method)
            else:
                result_cA = statistic(cA)
                result_cD = statistic(cD)
            health_index = np.sqrt(result_cA**2 + result_cD**2)
            #print(health_index)
            #exit()
            temp.append(health_index)
            #cD_temp.append(result_cD)
        container[chanel].append(temp)
        temp = []



    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    mx = max(bearing3[0])

    ax1.plot(range(len(bearing3[0])),[mx for _ in range(len(bearing3[0]))],c="orange",label="limit")
    ax1.plot(range(len(bearing1[0])),bearing1[0],c="red",label="bearing1")
    ax1.plot(range(len(bearing2[0])),bearing2[0],c="yellow", label="bearing2")
    ax1.plot(range(len(bearing3[0])),bearing3[0],c="green",label="bearing3")
    ax1.plot(range(len(bearing4[0])),bearing4[0],c="blue",label="bearing4")
    plt.xlabel("date index ")
    plt.ylabel("health index")
    plt.title("Health index and limit for each bearing")

    plt.legend(loc='upper left')
    plt.savefig("bearings_{}_health_bpfi.png".format(method))





def normal_distribution(test_number,metric):
    path_to_files = "../data/{}".format(test_number)
    files = get_all_files(path_to_files,type=None)
    chanel = 2
    distances = []
    reference_data = get_data(files[0],chanel)
    cA_ref, cD_ref = pywt.dwt(reference_data, 'db1')
    #ref_frequency, ref_amp,_,_ = get_peaks(reference_data)
    key = "chanel{}".format(chanel+1)
    for path in files[1:]:
        print("processing {} for {}".format(path,key))
        new_data = get_data(path,3)
        cA_new, cD_new = pywt.dwt(new_data, 'db1')
        #new_freq, new_amp,_,_ = get_peaks(new_data)
        distance = pdist_distance(cD_ref,cD_new,metric)
        print(distance)

        distances.append(distance[0][0])
    lim = len(distances)
    print(max(distances))
    sns.set_style("darkgrid")
    x = range(len(distances))
    lim = 0.02144557665360353
    plt.plot(x,[lim for _ in range(len(x))])
    y = np.array(distances)
    #print(y.ndim)
    #exit()
    x1 = range(len(y))
    plt.plot(x1,y)
    plt.show()


def variance_plot_wavelet(test_number,method):
    """
    use the wavelet transform to generate two new
    features and use the feature to compute the variance.
    """
    stats = {"iqr":iqr,"var":np.var,"mahalanobis":mahalanobis}
    statistic = stats[method]
    path_to_files = "../data/{}".format(test_number)
    files = get_all_files(path_to_files,type=None)
    cA_temp=[]; cD_temp=[]
    bearing1=[]; bearing2=[]; bearing3=[]; bearing4=[]
    container =[bearing1,bearing2,bearing3,bearing4]
    for k, chanel in enumerate([0,2,4,6]):
        if method == "mahalanobis":
            ref_path = files[0]
            ref_data = get_data(ref_path,chanel)
            cA_ref, cD_ref = pywt.dwt(ref_data, 'db1')
            files = files[1:]
        for path in files:
            print("bearing{} processing {}".format(k+1,path))
            data = get_data(path,chanel)
            #print("teste1")
            cA, cD = pywt.dwt(data, 'db1')
            #print("teste2")
            if method == "mahalanobis":
                print("computing mahalanobis for {} bearing{}".format(path,chanel+1))
                result_cA = pdist_distance(cA,cA_ref,method)
                result_cD = pdist_distance(cD,cD_ref,method)
            else:
                result_cA = statistic(cA)
                result_cD = statistic(cD)

            cA_temp.append(result_cA)
            cD_temp.append(result_cD)
        container[k].append([cD_temp, cA_temp])
        cA_temp = []
        cD_temp =[]

    mx_low = np.max(bearing2[0][1])
    mx_high = np.max(bearing2[0][0])

    y1 = np.linspace(0,mx_low,10)
    x1 = [mx_high for _ in range(10)]
    x2 = np.linspace(0,mx_high,10)
    y2 = [mx_low for _ in range(10)]

    eps = 0.01
    y11 = np.linspace(0,mx_low+eps,10)
    x11 = [mx_low+eps for _ in range(10)]

    x22 = np.linspace(0,mx_high+eps,10)
    y22 = [mx_high+eps for _ in range(10)]



    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(bearing1[0][0],bearing1[0][1],c="red",label="bearing1")
    ax1.scatter(bearing2[0][0],bearing2[0][1],c="yellow", label="bearing2")
    #ax1.scatter(bearing3[0][0],bearing3[0][1],c="green",label="bearing3")
    ax1.scatter(bearing4[0][0],bearing4[0][1],c="blue",label="bearing4")
    ax1.plot(x1,y1)
    ax1.plot(x2,y2)
    #ax1.plot(x11,y11)
    #ax1.plot(x22,y22)

    plt.xlabel("{} of hight frequency component".format(method))
    plt.ylabel("{} of low frequency component".format(method))
    plt.title("Bearings health index".format(method))

    plt.legend(loc='upper left')
    ax1.set_ylim(ymin=0)
    ax1.set_xlim(xmin=0)

    #plt.savefig("bearings_{}_bpfi.png".format(method))

    plt.show()







if __name__ == '__main__':
    test_number = "2nd_test"
    path_to_files = "../data/{}".format(test_number)
    files = get_all_files(path_to_files,type=None)
    k = 0
    path = files[0]
    data = get_data(path,k)
    ACF = acf(data,alpha=None)
    plot_acf(ACF)
    #plt.plot(ACF)
    plt.show()

    #test_number = "1st_test"
    #metric = "mahalanobis"
    #method = "var"
    #variance_plot_wavelet(test_number,method)










    #limit_plot(test_number,method)
