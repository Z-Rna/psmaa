import numpy as np


def utility(x_i, w):
    return np.sum(x_i.dot(w))

def compute_partial_utility(vector):
    min_value = np.min(vector)
    max_value = np.max(vector) - min_value
    return (vector - min_value) / max_value


def partial_utility_matrix(matrix):
    m, n = matrix.shape
    X = matrix.copy().to_numpy()
    for col in range(n):
        criterium = X[:, col]
        utility_vector = compute_partial_utility(criterium)
        X[:, col] = utility_vector
    return X
