import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

t = np.linspace(0, 6*np.pi, 1000)
signal = 0.3*np.sin(t) + 0.9*np.cos(3*t) + 0.3*np.sin(50*t)

data = pd.DataFrame({"Time":t, "Signal":signal})

ax = sns.lineplot(x="Time", y="Signal", data=data)
plt.show()
