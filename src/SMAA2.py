import numpy as np
from .ImpactMatrix import ImpactMatrix
from .sample import cardinal_mapping
from numba import njit


def compute_partial_utility(vector, ascending):
    if not ascending:
        vector *= -1
    min_value = np.min(vector)
    max_value = np.max(vector) - min_value
    return (vector - min_value) / max_value

@njit
def utility(x_i, w):
    return x_i @ w

@njit
def monte_carlo_simulation_wc_b(m, n, partial_utility_matrix, mc_it, random, preference_type, preference_vector):
    w_c = np.zeros((m, n))
    h = np.zeros((m, m))

    for i in range(mc_it):
        X_utility = partial_utility_matrix
        w = preference_type(n, preference_vector, random)

        t = [utility(X_utility[j, :], w) for j in range(m)]
        t = np.array(t)
        rank = np.argsort(t)[::-1][:m]
        for j in range(m):
            r = rank[j]
            h[r, j] += 1
            if r == 0:
                w_c[j] += w
    return h, w_c

@njit
def monte_carlo_simulation_p(m, w_c, partial_utility_matrix, mc_it):
    p = np.zeros(m)

    for i in range(mc_it):
        X_utility = partial_utility_matrix
        for j in range(m):
            worse = False
            w = w_c[j]
            t = utility(X_utility[j,:], w)
            for k in range(m):
                if k == j:
                    continue
                if utility(X_utility[k,:], w) > t:
                    worse = True
                    break
            if not worse:
                p[j] += 1

    return p / mc_it


class SMAA2:
    def __init__(self, impact_matrix, mc_it=10000):
        self.impact_matrix: ImpactMatrix = impact_matrix
        self.m, self.n = impact_matrix.impact_matrix.shape
        self.w_c, self.b, self.p = self.init_results()
        self.mc_it = mc_it
        self.random = np.random.default_rng(666)

    def init_results(self):
        return [None, None, None]

    def partial_utility_matrix(self):
        impact_matrix = self.impact_matrix.impact_matrix
        criterions = self.impact_matrix.criterions
        X = np.zeros([self.m, self.n])

        for col in range(self.n):
            criterion = criterions[col]
            ascending = criterion.ascending
            cri_values = impact_matrix[:, col]
            if criterion.criterion_type == "ordinal":
                values_mapped = cardinal_mapping(self.m, self.random, ascending)
                cri_values = [int(c) - 1 for c in cri_values]
                cri_values = values_mapped[cri_values]
            utility_vector = compute_partial_utility(cri_values, ascending)
            X[:, col] = utility_vector
        return X

    def compute_w_c_and_b(self, preference_type, preference_vector=None):
        partial_utility_matrix = self.partial_utility_matrix()
        if preference_vector is None:
            preference_vector = [0]

        preference_vector = np.array(preference_vector)

        try:
            h, w_c = monte_carlo_simulation_wc_b(self.m, self.n, partial_utility_matrix, self.mc_it, self.random,
                                            preference_type, preference_vector)
        except Exception as e:
            print(f"\033[91mException: {e}\033[00m")
            self.w_c, self.b = None, None
            return

        for i in range(self.m):
            if h[0, i] > 0:
                w_c[i] = w_c[i] / h[0, i]
        b = h / self.mc_it

        self.w_c, self.b = w_c, b

    def compute_p(self):
        if self.w_c is None:
            self.p = None
            return

        X_utility = self.partial_utility_matrix()

        self.p = monte_carlo_simulation_p(self.m, self.w_c, X_utility, self.mc_it)




