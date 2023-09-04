import numpy as np
from .ImpactMatrixTri import ImpactMatrixTri
from .ProfileMatrix import ProfileMatrix
from numba import njit


def concordance_index(a, b, q_j, p_j, ascending):
    diff = b - a
    if not ascending:
        diff *= -1
    if diff < q_j:
        return 1
    elif diff >= p_j:
        return 0
    else:
        return (p_j - diff) / (p_j - q_j)


def discordance_index(a, b, p_j, v_j, ascending):
    diff = b - a
    if not ascending:
        diff *= 1
    if diff < p_j:
        return 0
    elif diff >= v_j:
        return 1
    else:
        return ((diff - p_j) / (v_j - p_j))

@njit
def credibility_index(dj, C):
    if np.all((dj == 0.)):
        return C
    if np.any((dj == 1.)):
        return 0.
    diff = 1. - C
    result = C
    for d in dj:
        if d > C:
            result *= (1 - d) / diff
    return result

@njit
def compute_global_concordance_indexes(cj_ab, cj_ba, weights):
    weights = weights
    C_ab = np.sum(cj_ab * weights[:, None, None], axis=0) / np.sum(weights)
    C_ba = np.sum(cj_ba * weights[:, None, None], axis=0) / np.sum(weights)
    return C_ab, C_ba

@njit
def outranks(lambda_value, rand_gen, dj, C):
    if (lambda_value[0] == lambda_value[1]):
        l = lambda_value[0]
    else:
        if (lambda_value[0] > lambda_value[1]):
            raise Exception("The lower bound of lambda interval is over the high bound.")
        l = lambda_value[0] + rand_gen.uniform(0, 1) * (lambda_value[1] - lambda_value[0])
    return credibility_index(dj, C) >= l

@njit
def preferred(lambda_value, rand_gen, dj, C):
    return outranks(lambda_value, rand_gen, dj[0], C[0]) and not outranks(lambda_value, rand_gen, dj[1], C[1])

@njit
def optimistic_procedure(m, b, lambda_value, C_ab, C_ba, dj_ab, dj_ba, rand_gen):
    category_mapper = np.zeros((m))
    for i in range(m):
        for j in range(b):
            if j == b - 1:
                category_mapper[i] = b
            C = C_ba[i, j], C_ab[i, j]
            dj = dj_ba[:, i, j], dj_ab[:, i, j]
            if preferred(lambda_value, rand_gen, dj, C):
                category_mapper[i] = j
                break
    return category_mapper

@njit
def pessimistic_procedure(m, b, lambda_value, C_ab, dj_ab, rand_gen):
    category_mapper = np.zeros((m))
    for i in range(m):
        for j in range(b - 1, -1, -1):
            C = C_ab[i, j]
            dj = dj_ab[:, i, j]
            if outranks(lambda_value, rand_gen, dj, C):
                category_mapper[i] = j + 1
                break
    return category_mapper

@njit
def monte_carlo_simulation(m, n, b, mc_it, optimistic, lambda_value, rand_gen, cj_ab, cj_ba, dj_ab, dj_ba, preference_type,
                           preference_vector):
    h = np.zeros((m, b + 1))
    for i in range(mc_it):
        w = preference_type(n, preference_vector, rand_gen)
        C_ab, C_ba = compute_global_concordance_indexes(cj_ab, cj_ba, w)
        if optimistic:
            categories = optimistic_procedure(m, b, lambda_value, C_ab, C_ba, dj_ab, dj_ba, rand_gen)
        else:
            categories = pessimistic_procedure(m, b, lambda_value, C_ab, dj_ab, rand_gen)

        for j in range(m):
            cat = int(categories[j])
            h[j, cat] += 1
    return h


class SMAATri:
    def __init__(self, impact_matrix, profile_matrix, lambda_value, mc_it=10000, optimistic=True):
        self.impact_matrix: ImpactMatrixTri = impact_matrix
        self.profile_matrix: ProfileMatrix = profile_matrix
        self.m, self.n = impact_matrix.impact_matrix.shape
        self.b = profile_matrix.data.shape[1]
        self.mc_it: int = mc_it
        self.pi = self.init_results()
        self.lambda_value = np.array(lambda_value)
        self.optimistic = optimistic
        self.random = np.random.default_rng(666)

    def init_results(self):
        return None

    def compute_concordance_indexes(self):
        cj_ab = np.zeros([self.n, self.m, self.b])
        cj_ba = np.zeros([self.n, self.m, self.b])
        for j in range(self.n):
            cri = self.impact_matrix.criterions[j]
            ascending = cri.ascending
            q_j, p_j = cri.q, cri.p
            for i_a in range(self.m):
                a = self.impact_matrix.impact_matrix[i_a, j]
                for i_b in range(self.b):
                    b = self.profile_matrix.data[j, i_b]
                    cj_ab[j, i_a, i_b] = concordance_index(a, b, q_j, p_j, ascending)
                    cj_ba[j, i_a, i_b] = concordance_index(b, a, q_j, p_j, ascending)
        return cj_ab, cj_ba

    def compute_discordance_index(self):
        dj_ab = np.zeros([self.n, self.m, self.b])
        dj_ba = np.zeros([self.n, self.m, self.b])
        for j in range(self.n):
            cri = self.impact_matrix.criterions[j]
            ascending = cri.ascending
            p_j, v_j = cri.p, cri.v
            for i_a in range(self.m):
                a = self.impact_matrix.impact_matrix[i_a, j]
                for i_b in range(self.b):
                    b = self.profile_matrix.data[j, i_b]
                    dj_ab[j, i_a, i_b] = discordance_index(a, b, p_j, v_j, ascending)
                    dj_ba[j, i_a, i_b] = discordance_index(b, a, p_j, v_j, ascending)
        return dj_ab, dj_ba

    def compute_pi(self, preference_type, preference_vector=None):
        if preference_vector is None:
            preference_vector = [0]

        preference_vector = np.array(preference_vector)

        cj_ab, cj_ba = self.compute_concordance_indexes()
        dj_ab, dj_ba = self.compute_discordance_index()

        if preference_vector is None:
            preference_vector = []

        try:
            h = monte_carlo_simulation(self.m, self.n, self.b, self.mc_it, self.optimistic, self.lambda_value,
                                       self.random, cj_ab, cj_ba, dj_ab, dj_ba, preference_type, preference_vector)
        except Exception as e:
            print(f"\033[91mException: {e}\033[00m")
            self.pi = None
            return
        self.pi = h / self.mc_it
