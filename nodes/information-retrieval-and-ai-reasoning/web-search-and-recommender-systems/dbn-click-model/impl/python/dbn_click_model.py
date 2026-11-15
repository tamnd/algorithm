# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dbn-click-model/. The authors are listed in prov/H0ZAVM.jsonl.
"""The dynamic Bayesian network click model (Chapelle and Zhang, 2009).

The user examines the first result. At an examined result d the user
clicks with probability a[d]. After a click the user is satisfied with
probability s[d] and then stops. A user who did not click, or clicked and
was not satisfied, examines the next result with probability gamma and
otherwise stops.

click_probability computes P(click vector) with a forward pass over two
numbers: the probability of the clicks so far together with "the current
rank is examined", and together with "the user has stopped".
"""


def click_probability(ranking, clicks, a, s, gamma):
    """P(C_1..C_n = clicks) for the ranking under the DBN model."""
    if len(ranking) != len(clicks):
        raise ValueError("one click value per rank")
    examined, stopped = 1.0, 0.0
    for d, c in zip(ranking, clicks):
        if c:
            # Only an examined user clicks; afterwards the user goes on if
            # not satisfied and persevering, and stops otherwise.
            stay = examined * a[d] * (1.0 - s[d]) * gamma
            stopped = examined * a[d] * (s[d] + (1.0 - s[d]) * (1.0 - gamma))
            examined = stay
        else:
            # A skip by an examined user, or any rank after stopping.
            skip = examined * (1.0 - a[d])
            examined, stopped = skip * gamma, stopped + skip * (1.0 - gamma)
    return examined + stopped


def simulate(ranking, a, s, gamma, rng):
    """Draw one session; return its click vector as a tuple of 0/1."""
    clicks = [0] * len(ranking)
    for i, d in enumerate(ranking):
        if rng.random() < a[d]:
            clicks[i] = 1
            if rng.random() < s[d]:
                break
        if rng.random() >= gamma:
            break
    return tuple(clicks)


def click_rates(ranking, a, s, gamma):
    """P(C_i = 1) for each rank i."""
    rates = []
    examined = 1.0
    for d in ranking:
        rates.append(examined * a[d])
        examined *= (a[d] * (1.0 - s[d]) + (1.0 - a[d])) * gamma
    return rates
