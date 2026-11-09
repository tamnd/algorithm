# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/freivalds-algorithm/. The authors are listed in prov/Z43DEG.jsonl.

"""Freivalds' algorithm: check A B = C with random vectors.

Matrices are lists of rows of integers. If `modulus` is given, all arithmetic
is done modulo it; otherwise it is exact integer arithmetic. The answer
False ("not equal") is always correct. The answer True ("equal") is wrong
with probability at most 2^-k for vectors in {0, 1}^n.
"""

import itertools
import random
from fractions import Fraction
from typing import Sequence

Matrix = Sequence[Sequence[int]]


def mat_vec(m: Matrix, v: Sequence[int], modulus: int | None = None) -> list[int]:
    """The product m v, in O(rows * cols) operations."""
    out = []
    for row in m:
        s = sum(x * y for x, y in zip(row, v))
        out.append(s % modulus if modulus else s)
    return out


def detects(a: Matrix, b: Matrix, c: Matrix, r: Sequence[int], modulus: int | None = None) -> bool:
    """True if the vector r shows that A B != C, that is A (B r) != C r."""
    x = mat_vec(b, r, modulus)  # @line L3
    y = mat_vec(a, x, modulus)  # @line L4
    z = mat_vec(c, r, modulus)  # @line L5
    return y != z  # @line L6


def freivalds(
    a: Matrix,
    b: Matrix,
    c: Matrix,
    k: int,
    rng: random.Random,
    values: Sequence[int] = (0, 1),
    modulus: int | None = None,
) -> bool:
    """Return False if A B != C is proved; True ("probably equal") after k rounds.

    A is n x m, B is m x p and C is n x p. Each round draws r uniformly from
    values^p, so the default draws a uniform vector of p bits.
    """
    p = len(c[0]) if c else 0
    for _ in range(k):  # @line L1
        r = [values[rng.randrange(len(values))] for _ in range(p)]  # @line L2
        if detects(a, b, c, r, modulus):  # lines L3 to L6
            return False  # @line L6
    return True  # @line L7


def mat_mul(a: Matrix, b: Matrix, modulus: int | None = None) -> list[list[int]]:
    """The naive product, used only by the tests."""
    cols = list(zip(*b))
    out = []
    for row in a:
        r = [sum(x * y for x, y in zip(row, col)) for col in cols]
        out.append([v % modulus for v in r] if modulus else r)
    return out


def miss_probability(
    a: Matrix, b: Matrix, c: Matrix, values: Sequence[int] = (0, 1), modulus: int | None = None
) -> Fraction:
    """The exact probability that one round says "equal", by enumerating all of values^p."""
    p = len(c[0])
    total = 0
    misses = 0
    for r in itertools.product(values, repeat=p):
        total += 1
        if not detects(a, b, c, r, modulus):
            misses += 1
    return Fraction(misses, total)
