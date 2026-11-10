# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prophet-inequality/. The authors are listed in prov/WRNK0C.jsonl.

"""Exact values of stopping rules for independent discrete random variables.

A distribution is a list of (value, probability) pairs with Fraction entries,
values at least 0 and probabilities that add up to 1. The variables X_1, ...,
X_n are independent and are seen in the order of the list. All results are
exact fractions.
"""

from fractions import Fraction

Dist = list[tuple[Fraction, Fraction]]


def check(dists: list[Dist]) -> None:
    for d in dists:
        if sum((p for _, p in d), Fraction(0)) != 1 or any(p < 0 or x < 0 for x, p in d):
            raise ValueError("each distribution needs values >= 0 and probabilities that add up to 1")


def expected_max(dists: list[Dist]) -> Fraction:
    """E[max_i X_i], the expected value that a prophet who sees all values gets.

    Uses Pr[max <= v] = prod_i Pr[X_i <= v] at each support point v.
    Cost: O(m * n) for m support points in total.
    """
    check(dists)
    support = sorted({x for d in dists for x, _ in d})
    total, below = Fraction(0), Fraction(0)
    for v in support:
        at_most = Fraction(1)
        for d in dists:
            at_most *= sum((p for x, p in d if x <= v), Fraction(0))
        total += v * (at_most - below)
        below = at_most
    return total


def stop_probability(dists: list[Dist], tau: Fraction) -> Fraction:
    """Pr[some X_i >= tau], the probability that the threshold rule stops."""
    check(dists)
    none = Fraction(1)
    for d in dists:
        none *= sum((p for x, p in d if x < tau), Fraction(0))
    return 1 - none


def threshold_value(dists: list[Dist], tau: Fraction) -> Fraction:
    """Expected gain of the rule that stops at the first X_i >= tau (0 if none).

    Cost: O(m) for m support points in total.
    """
    check(dists)
    alive, total = Fraction(1), Fraction(0)
    for d in dists:
        total += alive * sum((x * p for x, p in d if x >= tau), Fraction(0))
        alive *= sum((p for x, p in d if x < tau), Fraction(0))
    return total


def optimal_value(dists: list[Dist]) -> Fraction:
    """Largest expected gain of any online stopping rule, by backward induction.

    With v the value of going on, the rule stops at X_i = x if x >= v, so the
    value before X_i is E[max(X_i, v)]. Cost: O(m).
    """
    check(dists)
    v = Fraction(0)
    for d in reversed(dists):
        v = sum((p * max(x, v) for x, p in d), Fraction(0))
    return v


def half_mean_threshold(dists: list[Dist]) -> Fraction:
    """The threshold E[max]/2 of Kleinberg and Weinberg."""
    return expected_max(dists) / 2


def guarantee(dists: list[Dist], tau: Fraction) -> Fraction:
    """The lower bound p*tau + (1 - p)*(E[max] - tau) of the proof, p = Pr[stop]."""
    p = stop_probability(dists, tau)
    return p * tau + (1 - p) * (expected_max(dists) - tau)
