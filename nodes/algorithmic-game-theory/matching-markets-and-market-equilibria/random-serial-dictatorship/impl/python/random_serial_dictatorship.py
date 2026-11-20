# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-serial-dictatorship/. The authors are listed in prov/K05SWB.jsonl.

import random
from fractions import Fraction
from itertools import permutations
from typing import Optional, Sequence


def _check(prefs: Sequence[Sequence[int]], m: Optional[int]) -> int:
    if m is None:
        m = 1 + max((o for lst in prefs for o in lst), default=-1)
    for lst in prefs:
        if len(set(lst)) != len(lst) or any(not 0 <= o < m for o in lst):
            raise ValueError("a preference list repeats an object or is out of range")
    return m


def _dictatorship(prefs: Sequence[Sequence[int]], order: Sequence[int], m: int) -> list[int]:
    """One run of serial dictatorship in the given order (lines L2 to L8)."""
    taken = [False] * m  # @line L2
    match = [-1] * len(prefs)  # @line L3
    for k in range(len(order)):  # @line L4
        i = order[k]  # @line L5
        for o in prefs[i]:  # @line L6
            if not taken[o]:  # @line L7
                match[i] = o
                taken[o] = True
                break
    return match  # @line L8


def random_serial_dictatorship(
    prefs: Sequence[Sequence[int]], rng: random.Random, m: Optional[int] = None
) -> list[int]:
    """Random serial dictatorship: serial dictatorship in a uniformly random order.

    prefs[i] lists the objects acceptable to agent i, best first; the objects are
    0, ..., m - 1. rng is the source of randomness (random.Random with a fixed seed in the
    tests). Returns the object of each agent, or -1 for no object.
    O(m + n^2) time and O(n + m) space, plus n - 1 random draws for the order.
    """
    m = _check(prefs, m)
    order = list(range(len(prefs)))
    for k in range(len(order) - 1, 0, -1):  # @line L1
        j = rng.randint(0, k)  # Fisher-Yates: order is uniform over all n! orders
        order[k], order[j] = order[j], order[k]
    return _dictatorship(prefs, order, m)


def rsd_lottery(prefs: Sequence[Sequence[int]], m: Optional[int] = None) -> dict:
    """The exact lottery of random serial dictatorship over matchings.

    Returns a dict from each matching (a tuple of objects, -1 for none) to its
    probability as a Fraction. It runs serial dictatorship on all n! orders, so it is for
    small n only: O(n! (m + n^2)) time.
    """
    m = _check(prefs, m)
    n = len(prefs)
    count: dict = {}
    total = 0
    for order in permutations(range(n)):
        mu = tuple(_dictatorship(prefs, order, m))
        count[mu] = count.get(mu, 0) + 1
        total += 1
    return {mu: Fraction(c, total) for mu, c in count.items()}


def rsd_probabilities(prefs: Sequence[Sequence[int]], m: Optional[int] = None) -> list[list[Fraction]]:
    """The exact random assignment of random serial dictatorship.

    Returns the n by m matrix P with P[i][o] the probability that agent i gets object o,
    as Fractions. Row i sums to 1 minus the probability that i gets nothing.
    O(n! (m + n^2) + n m) time; small n only.
    """
    m = _check(prefs, m)
    P = [[Fraction(0)] * m for _ in prefs]
    for mu, p in rsd_lottery(prefs, m).items():
        for i, o in enumerate(mu):
            if o >= 0:
                P[i][o] += p
    return P
