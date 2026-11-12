# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dirichlet-process/. The authors are listed in prov/CRF0XV.jsonl.

"""The Dirichlet process DP(alpha, H) through its two constructions: the Chinese restaurant
process (the Blackwell-MacQueen urn) and stick breaking (Sethuraman 1994).
Exact helpers use Fraction for the Ewens sampling formula and the Stirling numbers."""

import math
import random
from fractions import Fraction


def crp(n, alpha, rng: random.Random):
    """Seat n customers. Return the table of each customer (tables numbered 0, 1, ... in order of
    opening) and the table sizes."""
    seats, sizes = [], []  # @line L1
    for i in range(n):  # @line L2
        u = rng.random() * (alpha + i)  # @line L3
        acc, table = 0.0, len(sizes)
        for j, c in enumerate(sizes):
            acc += c
            if u < acc:
                table = j
                break
        if table == len(sizes):  # @line L4
            sizes.append(1)
        else:
            sizes[table] += 1  # @line L5
        seats.append(table)
    return seats, sizes  # @line L6


def polya_urn(n, alpha, base, rng: random.Random):
    """Blackwell-MacQueen: theta_1, ..., theta_n drawn from G ~ DP(alpha, H) with G integrated out.
    base(rng) draws from H."""
    seats, sizes = crp(n, alpha, rng)
    atoms = [base(rng) for _ in sizes]
    return [atoms[t] for t in seats]


def stick_breaking(alpha, k, base, rng: random.Random):
    """The first k weights and atoms of G = sum_k pi_k delta_{theta_k}, and the mass not yet assigned."""
    remaining = 1.0  # @line L7
    weights, atoms = [], []
    for _ in range(k):  # @line L8
        v = rng.betavariate(1.0, alpha)  # @line L9
        weights.append(v * remaining)  # @line L9
        remaining *= 1.0 - v  # @line L9
        atoms.append(base(rng))  # @line L9
    return weights, atoms, remaining  # @line L10


def sequential_probability(seats, alpha):
    """The probability that the CRP produces exactly this seating, as a product of its n steps."""
    p = Fraction(1)
    sizes = []
    for i, t in enumerate(seats):
        if t == len(sizes):
            p *= Fraction(alpha) / (alpha + i)
            sizes.append(1)
        else:
            p *= Fraction(sizes[t]) / (alpha + i)
            sizes[t] += 1
    return p


def rising(a, n):
    r = Fraction(1)
    for i in range(n):
        r *= a + i
    return r


def ewens(block_sizes, alpha):
    """The Ewens sampling formula: alpha^K prod (n_j - 1)! / alpha^(n rising)."""
    n = sum(block_sizes)
    p = Fraction(alpha) ** len(block_sizes)
    for c in block_sizes:
        p *= math.factorial(c - 1)
    return p / rising(Fraction(alpha), n)


def stirling_first_unsigned(n):
    """Table c[m][k] of the unsigned Stirling numbers of the first kind, m, k <= n."""
    c = [[0] * (n + 1) for _ in range(n + 1)]
    c[0][0] = 1
    for m in range(1, n + 1):
        for k in range(1, m + 1):
            c[m][k] = c[m - 1][k - 1] + (m - 1) * c[m - 1][k]
    return c


def number_of_tables_distribution(n, alpha):
    """P(K_n = k) = |s(n, k)| alpha^k / alpha^(n rising), for k = 0 .. n."""
    c = stirling_first_unsigned(n)
    a = Fraction(alpha)
    return [c[n][k] * a ** k / rising(a, n) for k in range(n + 1)]


def expected_tables(n, alpha):
    """E[K_n] = sum_{i=1}^n alpha / (alpha + i - 1)."""
    a = Fraction(alpha)
    return sum(a / (a + i) for i in range(n))


def seatings(n):
    """All seatings of n customers in canonical form (restricted growth strings)."""
    def rec(prefix, m):
        if len(prefix) == n:
            yield list(prefix)
            return
        for t in range(m + 1):
            yield from rec(prefix + [t], max(m, t + 1))
    yield from rec([], 0)


def block_sizes(seats):
    sizes = [0] * (max(seats) + 1)
    for t in seats:
        sizes[t] += 1
    return sizes
