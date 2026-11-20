# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-coherence/. The authors are listed in prov/1VF7YK.jsonl.
"""Mutual coherence of a matrix, the Welch bound, and brute force checks of the bounds it gives.

A matrix is a list of m rows of length n, with real or complex entries. Its
columns are the atoms. The mutual coherence is the largest absolute inner
product of two distinct normalized columns.
"""

import math
from itertools import combinations

from imgla import sym_eig


def columns(a):
    return [[row[j] for row in a] for j in range(len(a[0]))]


def coherence(a):
    """Return (mu, i, j): the mutual coherence and a pair of columns that attains it."""
    cols = []
    for c in columns(a):  # @line L1
        nrm = math.sqrt(sum(abs(v) ** 2 for v in c))
        if nrm == 0.0:
            raise ValueError("zero column")
        cols.append([v / nrm for v in c])
    mu, best = 0.0, (0, 1)  # @line L2
    n = len(cols)
    for i in range(n - 1):  # @line L3
        for j in range(i + 1, n):  # @line L4
            g = abs(sum(p.conjugate() * q for p, q in zip(cols[i], cols[j])))
            if g > mu:  # @line L5
                mu, best = g, (i, j)
    return mu, best[0], best[1]  # @line L6


def welch_bound(m, n):
    """The lower bound sqrt((n - m) / (m (n - 1))) on the coherence of n unit vectors in m dimensions."""
    if n <= m:
        return 0.0
    return math.sqrt((n - m) / (m * (n - 1)))


def max_sparsity_for_uniqueness(mu):
    """The largest integer s with s < (1 + 1/mu) / 2."""
    bound = (1.0 + 1.0 / mu) / 2.0
    s = math.ceil(bound) - 1
    return max(s, 0)


def _gram(cols, idx):
    return [[sum(p * q for p, q in zip(cols[i], cols[j])) for j in idx] for i in idx]


def spark(a, tol=1e-10):
    """The least number of linearly dependent columns (real matrices), by brute force.

    Returns n + 1 if all n columns are independent.
    """
    cols = columns(a)
    n = len(cols)
    for k in range(1, n + 1):
        for idx in combinations(range(n), k):
            w, _ = sym_eig(_gram(cols, idx))
            if w[0] <= tol * max(1.0, w[-1]):
                return k
    return n + 1


def restricted_isometry_constant(a, s):
    """delta_s of a real matrix whose columns have norm 1, by enumerating all supports of size s."""
    cols = columns(a)
    delta = 0.0
    for idx in combinations(range(len(cols)), s):
        w, _ = sym_eig(_gram(cols, idx))
        delta = max(delta, 1.0 - w[0], w[-1] - 1.0)
    return delta
