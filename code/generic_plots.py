import matplotlib.pyplot as plt
import numpy as np
from hilbert_huang_transform import hilbert_huang_transform


def h_sin(omega):
    n = 10000
    t = np.linspace(-10*np.pi, 10*np.pi, n)
    y = np.sin(omega*t)
    y_h = -np.cos(omega*t)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.plot(t,y)
    plt.plot(t,y_h)
    plt.legend(["sin(t)","Hilbert transform"],loc="best")
    plt.show()


def h_cos(omega):
    n = 10000
    t = np.linspace(-10*np.pi, 10*np.pi, n)
    y = np.cos(omega*t)
    y_h = np.sin(omega*t)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.plot(t,y)
    plt.plot(t,y_h)
    plt.legend(["cos(t)","Hilbert transform"],loc="best")
    plt.show()


def cauchy_pulse(a):
    n = 10000
    t = np.linspace(-10*np.pi, 10*np.pi, n)
    y = a/(a**2 + t**2)
    y_h = t/(a**2 + t**2)
    plt.xlabel("Time")
    plt.ylabel("Cauchy pulse/Hilbert transform")
    plt.plot(t,y)
    plt.plot(t,y_h)
    plt.legend(["Cauchy pulse","Hilbert transform"],loc="best")
    plt.show()


def sinc_pulse(a):
    n = 10000
    t = np.linspace(-10*np.pi, 10*np.pi, n)
    y = np.sin(a*t)/(a*t)
    y_h = (1.-np.cos(a*t))/(a*t)
    plt.xlabel("Time")
    plt.ylabel("sinc pulse/Hilbert transform")
    plt.plot(t,y)
    plt.plot(t,y_h)
    plt.legend(["Sinc pulse","Hilbert transform"],loc="best")
    plt.show()



def sinc_pulse_function(a):
    n = 10000
    t = np.linspace(-10*np.pi, 10*np.pi, n)
    y = np.sin(a*t)/(a*t)
    y_h = (1.-np.cos(a*t))/(a*t)
    return y



if __name__ == '__main__':
    a = 1.5
    data = sinc_pulse_function(a)
    imfs = hilbert_huang_transform(data)
    print(len(imfs))
