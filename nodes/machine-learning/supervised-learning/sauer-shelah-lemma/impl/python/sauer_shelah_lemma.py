# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sauer-shelah-lemma/. The authors are listed in prov/15YWCY.jsonl.

"""The Sauer-Shelah bound and the exact counts it bounds, for finite classes.

A finite class over the domain {0, ..., N-1} is a collection of tuples of labels 0 or 1.
"""

from itertools import combinations
from math import comb, e


def sauer_bound(n, d):
    """sum_{i=0}^{d} C(n, i): the Sauer-Shelah bound on the growth function."""
    return sum(comb(n, i) for i in range(d + 1))


def exp_bound(n, d):
    """(e n / d)^d, the closed form upper bound for n >= d >= 1."""
    return (e * n / d) ** d


def restriction(H, C):
    """H_C: the set of distinct labelings that the class gives to the points C."""
    return {tuple(h[c] for c in C) for h in H}


def shattered_subsets(H, C):
    """All subsets B of C (as tuples) that H shatters. The empty set is always one."""
    out = []
    for k in range(len(C) + 1):
        for B in combinations(C, k):
            if len(restriction(H, B)) == 2 ** k:
                out.append(B)
    return out


def vc_dimension(H, domain):
    """The largest size of a subset of the domain that H shatters (H not empty)."""
    return max(len(B) for B in shattered_subsets(H, domain))


def growth(H, domain, n):
    """tau_H(n): the largest number of labelings of n points of the domain."""
    return max(len(restriction(H, C)) for C in combinations(domain, n))


def at_most_d_ones(N, d):
    """The class of all labelings of N points with at most d ones. Its VC dimension
    is d, and on its domain it meets the Sauer-Shelah bound with equality."""
    out = []
    for k in range(d + 1):
        for S in combinations(range(N), k):
            out.append(tuple(1 if i in S else 0 for i in range(N)))
    return out


def intervals_on_line(N):
    """The labelings of N points on a line by intervals: the empty one and all runs."""
    out = [tuple([0] * N)]
    for a in range(N):
        for b in range(a, N):
            out.append(tuple(1 if a <= i <= b else 0 for i in range(N)))
    return out
