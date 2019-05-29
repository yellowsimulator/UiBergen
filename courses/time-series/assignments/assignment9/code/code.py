import matplotlib.pyplot as plt
import numpy as np

def cj(t,j):
    y = np.cos((2*np.pi/21)*t)
    return y

def sj(t,j):
    y = np.sin((2*np.pi/21)*t)
    return y


if __name__ == '__main__':

    t = np.linspace(1,22,21)
    for j in [1,5,10]:
        y = sj(t,j)
        plt.plot(t,y)
        plt.title("sj for j = {}".format(j))
        plt.xlabel("t")
        plt.ylabel("s{}(t)".format(j))
        plt.savefig("../note/sj{}.png".format(j))
        plt.close()
