import numpy as np


def no_preference(n: int, preference_vector=[]):
    from .sample import sample_weights
    return sample_weights(n)

def ordinal_preference(n: int, preference_vector):
    from .sample import sample_weights
    mapped_ranks = np.array(sample_weights(n))
    mapped_ranks = np.sort(mapped_ranks)[::-1]
    return mapped_ranks[preference_vector]

def cardinal_preference(n: int, preference_vector):
    from .sample import sample_weights
    max_it = 100000
    interval_count = 0
    lower_bounds_sum = .0
    for pref in preference_vector:
        if len(pref) == 2:
            interval_count += 1
        lower_bounds_sum += pref[0]

    if lower_bounds_sum > 1.0: raise Exception("Sum of bound have to be under 1.0")

    for i in range(max_it):
        current_interval = 0
        over_upper_bound = False
        ranks = np.zeros(n)
        if interval_count:
            sampled = sample_weights(interval_count, 1.-lower_bounds_sum)
        for j, pref in enumerate(preference_vector):
            if len(pref) == 1:
                ranks[j] = pref[0]
            else:
                ranks[j] = pref[0] + sampled[current_interval]
                if ranks[j] > pref[1]:
                    over_upper_bound = True
                    break
                current_interval += 1
        if not over_upper_bound and np.sum(ranks) == 1:
            return ranks
    raise ValueError("No value to return")