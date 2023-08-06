import numpy as np
from .ImpactMatrix import ImpactMatrix
from .sample import cardinal_mapping


def compute_partial_utility(vector, ascending):
    if not ascending:
        vector *= -1
    min_value = np.min(vector)
    max_value = np.max(vector) - min_value
    return (vector - min_value) / max_value


def utility(x_i, w):
    return np.sum(x_i.dot(w))


class SMAA2:
    def __init__(self, impact_matrix, mc_it=10000):
        self.impact_matrix: ImpactMatrix = impact_matrix
        self.m, self.n = impact_matrix.impact_matrix.shape
        self.results = self.init_results()
        self.mc_it = mc_it

    def init_results(self):
        return np.zeros([self.m, self.n])

    def partial_utility_matrix(self):
        impact_matrix = self.impact_matrix.impact_matrix
        criterions = self.impact_matrix.criterions
        X = np.zeros([self.m, self.n])

        for col in range(self.n):
            criterion = criterions[col]
            ascending = criterion.ascending
            cri_values = impact_matrix[:, col]
            if criterion.criterion_type == "ordinal":
                cri_values = cardinal_mapping(cri_values, ascending)
            utility_vector = compute_partial_utility(cri_values, ascending)
            X[:, col] = utility_vector
        return X

    def monte_carlo_simulation(self, X_utility, preference_type, preference_vector):
        w_c = np.zeros([self.m, self.n])
        h = np.zeros([self.m, self.m])
        for i in range(self.mc_it):
            w = preference_type(self.n, preference_vector)
            t = np.array([utility(X_utility[j, :], w) for j in range(self.m)])
            rank = np.argsort(t)
            for j in range(self.m):
                r = rank[j]
                h[r, j] += 1
                if r == (self.m - 1):
                    w_c[j] += w
        return h, w_c

    def compute_w_c_and_b(self, preference_type, preference_vector=None):
        if preference_vector is None:
            preference_vector = []

        X_utility = self.partial_utility_matrix()
        h, w_c = self.monte_carlo_simulation(X_utility, preference_type, preference_vector)
        b = np.zeros([self.m, self.m])
        highest_rank = self.m - 1

        for i in range(self.m):
            if h[highest_rank, i] > 0:
                w_c[i] = w_c[i] / h[highest_rank, i]
            for j in range(self.m):
                b[j, i] = h[j, i] / self.mc_it

        return w_c, b
