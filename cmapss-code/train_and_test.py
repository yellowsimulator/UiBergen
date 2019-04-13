"""
train and select a best model
"""
import numpy as np
np.seed(10)
#1) check which normalisation method is good for each method
regressors = {"name1":regressor1, "name2:regressor2", ...}
normalisation_score = {}
temp_dict = {}
temp_list = []

def get_better_normalization(X_train):
    """
    return a dictionary where key is a regression method
    and value is a list of dictionary with normalisation
    method and associated score.
    Arguments:
        X_train: training data
    Return:
        a dictionary of the form
        {"method1": [{"namalization": "max-min", "socre": 0.7}, ...], ...}
    """
    for regressor_name, method in regressors.items():
        for norm_name, norm_method in normalisations:
            X_train_norn = norm_method(X_train)
            method.fit(X_train_norn)
            X_cross = get_cross_validation_data(X_train_norn)
            train_score = cross_validation(method, X_cross)
            temp_dict["score"] = train_score
            temp_dict["narmalization"] = norm_name
            temp_list.append(temp_dict)
        normalisation_score[regressor_name] = temp_list
        temp_list = []
        temp_dict = {}
    return normalisation_score


def get_optimum_score(normalisation_score):
    """
    This function returns the best normalisation
    method for a given regression method
    Argument:
        a dictionary of the form
        {"method1": [{"norm1": score1}, ...,], ...}
    Return:
        a dictionary of the sorte:
        {"method": {"norm1": score1}, ...}
    """
    optimum_normalizers = {}
    for regressor_name, score_list in normalisation_score.items():
        sorted_list = sorted(score_list, key=lambda d: d["score"])
        optimum_normalizers[regressor_name] = sorted_list[-1]
    return optimum_normalize


def train_test(regressor,X_train,X_test):
    pass


def get_cross_validation_data(X_train):
    pass


def cross_validation(X_train):
    pass


def get_optimum_trained_regressor():
    pass


def get_optimum_tested_regressor():
    pass
















if __name__ == '__main__':
    main()
