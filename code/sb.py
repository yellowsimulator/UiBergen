import pandas as pd
import seaborn as sns
from data_processing import *
import numpy as np
#import matplotlib.pyplot as plt




def f(t,w):
    return np.cos(w*t)

def grad_f(t,w):
    f = np.cos(w*t)
    return np.gradient(f)

def frequency(t,w):
    f = np.cos(w*t)
    freq = np.gradient(f)/(1+np.cos(w*t)*np.cos(w*t))
    return freq

def frequency1(t,w):
    freq = (-w*np.sin(w*t))/(1+np.cos(w*t)*np.cos(w*t))
    return freq



w = 3
t = np.linspace(0,10*np.pi,10000)
#plt.plot(t,frequency1(t,w))
#plt.legend(["f","frequency"])
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
df = pd.DataFrame({"Time":t,"Frequency values":frequency1(t,w)})
ax = sns.lineplot(x="Time", y="Frequency values".format(1), data=df)
#plt.title("function f")
plt.show()
exit()
#data=np.random.randn(90, 5)
#print(data.shape)
#exit()
path_to_files = "../data/1st_test"
files = get_all_files(path_to_files,type=None)
colors = ["red","blue","green","yellow"]
path = files[10]
y = get_data(path,0)
decomposer = EMD(y)
d = {}
imfs = decomposer.decompose()
#print(len(imfs))
#exit()
for j, series in enumerate(imfs):
    d["imf{}".format(j+1)] = imfs[j]

x = range(len(imfs[0]))
d["Time"] = x
df = pd.DataFrame(d)

columns = ["imf{}".format(k+1) for k in range(len(imfs))]
df = pd.DataFrame(
    data=np.random.randn(90, len(imfs)),
    columns=pd.Series(columns, name="imf"),
    index=pd.date_range("2015-01-01", "2015-03-31",
                         name="date"))


#print(df)
#exit()
df = df.cumsum(axis=0).stack().reset_index(name="val")
def dateplot(x, y, **kwargs):
    ax = plt.gca()
    data = kwargs.pop("data")
    data.plot(x=x, y=y, ax=ax, grid=False, **kwargs)

g = sns.FacetGrid(df, col="imf", col_wrap=2, height=3.5)
g = g.map_dataframe(dateplot, "date", "val")

plt.show()
