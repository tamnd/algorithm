# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discount-factor/. The authors are listed in prov/E1K7NT.jsonl.
"""Three views of the discount factor gamma of a finite MDP, in exact arithmetic.

P[s][a][t] is the transition probability, R[s][a] the expected reward, d a
deterministic stationary policy (d[s] is the action in state s).
"""

from fractions import Fraction
from itertools import product
from typing import List


def _solve(a, b):
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def discounted_value(P, R, d, gamma) -> List[Fraction]:
    """V^d = (I - gamma P^d)^(-1) R^d. Cost O(n^3)."""
    n = len(P)
    a = [[(1 if s == t else 0) - gamma * P[s][d[s]][t] for t in range(n)] for s in range(n)]
    return _solve(a, [R[s][d[s]] for s in range(n)])


def geometric_horizon_value(P, R, d, gamma) -> List[Fraction]:
    """Expected undiscounted total reward when, after each step, the process
    stops with probability 1 - gamma. Builds the chain with one extra absorbing
    state and solves its total reward equations V = r + Q V with V(stop) = 0."""
    n = len(P)
    stop = n
    Q = [[gamma * P[s][d[s]][t] for t in range(n)] + [1 - gamma] for s in range(n)]
    Q.append([Fraction(0)] * n + [Fraction(1)])
    r = [R[s][d[s]] for s in range(n)] + [Fraction(0)]
    a = [[(1 if s == t else 0) - (Q[s][t] if s != stop else 0) for t in range(n + 1)] for s in range(n + 1)]
    return _solve(a, r)[:n]


def undiscounted_k_step(P, R, d, k: int) -> List[Fraction]:
    """E[R_1 + ... + R_k] under d. Cost O(k n^2)."""
    n = len(P)
    v = [Fraction(0)] * n
    for _ in range(k):
        v = [R[s][d[s]] + sum(P[s][d[s]][t] * v[t] for t in range(n)) for s in range(n)]
    return v


def discounted_k_step(P, R, d, gamma, k: int) -> List[Fraction]:
    """E[sum_(t<k) gamma^t R_(t+1)] under d. Cost O(k n^2)."""
    n = len(P)
    v = [Fraction(0)] * n
    for _ in range(k):
        v = [R[s][d[s]] + gamma * sum(P[s][d[s]][t] * v[t] for t in range(n)) for s in range(n)]
    return v


def horizon_for_tolerance(gamma: Fraction, eps: Fraction) -> int:
    """The least H >= 0 with gamma^H <= eps, for 0 < gamma < 1 and 0 < eps."""
    if not (0 < gamma < 1 and eps > 0):
        raise ValueError("need 0 < gamma < 1 and eps > 0")
    h, w = 0, Fraction(1)
    while w > eps:
        h, w = h + 1, w * gamma
    return h


def optimal_policies(P, R, gamma):
    """The deterministic stationary policies that are optimal in every state."""
    n, m = len(P), len(P[0])
    vals = {d: discounted_value(P, R, d, gamma) for d in product(range(m), repeat=n)}
    top = [max(v[s] for v in vals.values()) for s in range(n)]
    return sorted(d for d, v in vals.items() if v == top)
