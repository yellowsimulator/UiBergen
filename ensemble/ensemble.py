from sklearn import *
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_friedman1
from signal_processing import *
X,Y = make_friedman1(n_samples=100, random_state=0, noise=1.0)
print(X.shape)

base_classifier = KNeighborsClassifier()
bagging = BaggingClassifier(base_classifier)
