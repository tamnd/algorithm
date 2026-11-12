# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/policy/. The authors are listed in prov/SSS4DF.jsonl.
"""Markov stationary policies of a finite MDP and the state distributions they induce.

P[s][a][t] is the transition probability, pi[s][a] the probability that the
policy takes action a in state s, and mu the initial state distribution.
Use fractions.Fraction entries for exact answers.
"""

from fractions import Fraction
from typing import List, Sequence

Vector = List[Fraction]


def solve_linear(a, b):
    """Solve a x = b by Gaussian elimination with row pivoting. Cost O(n^3)."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def check_policy(pi, num_actions: int) -> None:
    """Raise ValueError if some row of pi is not a probability vector."""
    for row in pi:
        if len(row) != num_actions or min(row) < 0 or sum(row) != 1:
            raise ValueError("each pi[s] must be a probability vector over the actions")


def deterministic(d: Sequence[int], num_actions: int):
    """The table of a deterministic policy d, with d[s] the action in state s."""
    return [[Fraction(1 if a == d[s] else 0) for a in range(num_actions)] for s in range(len(d))]


def induced_chain(P, pi):
    """P^pi(s, t) = sum_a pi(a | s) P(t | s, a). Cost O(n^2 m)."""
    n, m = len(P), len(P[0])
    return [[sum(pi[s][a] * P[s][a][t] for a in range(m)) for t in range(n)] for s in range(n)]


def state_distribution(P, pi, mu: Vector, t: int) -> Vector:
    """The law of S_t: the row vector mu (P^pi)^t. Cost O(t n^2 + n^2 m)."""
    q = induced_chain(P, pi)
    x = list(mu)
    for _ in range(t):
        x = [sum(x[s] * q[s][u] for s in range(len(x))) for u in range(len(x))]
    return x


def discounted_occupancy(P, pi, mu: Vector, gamma) -> Vector:
    """d(s) = (1 - gamma) sum_t gamma^t Pr(S_t = s), found as the solution of
    d = (1 - gamma) mu + gamma d P^pi. Cost O(n^3)."""
    q = induced_chain(P, pi)
    n = len(mu)
    a = [[(1 if s == u else 0) - gamma * q[u][s] for u in range(n)] for s in range(n)]
    return solve_linear(a, [(1 - gamma) * mu[s] for s in range(n)])


def policy_value(P, R, pi, gamma) -> Vector:
    """V^pi = (I - gamma P^pi)^(-1) R^pi. Cost O(n^3)."""
    q = induced_chain(P, pi)
    n, m = len(P), len(P[0])
    r = [sum(pi[s][a] * R[s][a] for a in range(m)) for s in range(n)]
    a = [[(1 if s == u else 0) - gamma * q[s][u] for u in range(n)] for s in range(n)]
    return solve_linear(a, r)
