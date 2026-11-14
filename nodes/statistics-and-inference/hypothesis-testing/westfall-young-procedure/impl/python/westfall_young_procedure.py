# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/westfall-young-procedure/. The authors are listed in prov/3E4H4P.jsonl.
"""The Westfall-Young step-down maxT procedure, with exact permutation enumeration.

Input: the observed statistics t_1, ..., t_m (large values are evidence against
H_j) and the statistics recomputed on every element of a permutation group G,
one row per element, the identity included. The adjusted p-value of the
hypothesis of rank k (by decreasing t) is the running maximum over j <= k of
  #{g : max over ranks >= j of T(g) >= t_(j)} / |G|.
Rejecting the hypotheses with adjusted p-value <= alpha controls the FWER
strongly when the joint law of the true-null statistics is invariant under G.

two_sample_statistics computes |n_2 S_1 - n_1 S_2| for each variable, an integer
multiple of the absolute difference of the group means, for every split of n
integer observations into groups of sizes n_1 and n_2.
"""

import itertools
from collections.abc import Sequence
from fractions import Fraction


def max_t_adjusted(t_obs: Sequence, t_perm: Sequence[Sequence]) -> list[Fraction]:
    """Step-down maxT adjusted p-values; t_perm has one row per group element, identity included."""
    m, b = len(t_obs), len(t_perm)
    if m == 0:
        return []
    if b == 0 or any(len(row) != m for row in t_perm):
        raise ValueError("t_perm needs at least one row of length m")
    order = sorted(range(m), key=lambda j: -t_obs[j])  # @line L1
    count = [0] * m
    for row in t_perm:  # @line L2
        u = None
        for k in range(m - 1, -1, -1):  # @line L3
            v = row[order[k]]
            u = v if u is None or v > u else u  # @line L4
            if u >= t_obs[order[k]]:  # @line L5
                count[k] += 1
    adjusted = [Fraction(0)] * m
    running = Fraction(0)
    for k in range(m):  # @line L6
        running = max(running, Fraction(count[k], b))  # @line L7
        adjusted[order[k]] = running
    return adjusted  # @line L8


def single_step_max_t(t_obs: Sequence, t_perm: Sequence[Sequence]) -> list[Fraction]:
    """Single-step maxT: #{g : max_j T_j(g) >= t_i} / |G| for each i."""
    b = len(t_perm)
    maxima = [max(row) for row in t_perm]
    return [Fraction(sum(1 for v in maxima if v >= t), b) for t in t_obs]


def splits(n: int, n1: int):
    """All subsets of size n1 of range(n): the orbit of the permutation group acting on the group labels."""
    return itertools.combinations(range(n), n1)


def two_sample_statistics(data: Sequence[Sequence[int]], group1: Sequence[int]) -> list[int]:
    """|n_2 S_1 - n_1 S_2| for each column of data (rows are units), with group 1 the given row indices."""
    n, n1 = len(data), len(group1)
    n2 = n - n1
    in1 = set(group1)
    m = len(data[0])
    out = []
    for j in range(m):
        s1 = sum(data[i][j] for i in in1)
        s2 = sum(data[i][j] for i in range(n)) - s1
        out.append(abs(n2 * s1 - n1 * s2))
    return out


def westfall_young_two_sample(data: Sequence[Sequence[int]], n1: int, alpha=Fraction(1, 20)):
    """Rows 0..n1-1 are group 1. Return (reject, adjusted) by full enumeration of the splits."""
    n = len(data)
    t_obs = two_sample_statistics(data, range(n1))
    t_perm = [two_sample_statistics(data, s) for s in splits(n, n1)]
    adjusted = max_t_adjusted(t_obs, t_perm)
    return [a <= alpha for a in adjusted], adjusted
