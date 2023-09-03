import numpy as np
from numba import njit

@njit
def sample_weights(n: int, rand_gen, sum_to=1.0) -> list:
    q_j = rand_gen.uniform(0, 1, n - 1) * sum_to

    q_j = np.append(q_j, [0,1])
    q_j = np.sort(q_j)

    w = [q_j[i] - q_j[i - 1] for i in range(1, n + 1)]
    return w

@njit
def cardinal_mapping(m: int, rand_gen, desc=False) -> list:
    c_values = rand_gen.uniform(0, 1, m - 2)
    c_values = np.append(c_values, [0,1])
    c_values = np.sort(c_values)
    c_values = c_values if not desc else np.flip(c_values)
    return c_values