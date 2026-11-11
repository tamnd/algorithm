# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-hellman-knapsack/. The authors are listed in prov/TC99QJ.jsonl.

"""A local copy of LLL basis reduction (https://algorithm.tamnd.com/lll-algorithm/).

The copy keeps this page self contained. It uses exact rational arithmetic,
which is slow but simple, and is meant for the small lattices of the tests.
See the lll-algorithm page for the proof and the complexity.
"""

from fractions import Fraction
from math import floor


def _dot(u, v):
    return sum((a * b for a, b in zip(u, v)), 0)


def _nearest(x: Fraction) -> int:
    """The integer nearest to x; a half is rounded up."""
    return floor(x + Fraction(1, 2))


def lll_reduce(basis, delta=Fraction(99, 100)):
    """LLL-reduce linearly independent integer rows; return the reduced rows.

    delta must satisfy 1/4 < delta < 1. The first row of the result is within
    a factor (4 / (4 delta - 1))^((n - 1) / 2) of the shortest nonzero vector.
    """
    delta = Fraction(delta)
    if not Fraction(1, 4) < delta < 1:
        raise ValueError("delta must satisfy 1/4 < delta < 1")
    b = [list(row) for row in basis]
    n = len(b)
    if n == 0:
        return []
    mu = [[Fraction(0)] * n for _ in range(n)]
    big_b, star = [], []
    for i in range(n):
        v = [Fraction(x) for x in b[i]]
        for j in range(i):
            mu[i][j] = Fraction(_dot(b[i], star[j])) / big_b[j]
            v = [x - mu[i][j] * y for x, y in zip(v, star[j])]
        norm = _dot(v, v)
        if norm == 0:
            raise ValueError("the rows are linearly dependent")
        star.append(v)
        big_b.append(norm)

    def reduce(k, j):
        q = _nearest(mu[k][j])
        if q != 0:
            b[k] = [x - q * y for x, y in zip(b[k], b[j])]
            for i in range(j):
                mu[k][i] -= q * mu[j][i]
            mu[k][j] -= q

    k = 1
    while k < n:
        reduce(k, k - 1)
        if delta * big_b[k - 1] > big_b[k] + mu[k][k - 1] ** 2 * big_b[k - 1]:
            u = mu[k][k - 1]
            new_prev = big_b[k] + u * u * big_b[k - 1]
            mu[k][k - 1] = u * big_b[k - 1] / new_prev
            big_b[k] = big_b[k - 1] * big_b[k] / new_prev
            big_b[k - 1] = new_prev
            b[k - 1], b[k] = b[k], b[k - 1]
            for j in range(k - 1):
                mu[k - 1][j], mu[k][j] = mu[k][j], mu[k - 1][j]
            for i in range(k + 1, n):
                t = mu[i][k]
                mu[i][k] = mu[i][k - 1] - u * t
                mu[i][k - 1] = t + mu[k][k - 1] * mu[i][k]
            k = max(1, k - 1)
        else:
            for j in range(k - 2, -1, -1):
                reduce(k, j)
            k += 1
    return b
