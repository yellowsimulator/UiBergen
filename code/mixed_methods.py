"""
use mixed: wavelet and variance to
detect faulty bearing
"""
import pandas as pd
import numpy as np
import numpy
import pywt
import matplotlib.pyplot as plt
from data_processing import get_data, get_all_files


def inv_covariance(u,v):
    """
    compute the inverse of the covariant matrix
    between two vectore u and v
    """
    U = np.array([u,v])
    cov = np.cov(U)
    return np.linalg.inv(cov)


def dissimilarity(u,v):
    """
    compute the disimilarity measure between u
    and v
    """
    cov_uv = inv_covariance(u,v)
    V = np.array(list(map(lambda w: np.var(w),[u,v]))).reshape(-1,1).T
    d = np.matmul(np.matmul(V,cov_uv), V.T)
    return d


def get_wevelets(data):
    """
    get the detailed and approximate
    wavelet coefficient
    """
    cA, cD = pywt.dwt(data, 'db20')
    return cA, cD


def create_bpfo_failure_data():
    """
    Create a cvs file containing the
    failure data for each bearing.
    """
    cD_temp,cA_temp = [], []
    bearing1=[]; bearing2=[]; bearing3=[]; bearing4=[]
    container = [bearing1,bearing2,bearing3,bearing4]
    test_number = "2nd_test"
    path_to_files = "../data/{}".format(test_number)
    files = get_all_files(path_to_files,type=None)
    for k, bearing in enumerate(container):
        data_ref = get_data(files[0],k)
        cA_ref, cD_ref = get_wevelets(data_ref)
        for j, path in enumerate(files[1:]):
            print("processing bearing{} file {}".format(k+1,j))
            data = get_data(path,k)
            cA, cD = get_wevelets(data)
            cA_dissimilarity = dissimilarity(cA_ref,cA)
            cD_dissimilarity = dissimilarity(cD_ref,cD)
            cA_temp.append(cA_dissimilarity[0][0])
            cD_temp.append(cD_dissimilarity[0][0])
        bearing.append([cD_temp,cA_temp])
        cD_temp,cA_temp = [], []
    d_cD = {"bearing1":bearing1[0][0], "bearing2":bearing2[0][0],
            "bearing3":bearing3[0][0], "bearing4":bearing4[0][0]
            }
    d_cA = {"bearing1":bearing1[0][1], "bearing2":bearing2[0][1],
            "bearing3":bearing3[0][1], "bearing4":bearing4[0][1]
            }
    df_cD = pd.DataFrame(d_cD)
    df_cA = pd.DataFrame(d_cA)
    df_cA.to_csv("csv/cA_dissimilarity_bpfo20.csv")
    df_cD.to_csv("csv/cD_dissimilarity_bpfo20.csv")




def create_bpfi_failure_data():
    """
    Create a cvs file containing the
    failure data for each bearing.
    """
    cD_temp,cA_temp = [], []
    bearing1=[]; bearing2=[]; bearing3=[]; bearing4=[]
    container = [bearing1,bearing2,bearing3,bearing4]
    test_number = "1st_test"
    path_to_files = "../data/{}".format(test_number)
    files = get_all_files(path_to_files,type=None)
    for i, k in enumerate([0,2,4,6]):
        data_ref = get_data(files[0],k)
        cA_ref, cD_ref = get_wevelets(data_ref)
        for j, path in enumerate(files[1:]):
            print("processing bearing{} file {}".format(k+1,j))
            data = get_data(path,k)
            cA, cD = get_wevelets(data)
            cA_dissimilarity = dissimilarity(cA_ref,cA)
            cD_dissimilarity = dissimilarity(cD_ref,cD)
            cA_temp.append(cA_dissimilarity[0][0])
            cD_temp.append(cD_dissimilarity[0][0])
        container[i].append([cD_temp,cA_temp])
        cD_temp,cA_temp = [], []
    d_cD = {"bearing1":bearing1[0][0], "bearing2":bearing2[0][0],
            "bearing3":bearing3[0][0], "bearing4":bearing4[0][0]
            }
    d_cA = {"bearing1":bearing1[0][1], "bearing2":bearing2[0][1],
            "bearing3":bearing3[0][1], "bearing4":bearing4[0][1]
            }
    df_cD = pd.DataFrame(d_cD)
    df_cA = pd.DataFrame(d_cA)
    df_cA.to_csv("csv/cA_dissimilarity_bpfi20.csv")
    df_cD.to_csv("csv/cD_dissimilarity_bpfi20.csv")



def plot_dissimilarity(fault):
    cA_path = "csv/cA_dissimilarity_{}20.csv".format(fault)
    cD_path = "csv/cD_dissimilarity_{}20.csv".format(fault)
    cA_df = pd.read_csv(cA_path)
    cD_df = pd.read_csv(cD_path)
    columns = [ "bearing{}".format(k+1) for k in range(4)]
    bearing1=[]; bearing2=[]; bearing3=[]; bearing4=[]
    container = [bearing1,bearing2,bearing3,bearing4]
    for column, bearing in zip(columns,container):
        cD, cA = list(cD_df[column]), list(cA_df[column])
        bearing.append([cD, cA])

    e = 0.02
    mx_low = np.max(bearing2[0][1]) + 0.02
    mx_high = np.max(bearing2[0][0]) +e

    y1 = np.linspace(0,mx_low,10)
    x1 = [mx_high for _ in range(10)]
    x2 = np.linspace(0,mx_high,10)
    y2 = [mx_low for _ in range(10)]

    eps = 0.1
    y11 = np.linspace(0,mx_low+eps,10)
    x11 = [mx_low+eps for _ in range(10)]

    x22 = np.linspace(0,mx_high+eps,10)
    y22 = [mx_high+eps for _ in range(10)]



    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(bearing1[0][0],bearing1[0][1],label="Bearing1")
    ax1.scatter(bearing2[0][0],bearing2[0][1], label="Bearing2")
    ax1.scatter(bearing3[0][0],bearing3[0][1],c="red",label="Bearing3 with BPFI defect")
    if fault == "bpfo":
        ax1.scatter(bearing4[0][0],bearing4[0][1],c="blue",label="Bearing4")
    ax1.plot(x1,y1,color="green", label="Healthy operating region")
    ax1.plot(x2,y2,color="green")





    plt.xlabel("Dissimilarity measure of detailed coefficients")
    plt.ylabel("Dissimilarity measure of approximate coefficients")
    if fault == "bpfo":
        title = "Ball Pass Frequency Outer race defect in bearing1"
    elif fault == "bpfi":
        title = "Ball Pass Frequency inner race defect in bearing3"
    else:
        title = "Roller element defect in bearing4"
    plt.title("{}".format(title))
    plt.legend(loc='upper left')
    ax1.set_ylim(ymin=0)
    ax1.set_xlim(xmin=0)
    plt.show()
    #plt.savefig("bearings_{}_health_bpfi.png".format(method))
    #plt.savefig("bearings_{}_health_bpfi.png".format(method))







if __name__ == '__main__':
    fault = "bpfi"
    #create_bpfo_failure_data()
    #create_bpfi_failure_data()
    plot_dissimilarity(fault)
