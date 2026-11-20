# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-n-body-summation/. The authors are listed in prov/14GKBC.jsonl.
"""Direct N-body summation of gravitational accelerations and potential energy.

The bodies have masses m[i] and positions x[i] (tuples of any dimension,
usually 3). The softening parameter eps gives the Plummer pair potential
-G m_i m_j / sqrt(r^2 + eps^2); eps = 0 is Newtonian gravity. Units: G = 1
unless given.

Each of the N(N - 1) / 2 pairs is visited once, and Newton's third law gives
the force on both bodies of the pair.

Cost: N(N - 1) / 2 pair evaluations, Theta(N^2) time, Theta(N) extra space.
"""

import math
from typing import Sequence

Vec = tuple[float, ...]


def direct_sum(m: Sequence[float], x: Sequence[Vec], eps: float = 0.0, G: float = 1.0) -> tuple[list[list[float]], float]:
    """Return (accelerations, potential energy) by summation over all pairs."""
    n = len(m)
    dim = len(x[0]) if n else 0
    a = [[0.0] * dim for _ in range(n)]  # @line L1
    u = 0.0
    e2 = eps * eps
    for i in range(n - 1):  # @line L2
        xi, ai = x[i], a[i]
        for j in range(i + 1, n):  # @line L3
            xj, aj = x[j], a[j]
            d = [xj[k] - xi[k] for k in range(dim)]  # @line L4
            s = sum(c * c for c in d) + e2  # @line L5
            if s == 0.0:
                raise ValueError("two bodies at the same point with eps = 0")
            r = math.sqrt(s)
            w = G / (s * r)  # @line L6
            for k in range(dim):
                ai[k] += m[j] * w * d[k]  # @line L7
                aj[k] -= m[i] * w * d[k]  # @line L8
            u -= G * m[i] * m[j] / r  # @line L9
    return a, u  # @line L10


def accelerations(m: Sequence[float], x: Sequence[Vec], eps: float = 0.0, G: float = 1.0) -> list[list[float]]:
    return direct_sum(m, x, eps, G)[0]


def potential_energy(m: Sequence[float], x: Sequence[Vec], eps: float = 0.0, G: float = 1.0) -> float:
    return direct_sum(m, x, eps, G)[1]


def kinetic_energy(m: Sequence[float], v: Sequence[Vec]) -> float:
    return 0.5 * sum(mi * sum(c * c for c in vi) for mi, vi in zip(m, v))


def leapfrog(m: Sequence[float], x: Sequence[Vec], v: Sequence[Vec], h: float, steps: int, eps: float = 0.0, G: float = 1.0) -> tuple[list[list[float]], list[list[float]]]:
    """Kick-drift-kick leapfrog (velocity Verlet) driven by direct_sum. Used to test the forces in motion."""
    x = [list(p) for p in x]
    v = [list(q) for q in v]
    a = accelerations(m, x, eps, G)
    for _ in range(steps):
        for i in range(len(m)):
            for k in range(len(x[i])):
                v[i][k] += 0.5 * h * a[i][k]
                x[i][k] += h * v[i][k]
        a = accelerations(m, x, eps, G)
        for i in range(len(m)):
            for k in range(len(x[i])):
                v[i][k] += 0.5 * h * a[i][k]
    return x, v
