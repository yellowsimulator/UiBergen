import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from data_processing import get_data, get_all_files

def inv_covariance(u,v):
    """
    compute the inverse of the covariant matrix
    between two vectore u and v
    """
    U = np.array([u,v])
    cov = np.cov(U)
    return np.linalg.inv(cov)


def dissimilarity_measure(u,v):
    """
    compute the disimilarity measure between u
    and v
    """
    cov_uv = inv_covariance(u,v)
    V = np.array(list(map(lambda w: np.var(w),[u,v]))).reshape(-1,1).T
    d = np.matmul(np.matmul(V,cov_uv), V.T)
    return d

def dissimilarity(test_number):
    path_to_files = "../data/{}".format(test_number)
    file_paths = get_all_files(path_to_files,type=None)
    bearing1=[]; bearing2=[]; bearing3=[]; bearing4=[]
    container = [bearing1,bearing2,bearing3,bearing4]
    if test_number == "1st_test":
        chanels = [0,2,4,6]
    if test_number == "2nd_test":
        chanels = [0,1,2,3]
    for k, chanel in enumerate(chanels):
        ref_path = file_paths[0]
        for j,path in enumerate(file_paths[1:]):
            print("processing bearing {} files {}".format(chanel+1,j))
            ref_data = get_data(ref_path,chanel)
            data = get_data(path,chanel)
            d = dissimilarity_measure(ref_data, data)
            container[k].append(d[0][0])
    d = {"bearing1":bearing1, "bearing2":bearing2,
            "bearing3":bearing3, "bearing4":bearing4
        }
    df = pd.DataFrame(d)
    df.to_csv("csv/{}_statistical_method.csv".format(test_number))



def plot_dissimilarity(test_number):
    path = "csv/{}_statistical_method.csv".format(test_number)
    df = pd.read_csv(path)
    size = 5
    df["bearing1"].rolling(size).mean().plot(figsize=(20,10), linewidth=5, fontsize=20,label="Bearing1")
    df["bearing2"].rolling(size).mean().plot(figsize=(20,10), linewidth=5, fontsize=20,label="Bearing2")
    df["bearing3"].rolling(size).mean().plot(figsize=(20,10), linewidth=5, fontsize=20,color="red",label="Bearing3 with ball pass frequency inner race defect")
    df["bearing4"].rolling(size).mean().plot(figsize=(20,10), linewidth=5, fontsize=20,label="Bearing4")
    plt.xlabel("Date index")
    plt.ylabel("Dissimilarity measure")
    plt.title("Dissimilarity measure for four different bearings. Rolling average plot")
    plt.legend(loc='upper left')
    plt.show()




if __name__ == '__main__':
    test_number = "1st_test"
    plot_dissimilarity(test_number)
    #dissimilarity(test_number)
