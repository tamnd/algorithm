# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zadoff-chu-sequence/. The authors are listed in prov/MHXFB8.jsonl.

"""Zadoff-Chu sequences and their periodic correlations.

For a root u with gcd(u, N) = 1:
    x_u[n] = exp(-j pi u n (n + 1) / N)   for odd N,
    x_u[n] = exp(-j pi u n^2 / N)         for even N,
for n = 0, ..., N - 1. The periodic correlation at shift t is
    C(t) = sum over n of x[n] conj(y[(n + t) mod N]).
"""

import cmath
import math


def zadoff_chu(u: int, n: int) -> list[complex]:
    """The Zadoff-Chu sequence of root u and length n (gcd(u, n) = 1)."""
    if n < 1 or math.gcd(u, n) != 1:
        raise ValueError("need n >= 1 and gcd(u, n) = 1")
    c = n % 2  # @line L1
    return [cmath.exp(-1j * math.pi * u * k * (k + c) / n) for k in range(n)]  # @line L2


def zc_exponents(u: int, n: int) -> list[int]:
    """For odd n: the integers m[k] = u k (k + 1) / 2 mod n, so that x_u[k] = exp(-j 2 pi m[k] / n)."""
    if n % 2 == 0:
        raise ValueError("n must be odd")
    return [(u * k * (k + 1) // 2) % n for k in range(n)]


def periodic_corr(x: list[complex], y: list[complex], t: int) -> complex:
    """C(t) = sum over k of x[k] conj(y[(k + t) mod N])."""
    n = len(x)
    if len(y) != n:
        raise ValueError("lengths differ")
    return sum(x[k] * y[(k + t) % n].conjugate() for k in range(n))  # @line L3


def corr_all(x: list[complex], y: list[complex]) -> list[complex]:
    """C(t) for t = 0, ..., N - 1."""
    return [periodic_corr(x, y, t) for t in range(len(x))]


def corr_exact_odd(u1: int, u2: int, n: int, t: int) -> tuple[int, list[int]]:
    """C(t) for two Zadoff-Chu sequences of odd length n, exactly, as a sum of n-th roots of unity.

    Returns (n, counts) where counts[r] is how many k give the root exp(-j 2 pi r / n),
    so that C(t) = sum over r of counts[r] exp(-j 2 pi r / n). Integer arithmetic only.
    """
    a = zc_exponents(u1, n)
    b = zc_exponents(u2, n)
    counts = [0] * n
    for k in range(n):
        counts[(a[k] - b[(k + t) % n]) % n] += 1
    return n, counts
