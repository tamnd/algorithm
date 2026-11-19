# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sinusoidal-positional-encoding/. The authors are listed in prov/D6ZPH5.jsonl.

"""The sinusoidal positional encoding of Vaswani et al. (2017).

For an even size d and i = 0, ..., d/2 - 1, with omega_i = base^(-2i/d):

    PE(pos)[2i]     = sin(pos * omega_i)
    PE(pos)[2i + 1] = cos(pos * omega_i)

Coordinates are numbered from 0, as in the paper. The paper also numbers
positions from 0; any integer or real pos is accepted here.

shift_matrix(k, d) is the d x d matrix with PE(pos + k) = shift_matrix(k, d) PE(pos)
for every pos: a block-diagonal matrix of 2 x 2 rotations by k * omega_i.

Precondition: d is even and positive, base > 1.
Cost: Theta(d) operations for one position, Theta(n d) for n positions,
Theta(d^2) to build the shift matrix (only the 2 x 2 blocks are non-zero).
"""

import math
from typing import List

Vector = List[float]
Matrix = List[List[float]]


def _check(d: int, base: float) -> None:
    if d <= 0 or d % 2:
        raise ValueError("d must be even and positive")
    if not base > 1:
        raise ValueError("the base must be greater than 1")


def frequencies(d: int, base: float = 10000.0) -> Vector:
    """The d/2 angular frequencies omega_i = base^(-2i/d), from 1 down to base^(-(d-2)/d)."""
    _check(d, base)
    return [base ** (-2 * i / d) for i in range(d // 2)]


def positional_encoding(pos: float, d: int, base: float = 10000.0) -> Vector:
    """The encoding vector PE(pos) of size d."""
    _check(d, base)
    pe = [0.0] * d
    for i in range(d // 2):  # @line L1
        omega = base ** (-2 * i / d)  # @line L2
        pe[2 * i] = math.sin(pos * omega)  # @line L3
        pe[2 * i + 1] = math.cos(pos * omega)  # @line L4
    return pe  # @line L5


def encoding_matrix(n: int, d: int, start: int = 0, base: float = 10000.0) -> Matrix:
    """The n x d matrix whose row t is PE(start + t)."""
    return [positional_encoding(start + t, d, base) for t in range(n)]


def shift_matrix(k: float, d: int, base: float = 10000.0) -> Matrix:
    """The d x d matrix M_k with PE(pos + k) = M_k PE(pos); it does not depend on pos."""
    _check(d, base)
    m = [[0.0] * d for _ in range(d)]
    for i, omega in enumerate(frequencies(d, base)):
        c, s = math.cos(k * omega), math.sin(k * omega)
        m[2 * i][2 * i], m[2 * i][2 * i + 1] = c, s
        m[2 * i + 1][2 * i], m[2 * i + 1][2 * i + 1] = -s, c
    return m
