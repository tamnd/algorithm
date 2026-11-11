# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-hellman-knapsack-cryptosystem/. The authors are listed in prov/FC4WWX.jsonl.
"""A copy of the LLL basis reduction of https://algorithm.tamnd.com/lll-algorithm/.

The copy keeps this page self contained. The only changes are the removal of
the line markers of that page and of the swap counter in the public helper.
See the lll-algorithm page for the proof and the complexity.
"""

from fractions import Fraction
from math import floor
from typing import Sequence, Union

Number = Union[int, Fraction]
Basis = list[list[Number]]


def _dot(u: Sequence[Number], v: Sequence[Number]) -> Number:
    return sum((a * b for a, b in zip(u, v)), 0)


def _nearest(x: Fraction) -> int:
    """The integer nearest to x; a half is rounded up, so -1/2 <= x - result < 1/2."""
    return floor(x + Fraction(1, 2))


def lll_reduce(basis: Sequence[Sequence[Number]], delta: Number = Fraction(3, 4)) -> Basis:
    """LLL-reduce a lattice basis with exact rational arithmetic.

    Input: n >= 1 linearly independent rows of the same length m, with int or
    Fraction entries, and a rational delta with 1/4 < delta < 1. The rows of
    the result are a basis of the same lattice that is size-reduced and meets
    the Lovasz condition, so the first row is within a factor 2^((n-1)/2) of
    the shortest vector of the lattice.
    """
    delta = Fraction(delta)
    if not Fraction(1, 4) < delta < 1:
        raise ValueError("delta must satisfy 1/4 < delta < 1")
    b: Basis = [list(row) for row in basis]
    n = len(b)
    if n == 0:
        return []
    m = len(b[0])
    if m == 0 or any(len(row) != m for row in b):
        raise ValueError("rows must have the same positive length")

    mu = [[Fraction(0)] * n for _ in range(n)]
    big_b: list[Fraction] = []
    star: list[list[Fraction]] = []
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

    def reduce(k: int, j: int) -> None:
        """Subtract the nearest integer multiple of b_j from b_k (0-based)."""
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
