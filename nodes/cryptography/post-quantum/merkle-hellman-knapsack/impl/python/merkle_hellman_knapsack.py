# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-hellman-knapsack/. The authors are listed in prov/TC99QJ.jsonl.

"""The CJLOSS low-density attack on knapsack (subset sum) cryptosystems.

Coster, Joux, LaMacchia, Odlyzko, Schnorr and Stern (1992) improved the
lattice of Lagarias and Odlyzko (1985): the target vector has entries +1 and
-1 in place of 0 and 1, so it is about half as long, and lattice reduction
finds it for almost all instances of density below 0.9408 when the lattice
oracle finds shortest vectors. Here LLL stands in for that oracle, so the
attack is the practical form of CJLOSS, which works well at small n.

For study only, on toy instances, and not constant time.
"""

import math
import random

from lll import lll_reduce


def density(a) -> float:
    """d = n / log2(max a_i)."""
    return len(a) / math.log2(max(a))


def cjloss_basis(a, s, N=None):
    n = len(a)
    if N is None:
        N = math.isqrt(n) + 1  # @line L1
    rows = []
    for i in range(n):  # @line L2
        rows.append([2 if j == i else 0 for j in range(n)] + [N * a[i]])
    rows.append([1] * n + [N * s])  # @line L3
    return rows


def lo_basis(a, s, N=None):
    """The Lagarias-Odlyzko lattice: rows (e_i, N a_i) and (0, ..., 0, N s)."""
    n = len(a)
    if N is None:
        N = math.isqrt(n) + 1
    rows = [[1 if j == i else 0 for j in range(n)] + [N * a[i]] for i in range(n)]
    rows.append([0] * n + [N * s])
    return rows


def cjloss_attack(a, s):
    """Return a 0/1 vector x with sum x_i a_i = s, or None."""
    n = len(a)
    reduced = lll_reduce(cjloss_basis(a, s))  # @line L4
    for row in reduced:
        for v in (row, [-c for c in row]):  # @line L5
            if v[n] == 0 and all(c in (-1, 1) for c in v[:n]):  # @line L6
                x = [(c + 1) // 2 for c in v[:n]]  # @line L7
                if sum(xi * ai for xi, ai in zip(x, a)) == s:  # @line L8
                    return x
    return None  # @line L9


def lo_attack(a, s):
    """The Lagarias-Odlyzko attack with LLL, for comparison."""
    n = len(a)
    for row in lll_reduce(lo_basis(a, s)):
        for v in (row, [-c for c in row]):
            if v[n] == 0 and all(c in (0, 1) for c in v[:n]) and any(v[:n]):
                x = v[:n]
                if sum(xi * ai for xi, ai in zip(x, a)) == s:
                    return x
    return None


def random_instance(n: int, bits: int, rng: random.Random):
    """Random weights below 2^bits and a target from a random subset of weight n/2."""
    a = [rng.randrange(1, 1 << bits) for _ in range(n)]
    ones = set(rng.sample(range(n), n // 2))
    x = [1 if i in ones else 0 for i in range(n)]
    return a, x, sum(ai for ai, xi in zip(a, x) if xi)


def merkle_hellman_public_key(n: int, rng: random.Random):
    """A basic (single iteration) Merkle-Hellman key: a superincreasing w, then a_i = r w_i mod q."""
    w, total = [], 0
    for _ in range(n):
        v = total + rng.randrange(1, 1 << 4)
        w.append(v)
        total += v
    q = total + rng.randrange(1, 1 << 4)
    while True:
        r = rng.randrange(2, q)
        if math.gcd(r, q) == 1:
            break
    return [r * wi % q for wi in w], (w, q, r)
