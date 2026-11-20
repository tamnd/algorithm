# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dorfler-marking/. The authors are listed in prov/G0MEX4.jsonl.

"""Dorfler (bulk) marking with a marked set of minimal size.

Input: a list eta2 of squared error indicators eta_K^2 >= 0, one per
element, and a parameter theta in (0, 1]. Output: a list M of element
numbers with sum(eta2[K] for K in M) >= theta * sum(eta2) and with the
smallest possible size. The functions work on float or Fraction data; with
Fraction the comparisons are exact.

dorfler_sort sorts and takes the largest indicators: O(M log M) for M
elements. dorfler_select finds the same size by partitions around random
pivots, as in quickselect: O(M) expected time (real-RAM).
"""

import random


def dorfler_sort(eta2, theta):
    """Return a minimal bulk set by sorting the indicators in decreasing order."""
    goal = theta * sum(eta2)  # @line L1
    order = sorted(range(len(eta2)), key=lambda t: -eta2[t])  # @line L2
    marked, acc = [], 0  # @line L3
    for t in order:  # @line L4
        if acc >= goal and marked:
            break
        marked.append(t)  # @line L5
        acc += eta2[t]
    return marked  # @line L6


def dorfler_select(eta2, theta, rng=None):
    """Return a minimal bulk set by partitions around random pivots (expected linear time)."""
    rng = rng or random.Random(0)
    goal = theta * sum(eta2)  # @line L7
    marked = []
    cand = list(range(len(eta2)))  # @line L8
    while cand:  # @line L9
        p = eta2[cand[rng.randrange(len(cand))]]  # @line L10
        high = [t for t in cand if eta2[t] > p]  # @line L11
        equal = [t for t in cand if eta2[t] == p]
        low = [t for t in cand if eta2[t] < p]
        sh = sum(eta2[t] for t in high)  # @line L12
        if high and sh >= goal:  # @line L13
            cand = high  # the answer ends inside high
            continue
        se = sum(eta2[t] for t in equal)
        if sh + se >= goal:  # @line L14
            marked.extend(high)
            acc = sh
            for t in equal:
                if acc >= goal and marked:
                    break
                marked.append(t)
                acc += eta2[t]
            return marked
        marked.extend(high + equal)  # @line L15
        goal -= sh + se
        cand = low
    return marked  # @line L16
