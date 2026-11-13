# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-superposition/. The authors are listed in prov/F1S9BZ.jsonl.
"""Superposition of basis states, and the contrast between adding probabilities and adding amplitudes.

States are lists of 2**n complex amplitudes; qubit 0 is the least significant bit of the index.
"""

import itertools
import math
from fractions import Fraction

from qsim import TOL, apply_1q, inner

Vector = list[complex]

R = math.sqrt(0.5)
H = [[complex(R), complex(R)], [complex(R), complex(-R)]]
Z_BASIS = [[1 + 0j, 0j], [0j, 1 + 0j]]
X_BASIS = [[complex(R), complex(R)], [complex(R), complex(-R)]]


def uniform_superposition(n: int) -> Vector:
    """2^(-n/2) times the sum of all 2^n basis states, built by H on each qubit of |0...0>."""
    s = [0j] * (1 << n)
    s[0] = 1 + 0j
    for q in range(n):
        s = apply_1q(s, H, q)
    return s


def coefficients(state: Vector, basis: list[Vector]) -> list[complex]:
    """The amplitudes <e_k|state> in an orthonormal basis e_0, e_1, ..."""
    return [inner(e, state) for e in basis]


def support(state: Vector, basis: list[Vector], tol: float = TOL) -> list[int]:
    """Indices k with a nonzero amplitude <e_k|state>."""
    return [k for k, c in enumerate(coefficients(state, basis)) if abs(c) > tol]


def is_superposition(state: Vector, basis: list[Vector], tol: float = TOL) -> bool:
    """True if the state has two or more nonzero amplitudes in the given basis."""
    return len(support(state, basis, tol)) >= 2


def coin_flip_twice() -> list[Fraction]:
    """A classical bit that starts at 0 and is flipped by a fair coin twice: the distribution stays uniform."""
    m = [[Fraction(1, 2), Fraction(1, 2)], [Fraction(1, 2), Fraction(1, 2)]]
    p = [Fraction(1), Fraction(0)]
    for _ in range(2):
        p = [sum(m[i][j] * p[j] for j in range(2)) for i in range(2)]
    return p


def hadamard_path_sum(k: int, start: int, end: int) -> int:
    """The sum over all bit paths start -> ... -> end of length k of the signs (-1)^(a*b) of the H entries.

    The amplitude <end| H^k |start> is this integer divided by 2^(k/2). Paths with opposite signs cancel.
    """
    total = 0
    for mid in itertools.product((0, 1), repeat=k - 1):
        path = (start, *mid, end)
        sign = 1
        for a, b in zip(path, path[1:]):
            if a & b:
                sign = -sign
        total += sign
    return total


def classical_path_probability(k: int, start: int, end: int) -> Fraction:
    """The probability of end after k fair re-randomizations from start: each path has weight 1/2^k, and none cancel."""
    total = Fraction(0)
    for mid in itertools.product((0, 1), repeat=k - 1):
        path = (start, *mid, end)
        total += Fraction(1, 2 ** (len(path) - 1))
    return total
