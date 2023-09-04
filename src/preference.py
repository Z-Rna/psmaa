import numpy as np
from numba import njit
from .sample import sample_weights


@njit
def no_preference(n: int, _, rand_gen=np.random.default_rng(666)):
    w = sample_weights(n, rand_gen)
    return np.array(w)


@njit
def ordinal_preference(n: int, preference_vector, rand_gen=np.random.default_rng(666)):
    if n != len(preference_vector):
        raise Exception(f"The length od preference_vector is not the same as n, {len(preference_vector)}!={n}")

    preference_vector = [p - 1 for p in preference_vector]
    mapped_ranks = sample_weights(n, rand_gen)
    mapped_ranks = np.sort(mapped_ranks)[::-1]

    preference_vector = np.array(preference_vector)
    mapped_ranks = np.array(mapped_ranks)

    return mapped_ranks[preference_vector]


@njit
def cardinal_preference(n: int, preference_vector, rand_gen=np.random.default_rng(666)):
    if n != len(preference_vector):
        raise Exception(f"The length od preference_vector is not the same as n, {len(preference_vector)}!={n}")

    max_it = 100000
    interval_count = 0
    lower_bounds_sum = .0
    for pref in preference_vector:
        if len(pref) == 2:
            if pref[0] != pref[1]:
                interval_count += 1
            if pref[0] > pref[1]:
                raise Exception(
                    f"A one of the intervals have the first bound greater than the second one:[{pref[0]},{pref[1]}]")
        lower_bounds_sum += pref[0]

    if lower_bounds_sum > 1.0: raise Exception("Sum of bounds have to be under 1.0")

    for i in range(max_it):
        current_interval = 0
        over_upper_bound = False
        ranks = np.zeros(n)
        if interval_count:
            sampled = sample_weights(interval_count, rand_gen, 1. - lower_bounds_sum)
        for j, pref in enumerate(preference_vector):
            if len(pref) == 1:
                ranks[j] = pref[0]
            else:
                if pref[0] == pref[1]:
                    ranks[j] = pref[0]
                else:
                    ranks[j] = pref[0] + sampled[current_interval]
                    if ranks[j] > pref[1]:
                        over_upper_bound = True
                        break
                    current_interval += 1
        if not over_upper_bound and np.sum(ranks) == 1:
            return ranks
    raise Exception("No value of weights to return")
