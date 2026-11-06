# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/babai-nearest-plane/. The authors are listed in prov/70W13Q.jsonl.

from fractions import Fraction
from math import floor
from typing import Sequence, Union

Number = Union[int, Fraction]


def _dot(u: Sequence[Fraction], v: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def _gram_schmidt(b: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[Fraction]]:
    """Exact Gram-Schmidt rows b_i* and their squared norms; ValueError if a norm is 0."""
    stars: list[list[Fraction]] = []
    norms: list[Fraction] = []
    for row in b:
        w = row[:]
        for s, ns in zip(stars, norms):
            mu = _dot(row, s) / ns
            w = [a - mu * c for a, c in zip(w, s)]
        nw = _dot(w, w)
        if nw == 0:
            raise ValueError("the basis vectors are linearly dependent")
        stars.append(w)
        norms.append(nw)
    return stars, norms


def babai_nearest_plane(basis: Sequence[Sequence[Number]], target: Sequence[Number]) -> tuple[list[int], list[Fraction]]:
    """Babai's nearest plane method for the closest vector problem.

    Input: n >= 1 linearly independent rows b_1..b_n of length m (int or Fraction
    entries, exact arithmetic) and a target t of length m. Output: (x, v) with x an
    integer vector and v = x_1 b_1 + ... + x_n b_n. For i = n down to 1 the
    coefficient x_i is the nearest integer (halves rounded up) to <w, b_i*> / ||b_i*||^2,
    where w = t - x_{i+1} b_{i+1} - ... - x_n b_n.
    Guarantees: t - v = o + sum c_i b_i* with o orthogonal to the span and
    -1/2 <= c_i < 1/2; v is a closest vector whenever dist(t, L) < min ||b_i*|| / 2.
    Cost: O(n^2 m) arithmetic operations for Gram-Schmidt, then O(n m) for the loop.
    Raises ValueError for dependent rows or mismatched lengths.
    """
    b = [[Fraction(c) for c in row] for row in basis]
    t = [Fraction(c) for c in target]
    n = len(b)
    if n == 0 or any(len(row) != len(t) for row in b):
        raise ValueError("need at least one basis row, all of the target's length")
    stars, norms = _gram_schmidt(b)  # @line L1
    w = t[:]  # @line L2
    x = [0] * n
    for i in range(n - 1, -1, -1):  # @line L3
        x[i] = floor(_dot(w, stars[i]) / norms[i] + Fraction(1, 2))  # @line L4
        w = [a - x[i] * c for a, c in zip(w, b[i])]  # @line L5
    return x, [a - c for a, c in zip(t, w)]  # @line L6
