# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deep-lll/. The authors are listed in prov/NEWYCT.jsonl.

from fractions import Fraction
from math import floor
from typing import Sequence, Union

Number = Union[int, Fraction]


def _dot(u: Sequence[Fraction], v: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def _gso(b: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[list[Fraction]], list[Fraction]]:
    """Gram-Schmidt rows b_i*, coefficients mu[i][j] (j < i) and squared norms N_i."""
    n = len(b)
    stars: list[list[Fraction]] = []
    norms: list[Fraction] = []
    mu = [[Fraction(0)] * n for _ in range(n)]
    for i, row in enumerate(b):
        w = row[:]
        for j in range(i):
            mu[i][j] = _dot(row, stars[j]) / norms[j]
            w = [a - mu[i][j] * c for a, c in zip(w, stars[j])]
        nw = _dot(w, w)
        if nw == 0:
            raise ValueError("the basis vectors are linearly dependent")
        stars.append(w)
        norms.append(nw)
    return stars, mu, norms


def deep_lll(basis: Sequence[Sequence[Number]], delta: Number = Fraction(3, 4)) -> list[list[Fraction]]:
    """Schnorr-Euchner LLL with deep insertions, in exact rational arithmetic.

    Input: n >= 1 linearly independent rows of length m (int or Fraction) and a
    parameter 1/4 < delta <= 1. Output: a basis of the same lattice that is size
    reduced (|mu_kj| <= 1/2) and deep-reduced: for all i < k,
    ||pi_i(b_k)||^2 = sum_{j=i..k} mu_kj^2 N_j >= delta N_i, where N_j = ||b_j*||^2.
    Each pass of the main loop costs O(n^2 m) arithmetic operations (Gram-Schmidt is
    recomputed); the number of passes is finite but has no known polynomial bound.
    Raises ValueError for dependent rows, bad lengths or delta outside (1/4, 1].
    """
    d = Fraction(delta)
    if not Fraction(1, 4) < d <= 1:
        raise ValueError("delta must satisfy 1/4 < delta <= 1")
    b = [[Fraction(c) for c in row] for row in basis]
    n = len(b)
    if n == 0 or any(len(row) != len(b[0]) for row in b):
        raise ValueError("need at least one basis row, all of the same length")
    _gso(b)  # raises on dependent input
    k = 1  # @line L1
    while k < n:  # @line L2
        _, mu, norms = _gso(b[: k + 1])
        for j in range(k - 1, -1, -1):  # @line L3
            q = floor(mu[k][j] + Fraction(1, 2))
            if q:
                b[k] = [a - q * c for a, c in zip(b[k], b[j])]
                for l in range(j):
                    mu[k][l] -= q * mu[j][l]
                mu[k][j] -= q
        c = _dot(b[k], b[k])  # @line L4
        i = 0
        inserted = False
        while i < k:  # @line L5
            if c < d * norms[i]:  # @line L6
                b.insert(i, b.pop(k))
                k = max(i, 1)
                inserted = True
                break
            c -= mu[k][i] ** 2 * norms[i]  # @line L7
            i += 1
        if not inserted:
            k += 1  # @line L8
    return b  # @line L9
