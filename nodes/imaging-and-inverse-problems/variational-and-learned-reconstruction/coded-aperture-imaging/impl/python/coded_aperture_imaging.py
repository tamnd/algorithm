# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coded-aperture-imaging/. The authors are listed in prov/RBP3GB.jsonl.
"""Coded aperture imaging with uniformly redundant arrays (URAs).

Arrays are 2D lists of rows with cyclic indices; a 1D array of length v is a
single row. The mask A is 0/1. The detector records the cyclic shadow
P(j) = sum_i O(i) A(j - i), and the decoder correlates P with G = 2A - 1.
If A is a (v, k, lam) cyclic difference set with 2 lam - k = -1, then
(A corr G)(d) = (k + 1) delta(d) - 1, so the decoder returns the object exactly.
"""

from fractions import Fraction

Array = list[list[int]]


def legendre(a: int, p: int) -> int:
    """Legendre symbol (a / p) for an odd prime p, by Euler's criterion."""
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def quadratic_residue_ura(p: int) -> Array:
    """1D URA of length p: A(j) = 1 for the nonzero squares mod p.

    For a prime p = 3 mod 4 the squares form a (p, (p-1)/2, (p-3)/4)
    cyclic difference set.
    """
    if not is_prime(p) or p % 4 != 3:
        raise ValueError("p must be a prime with p % 4 == 3")
    return [[1 if legendre(j, p) == 1 else 0 for j in range(p)]]  # @line L1


def twin_prime_ura(r: int) -> Array:
    """r x (r + 2) URA from twin primes r and s = r + 2.

    A(i, 0) = 1 for every i, A(0, j) = 0 for j != 0, and otherwise
    A(i, j) = 1 when (i / r)(j / s) = 1. This is a (rs, (rs-1)/2, (rs-3)/4)
    difference set in Z_r x Z_s.
    """
    s = r + 2
    if not (is_prime(r) and is_prime(s)) or r < 3:
        raise ValueError("r and r + 2 must be odd primes")
    a = [[0] * s for _ in range(r)]
    for i in range(r):
        for j in range(s):
            if j == 0:
                a[i][j] = 1
            elif i != 0 and legendre(i, r) * legendre(j, s) == 1:
                a[i][j] = 1
    return a  # @line L1


def periodic_correlation(a: Array, b: Array) -> Array:
    """(a corr b)(d) = sum_t a(t) b(t + d) with cyclic indices. Cost O(v^2)."""
    n1, n2 = len(a), len(a[0])
    return [[sum(a[t1][t2] * b[(t1 + d1) % n1][(t2 + d2) % n2]
                 for t1 in range(n1) for t2 in range(n2))
             for d2 in range(n2)] for d1 in range(n1)]


def encode(o: Array, a: Array) -> Array:
    """Cyclic shadow P(j) = sum_i O(i) A(j - i). Cost O(v^2)."""
    n1, n2 = len(a), len(a[0])
    return [[sum(o[i1][i2] * a[(j1 - i1) % n1][(j2 - i2) % n2]  # @line L2
                 for i1 in range(n1) for i2 in range(n2))
             for j2 in range(n2)] for j1 in range(n1)]


def adjoint_encode(p: Array, a: Array) -> Array:
    """Adjoint of encode: (A^T P)(i) = sum_j P(j) A(j - i)."""
    n1, n2 = len(a), len(a[0])
    return [[sum(p[j1][j2] * a[(j1 - i1) % n1][(j2 - i2) % n2]
                 for j1 in range(n1) for j2 in range(n2))
             for i2 in range(n2)] for i1 in range(n1)]


def decoding_array(a: Array) -> Array:
    """Balanced decoding array G = 2A - 1."""
    return [[2 * x - 1 for x in row] for row in a]  # @line L3


def decode_scaled(p: Array, a: Array) -> Array:
    """Return k (k + 1) times the decoded object: k C(s) + S.

    For integer data the result is an integer array; it equals
    k (k + 1) O exactly when P = encode(O, A) and A is a URA.
    """
    g = decoding_array(a)
    n1, n2 = len(a), len(a[0])
    k = sum(map(sum, a))  # @line L4
    total = sum(map(sum, p))  # @line L4
    out = [[0] * n2 for _ in range(n1)]
    for s1 in range(n1):  # @line L5
        for s2 in range(n2):  # @line L5
            c = sum(p[j1][j2] * g[(j1 - s1) % n1][(j2 - s2) % n2]  # @line L6
                    for j1 in range(n1) for j2 in range(n2))
            out[s1][s2] = k * c + total  # @line L7
    return out


def decode(p: Array, a: Array) -> list[list[Fraction]]:
    """Decoded object O^(s) = (C(s) + S / k) / (k + 1), as exact fractions."""
    k = sum(map(sum, a))
    scaled = decode_scaled(p, a)
    return [[Fraction(x) / (k * (k + 1)) for x in row] for row in scaled]  # @line L8
