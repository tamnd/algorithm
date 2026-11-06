# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lagrange-gauss-reduction/. The authors are listed in prov/TQ44SE.jsonl.

from fractions import Fraction
from math import floor
from typing import Sequence, Union

Number = Union[int, Fraction]
Vector = list[Number]


def _dot(u: Sequence[Number], v: Sequence[Number]) -> Number:
    return sum((a * b for a, b in zip(u, v)), 0)


def _nearest(x: Fraction) -> int:
    """The integer nearest to x; a half is rounded up, so -1/2 <= x - result < 1/2."""
    return floor(x + Fraction(1, 2))


def lagrange_gauss_reduce(b1: Sequence[Number], b2: Sequence[Number]) -> tuple[Vector, Vector]:
    """Reduce a basis of a lattice of rank 2.

    Input: two linearly independent vectors of the same length m >= 1 with int or
    Fraction entries (exact arithmetic). Output: (b1, b2), a basis of the same
    lattice with ||b1|| <= ||b2|| and |<b1, b2>| <= ||b1||^2 / 2. Then ||b1|| is
    the first minimum and ||b2|| the second minimum of the lattice.
    Cost: O(1 + log(||b1|| / lambda_1)) loop iterations of O(m) arithmetic
    operations each, where b1 is the shorter input vector.
    Raises ValueError if the vectors are dependent or of different lengths.
    """
    u, v = list(b1), list(b2)
    if len(u) != len(v) or not u:
        raise ValueError("the two vectors must have the same positive length")
    if _dot(u, u) * _dot(v, v) - _dot(u, v) ** 2 == 0:
        raise ValueError("the vectors are linearly dependent")
    if _dot(u, u) > _dot(v, v):  # @line L1
        u, v = v, u
    while True:  # @line L2
        q = _nearest(Fraction(_dot(u, v)) / _dot(u, u))  # @line L3
        v = [y - q * x for x, y in zip(u, v)]  # @line L4
        if _dot(v, v) >= _dot(u, u):  # @line L5
            return u, v
        u, v = v, u  # @line L6
