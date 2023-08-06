import numpy as np

def sample_weights(n: int, sum_to=1.0) -> list:
    q_j = np.random.uniform(0, 1, n - 1) * sum_to

    q_j = np.sort(q_j)
    q_j = np.insert(q_j, 0, 0)
    q_j = np.insert(q_j, n, sum_to)

    w = [q_j[i] - q_j[i - 1] for i in range(1, n + 1)]
    return w

def cardinal_mapping(m: int, desc=False) -> list:
    c_values = np.random.uniform(0, 1, m - 2)
    c_values = np.append(c_values, [0,1])
    c_values = np.sort(c_values)
    c_values = c_values if not desc else np.flip(c_values)
    return c_values