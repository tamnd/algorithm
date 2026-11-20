# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lipton-markakis-mehta-algorithm/. The authors are listed in prov/JTYPN5.jsonl.
"""The Lipton-Markakis-Mehta search over k-uniform strategies, in exact rational arithmetic.

The row player gets A[i][j] and the column player gets B[i][j]; both maximize. A strategy is
k-uniform if it is the uniform distribution on a multiset of k pure strategies, so every
probability is a multiple of 1/k. If the payoffs are in [0, 1] and k > 2 ln(2(m + n)) / eps^2,
some pair of k-uniform strategies is an eps-Nash equilibrium, so the search succeeds.
"""

import math
from fractions import Fraction
from itertools import combinations_with_replacement


def sample_size(m, n, eps):
    """Return the least integer k with k > 2 ln(2(m + n)) / eps^2."""
    eps = Fraction(eps)
    bound = 2 * math.log(2 * (m + n)) / float(eps * eps)
    k = max(1, math.floor(bound))
    while k <= bound:
        k += 1
    return k


def _mix(multiset, size, k):
    p = [Fraction(0)] * size
    for a in multiset:
        p[a] += Fraction(1, k)
    return p


def k_uniform_pairs(A, B, k):
    """Yield (x, y, row gain, column gain) for every pair of k-uniform strategies.

    The work for one pair is O(k), after O(k (m + n)) work for each multiset.
    """
    A = [[Fraction(v) for v in row] for row in A]
    B = [[Fraction(v) for v in row] for row in B]
    m, n = len(A), len(A[0])
    cols = []
    for C in combinations_with_replacement(range(n), k):
        kAy = [sum(A[r][c] for c in C) for r in range(m)]  # k times A y
        cols.append((C, kAy, max(kAy)))
    for R in combinations_with_replacement(range(m), k):
        kxB = [sum(B[r][c] for r in R) for c in range(n)]  # k times x^T B
        best_c = max(kxB)
        x = None
        for C, kAy, best_r in cols:
            row_gain = Fraction(best_r - sum(kAy[r] for r in R) / k, k)
            col_gain = Fraction(best_c - sum(kxB[c] for c in C) / k, k)
            if x is None:
                x = _mix(R, m, k)
            yield x, _mix(C, n, k), row_gain, col_gain


def lmm(A, B, eps, k=None):
    """Return the first pair of k-uniform strategies that is an eps-Nash equilibrium, or None."""
    eps = Fraction(eps)
    m, n = len(A), len(A[0])
    if k is None:
        k = sample_size(m, n, eps)  # @line L1
    A = [[Fraction(v) for v in row] for row in A]
    B = [[Fraction(v) for v in row] for row in B]
    cols = []
    for C in combinations_with_replacement(range(n), k):
        kAy = [sum(A[r][c] for c in C) for r in range(m)]
        cols.append((C, kAy, max(kAy)))
    for R in combinations_with_replacement(range(m), k):  # @line L2
        kxB = [sum(B[r][c] for r in R) for c in range(n)]  # @line L3
        best_c = max(kxB)
        for C, kAy, best_r in cols:  # @line L4
            # y is uniform on C. kAy and best_r were computed once for each C.
            kkAxy = sum(kAy[r] for r in R)  # @line L5
            kkBxy = sum(kxB[c] for c in C)  # k^2 times x^T B y, and kkAxy is k^2 times x^T A y
            if best_r * k - kkAxy <= eps * k * k and best_c * k - kkBxy <= eps * k * k:  # @line L6
                return _mix(R, m, k), _mix(C, n, k)  # @line L7
    return None


def best_k_uniform(A, B, k):
    """Return (gain, x, y) for a pair of k-uniform strategies with the least largest gain."""
    best = None
    for x, y, gr, gc in k_uniform_pairs(A, B, k):
        g = max(gr, gc)
        if best is None or g < best[0]:
            best = (g, x, y)
    return best
