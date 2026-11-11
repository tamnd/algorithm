# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blom-scheme/. The authors are listed in prov/809KWA.jsonl.
"""Blom's key predistribution scheme over GF(q) (Blom, Eurocrypt 1984).

A trusted center picks a secret symmetric (k+1) x (k+1) matrix D over GF(q).
User i has a public identity x_i and the public column g_i = (1, x_i, ...,
x_i^k) of a Vandermonde matrix G. The center gives user i the private
vector a_i = D g_i, which is row i of (D G)^T. Users i and j then share
K_ij = a_i . g_j = g_i^T D g_j = g_j^T D g_i = K_ji with no message.

Any k users who pool their vectors learn nothing about a key between two
other users. Any k + 1 users can solve for D and so find every key; the
module has that attack too.

For study only. The code is not constant time. Do not use it to protect
real data. For sensor networks use a maintained library and a reviewed
design; for keys between two parties use X25519 from libsodium or the
Python package cryptography.

Cost: the center does O(k^2) field operations per user; a user does k + 1
multiplications per key and stores k + 1 field elements. The attack by
k + 1 users is one linear solve, O(k^3) field operations.
"""

import random
import secrets
from typing import Optional

Matrix = list[list[int]]


def vandermonde_column(x: int, k: int, q: int) -> list[int]:
    """g = (1, x, x^2, ..., x^k) mod q."""
    g = [1]
    for _ in range(k):
        g.append(g[-1] * x % q)
    return g


def random_symmetric_matrix(k: int, q: int, rng: Optional[random.Random] = None) -> Matrix:
    """A uniform symmetric (k+1) x (k+1) matrix over GF(q)."""
    r = rng or secrets.SystemRandom()
    d = [[0] * (k + 1) for _ in range(k + 1)]
    for i in range(k + 1):
        for j in range(i, k + 1):
            d[i][j] = d[j][i] = r.randrange(q)
    return d


def mat_vec(m: Matrix, v: list[int], q: int) -> list[int]:
    return [sum(a * b for a, b in zip(row, v)) % q for row in m]


def dot(u: list[int], v: list[int], q: int) -> int:
    return sum(a * b for a, b in zip(u, v)) % q


def setup(ids: list[int], k: int, q: int, rng: Optional[random.Random] = None) -> tuple[Matrix, dict[int, list[int]]]:
    """The center: pick D and give each user x the private vector a_x = D g_x."""
    if len(set(ids)) != len(ids) or not all(0 <= x < q for x in ids):
        raise ValueError("identities must be distinct elements of GF(q)")
    d = random_symmetric_matrix(k, q, rng)  # @line L1
    private: dict[int, list[int]] = {}
    for x in ids:
        g = vandermonde_column(x, k, q)  # @line L2
        private[x] = mat_vec(d, g, q)  # @line L3
    return d, private


def shared_key(a_i: list[int], x_j: int, k: int, q: int) -> int:
    """User i computes K_ij = a_i . g_j from its private vector and j's identity."""
    return dot(a_i, vandermonde_column(x_j, k, q), q)  # @line L4


def solve_mod(m: Matrix, b: Matrix, q: int) -> Matrix:
    """Solve m X = b over GF(q), q prime, m square and invertible (Gauss-Jordan)."""
    n = len(m)
    aug = [list(m[i]) + list(b[i]) for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if aug[r][col] % q), None)
        if piv is None:
            raise ValueError("the matrix is singular")
        aug[col], aug[piv] = aug[piv], aug[col]
        inv = pow(aug[col][col], -1, q)
        aug[col] = [v * inv % q for v in aug[col]]
        for r in range(n):
            if r != col and aug[r][col]:
                f = aug[r][col]
                aug[r] = [(v - f * w) % q for v, w in zip(aug[r], aug[col])]
    return [row[n:] for row in aug]


def coalition_recovers_matrix(coalition: dict[int, list[int]], k: int, q: int) -> Matrix:
    """The attack: k + 1 users with vectors a_c = D g_c solve G_C^T D = A^T for D.

    G_C is the Vandermonde matrix of the k + 1 distinct identities, so it is
    invertible, and D is symmetric, so A^T = (D G_C)^T = G_C^T D.
    """
    if len(coalition) != k + 1:
        raise ValueError("the attack needs exactly k + 1 users")
    xs = list(coalition)
    gct = [vandermonde_column(x, k, q) for x in xs]  # row c is g_c^T
    at = [coalition[x] for x in xs]  # row c is a_c^T
    return solve_mod(gct, at, q)
