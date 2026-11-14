# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/propensity-score-matching/. The authors are listed in prov/SWSA9A.jsonl.

"""Pair matching on a one-dimensional score, such as the propensity score or its logit.

optimal_pair_match finds m disjoint treated-control pairs with the least total
absolute score distance, by sorting and a dynamic program over the two sorted
lists. greedy_match is the common nearest-available heuristic, and
nearest_with_replacement lets controls be reused. att_from_pairs turns pairs
into the matching estimate of the effect on the treated. With int or Fraction
scores every distance and cost is exact.
"""

import bisect
from collections.abc import Sequence


def optimal_pair_match(s: Sequence, c: Sequence) -> tuple:
    """Minimum total |s_i - c_j| over all matchings of every treated unit to a distinct control.

    s: m treated scores, c: n control scores, m <= n. Returns (cost, pairs), where
    pairs is a list of (treated index, control index) in the input numbering,
    sorted by treated index. Cost: Theta(m n + n log n) time and Theta(m n) space.
    """
    m, n = len(s), len(c)
    if m > n:
        raise ValueError("pair matching needs at least as many controls as treated units")
    ts = sorted(range(m), key=lambda i: (s[i], i))  # @line L1
    cs = sorted(range(n), key=lambda j: (c[j], j))
    inf = None  # None stands for infinity
    D = [[0] * (n + 1)] + [[inf] * (n + 1) for _ in range(m)]  # @line L2
    for i in range(1, m + 1):  # @line L3
        si = s[ts[i - 1]]
        row, prev = D[i], D[i - 1]
        for j in range(i, n + 1):  # @line L4
            take = prev[j - 1] + abs(si - c[cs[j - 1]])
            skip = row[j - 1]
            row[j] = take if skip is None or take < skip else skip  # @line L5
    pairs = []
    i, j = m, n
    while i > 0:  # @line L6
        if j > i and D[i][j - 1] is not None and D[i][j - 1] == D[i][j]:
            j -= 1
        else:
            pairs.append((ts[i - 1], cs[j - 1]))
            i, j = i - 1, j - 1
    pairs.sort()
    return D[m][n], pairs  # @line L7


def greedy_match(s: Sequence, c: Sequence, order: Sequence | None = None, caliper=None) -> list:
    """Nearest available control for each treated unit in turn, without replacement.

    order: the order in which treated units choose (default: decreasing score,
    ties by index). A treated unit whose nearest available control is farther
    than the caliper, or that finds no control left, stays unmatched. Ties in
    distance go to the lower control index. Cost: O(m n).
    """
    if order is None:
        order = sorted(range(len(s)), key=lambda i: (-s[i], i))
    free = set(range(len(c)))
    pairs = []
    for i in order:
        if not free:
            break
        j = min(free, key=lambda k: (abs(s[i] - c[k]), k))
        if caliper is not None and abs(s[i] - c[j]) > caliper:
            continue
        free.remove(j)
        pairs.append((i, j))
    pairs.sort()
    return pairs


def nearest_with_replacement(s: Sequence, c: Sequence) -> list:
    """For each treated unit, the index of the nearest control (controls may repeat).

    Ties go to the lower score, then to the lower index. Cost: O((m + n) log n).
    """
    if not c:
        raise ValueError("no controls")
    cs = sorted(range(len(c)), key=lambda j: (c[j], j))
    keys = [c[j] for j in cs]
    out = []
    for i, si in enumerate(s):
        k = bisect.bisect_left(keys, si)
        cand = [q for q in (k - 1, k) if 0 <= q < len(keys)]
        q = min(cand, key=lambda q: (abs(si - keys[q]), keys[q], cs[q]))
        out.append((i, cs[q]))
    return out


def att_from_pairs(y_treated: Sequence, y_control: Sequence, pairs: Sequence) -> object:
    """The matching estimate of the ATT: the mean over pairs of y_treated - y_control."""
    if not pairs:
        raise ValueError("no pairs")
    total = 0
    for i, j in pairs:
        total = total + (y_treated[i] - y_control[j])
    return total / len(pairs)


def total_distance(s: Sequence, c: Sequence, pairs: Sequence) -> object:
    """Sum of |s_i - c_j| over the pairs."""
    total = 0
    for i, j in pairs:
        total = total + abs(s[i] - c[j])
    return total
