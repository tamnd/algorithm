# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-decoding/. The authors are listed in prov/16771S.jsonl.

"""Exhaustive ML, MAP and minimum distance decoders for a small block code.

A discrete memoryless channel is a matrix W with W[x][y] = P(y | x). The
decoders search the whole code, so they cost Θ(|C| n) channel lookups; they
are the reference that faster decoders are tested against.

Soft decisions: BPSK maps bit b to x = 1 - 2b, and the AWGN channel adds
Gaussian noise of variance sigma^2 to each x. ML then maximizes the
correlation sum r_i x_i.
"""

from itertools import product
from math import prod

Vector = tuple[int, ...]
Channel = list[list[float]]


def codewords(g: list[list[int]], q: int = 2) -> list[Vector]:
    k, n = len(g), len(g[0])
    return [tuple(sum(m[i] * g[i][j] for i in range(k)) % q for j in range(n)) for m in product(range(q), repeat=k)]


def likelihood(w: Channel, c: Vector, y: Vector) -> float:
    """P(y | c) on a memoryless channel."""
    return prod(w[a][b] for a, b in zip(c, y))


def ml_decode(code: list[Vector], w: Channel, y: Vector) -> Vector:
    """A codeword that maximizes P(y | c). Ties go to the first codeword in the list."""
    return max(code, key=lambda c: likelihood(w, c, y))


def map_decode(code: list[Vector], prior: list[float], w: Channel, y: Vector) -> Vector:
    """A codeword that maximizes P(c) P(y | c), the posterior up to a constant."""
    i = max(range(len(code)), key=lambda t: prior[t] * likelihood(w, code[t], y))
    return code[i]


def min_distance_decode(code: list[Vector], y: Vector) -> Vector:
    """A codeword at least Hamming distance from y."""
    return min(code, key=lambda c: sum(a != b for a, b in zip(c, y)))


def bsc(p: float) -> Channel:
    return [[1 - p, p], [p, 1 - p]]


def binary_asymmetric(p0: float, p1: float) -> Channel:
    """0 becomes 1 with probability p0, 1 becomes 0 with probability p1."""
    return [[1 - p0, p0], [p1, 1 - p1]]


def soft_ml_decode(code: list[Vector], r: list[float]) -> Vector:
    """ML for BPSK on AWGN: maximize the correlation of r with x = 1 - 2c."""
    return max(code, key=lambda c: sum(ri * (1 - 2 * b) for ri, b in zip(r, c)))
