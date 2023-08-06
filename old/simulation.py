import numpy as np
from tqdm import tqdm


def monte_carlo_simulation(it, m, n, X_utility, preference_type, preference_vector=[]):
    from old.utility_utils import utility
    w_c = np.zeros([m, n])
    h = np.zeros([m, m])
    for i in tqdm(range(it)):
        w = preference_type(n, preference_vector)
        t = np.array([utility(X_utility[j, :], w) for j in range(m)])
        rank = np.argsort(t)
        for j in range(m):
            r = rank[j]
            h[r, j] += 1
            if r == (m - 1):
                w_c[j] += w
    return h, w_c


def alg_3(X, it: int, preference_type, preference_vector=[]):
    from old.utility_utils import partial_utility_matrix
    m, n = X.shape
    X_utility = partial_utility_matrix(X)

    h, w_c = monte_carlo_simulation(it, m, n, X_utility, preference_type, preference_vector)
    b = np.zeros([m, m])
    highest_rank = m - 1
    for i in range(m):
        if h[highest_rank, i] > 0:
            w_c[i] = w_c[i] / h[highest_rank, i]
        for j in range(m):
            b[j, i] = h[j, i] / it

    return w_c, b
