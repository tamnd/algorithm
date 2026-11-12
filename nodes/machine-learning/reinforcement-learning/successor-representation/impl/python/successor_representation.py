# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successor-representation/. The authors are listed in prov/FGK3ES.jsonl.

"""The successor representation (Dayan 1993): M = (I - gamma P)^{-1}, V = M r, and TD learning of M.

P is the state transition matrix of a fixed policy, as a list of rows. States are 0, ..., n - 1.
"""

import random
from fractions import Fraction
from typing import Sequence


def successor_matrix(p: Sequence[Sequence], gamma) -> list:
    """M = (I - gamma P)^{-1} by Gauss-Jordan elimination; exact when the entries are Fractions."""
    n = len(p)
    a = [[Fraction(int(i == j)) - gamma * p[i][j] for j in range(n)] + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda i: abs(a[i][col]))
        if a[piv][col] == 0:
            raise ValueError("I - gamma P is singular")
        a[col], a[piv] = a[piv], a[col]
        lead = a[col][col]
        a[col] = [x / lead for x in a[col]]
        for i in range(n):
            if i != col and a[i][col] != 0:
                f = a[i][col]
                a[i] = [x - f * y for x, y in zip(a[i], a[col])]
    return [row[n:] for row in a]


def values(m: Sequence[Sequence], r: Sequence) -> list:
    """V = M r: expected discounted reward from each state."""
    return [sum(mij * rj for mij, rj in zip(row, r)) for row in m]


def step(p: Sequence[Sequence], s: int, rng: random.Random) -> int:
    u, acc = rng.random(), 0.0
    for t, pr in enumerate(p[s]):
        acc += float(pr)
        if u < acc:
            return t
    return len(p) - 1


def td_successor(p: Sequence[Sequence], gamma: float, steps: int, rng: random.Random, alpha: float = 0.1, decay: float = 0.0, s0: int = 0) -> list:
    """Learn M along one trajectory of the chain with M(s, :) += a (1_s + gamma M(s', :) - M(s, :)).

    The step size for a state visited k times is alpha / k^decay.
    """
    n = len(p)
    m = [[0.0] * n for _ in range(n)]
    visits = [0] * n
    s = s0
    for _ in range(steps):
        s_next = step(p, s, rng)
        visits[s] += 1
        a = alpha / visits[s] ** decay
        row, nxt = m[s], m[s_next]
        for j in range(n):
            row[j] += a * ((j == s) + gamma * nxt[j] - row[j])
        s = s_next
    return m
