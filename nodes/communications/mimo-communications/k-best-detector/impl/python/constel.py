# SPDX-License-Identifier: MIT
# Shared helper of the communications pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Constellations, Gray labels and brute-force maximum likelihood detection.

Each constellation function returns a list of M complex points with unit
average energy, ordered by label: points[i] is the point whose bit label is
the integer i, and bits(i, log2 M) gives that label, most significant bit
first. The labels follow the communications area rules:

- M-PAM: the point with amplitude index m = 0, ..., M-1 (raw amplitude
  M - 1 - 2m, from the most positive) gets the Gray label gray(m).
  So 2-PAM maps bit 0 to +1 and bit 1 to -1.
- Square M-QAM, M = 4^k: the label is the in-phase PAM label followed by the
  quadrature PAM label, each of log2(sqrt(M)) bits.
- M-PSK: the point e^(j(2 pi m / M + phase0)) gets the label gray(m).

PAM points are returned as complex numbers with zero imaginary part.
This file imports nothing from cbb.py. It holds no demapper: soft and
max-log demapping are algorithm pages of their own.
"""

import cmath
import itertools
import math


def gray(n: int) -> int:
    """The binary reflected Gray code of n: n XOR (n >> 1)."""
    return n ^ (n >> 1)


def _gray_inv(g: int) -> int:
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n


def bits(i: int, m: int) -> list[int]:
    """The m bits of the integer i, most significant bit first."""
    if i < 0 or i >= 1 << m:
        raise ValueError("i does not fit in m bits")
    return [(i >> (m - 1 - t)) & 1 for t in range(m)]


def _log2(m: int) -> int:
    if m < 2 or m & (m - 1):
        raise ValueError("M must be a power of two, at least 2")
    return m.bit_length() - 1


def pam(m: int) -> list[complex]:
    """Unit-energy M-PAM, ordered by Gray label."""
    _log2(m)
    s = math.sqrt((m * m - 1) / 3.0)
    return [complex((m - 1 - 2 * _gray_inv(lab)) / s, 0.0) for lab in range(m)]


def qam(m: int) -> list[complex]:
    """Unit-energy square M-QAM (M = 4, 16, 64, ...), ordered by label (in-phase bits first)."""
    k = _log2(m)
    if k % 2:
        raise ValueError("square QAM needs M = 4^k")
    side = 1 << (k // 2)
    s = math.sqrt(2.0 * (m - 1) / 3.0)
    raw = [side - 1 - 2 * _gray_inv(lab) for lab in range(side)]
    return [complex(raw[lab // side], raw[lab % side]) / s for lab in range(m)]


def psk(m: int, phase0: float = 0.0) -> list[complex]:
    """Unit-energy M-PSK with first point at angle phase0, ordered by Gray label."""
    _log2(m)
    return [cmath.exp(1j * (2.0 * math.pi * _gray_inv(lab) / m + phase0)) for lab in range(m)]


def energy(points: list[complex]) -> float:
    """The average energy (1/M) sum |p|^2 of equally likely points."""
    return sum(abs(p) ** 2 for p in points) / len(points)


def ml_detect(y: complex, points: list[complex], h: complex = 1) -> int:
    """The index of the point p that minimizes |y - h p|^2, by brute force (lowest index on a tie)."""
    best, arg = math.inf, -1
    for i, p in enumerate(points):
        d = abs(y - h * p) ** 2
        if d < best:
            best, arg = d, i
    return arg


def ml_vector(y: list[complex], h: list[list[complex]], points: list[complex]) -> list[int]:
    """The index vector that minimizes ||y - H x||^2 over all M^n vectors x, by brute force.

    h is the m by n channel matrix as a list of rows; the result has n indices.
    The first minimizer in lexicographic order of the indices wins a tie.
    """
    n = len(h[0])
    best, arg = math.inf, None
    for idx in itertools.product(range(len(points)), repeat=n):
        x = [points[i] for i in idx]
        d = 0.0
        for yi, row in zip(y, h):
            d += abs(yi - sum(a * b for a, b in zip(row, x))) ** 2
        if d < best:
            best, arg = d, idx
    return list(arg)


def bit_errors(a, b) -> int:
    """The number of differing bits between two integer labels, or summed over two equal-length lists."""
    if isinstance(a, int) and isinstance(b, int):
        return bin(a ^ b).count("1")
    if len(a) != len(b):
        raise ValueError("lengths differ")
    return sum(bit_errors(x, y) for x, y in zip(a, b))
