# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-expectation-equation/. The authors are listed in prov/MAY0T7.jsonl.
"""The Bellman expectation equation V = R^pi + gamma P^pi V, solved two ways.

P[s][a][t] is the transition probability, R[s][a] the expected reward and
pi[s][a] the probability of action a in state s. Use Fractions for exact values.
"""

from fractions import Fraction
from itertools import product
from typing import List


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


def policy_model(P, R, pi):
    """Return (P^pi, R^pi), the chain and the expected reward that pi induces."""
    n, m = len(P), len(P[0])
    pp = [[sum(pi[s][a] * P[s][a][t] for a in range(m)) for t in range(n)] for s in range(n)]
    rp = [sum(pi[s][a] * R[s][a] for a in range(m)) for s in range(n)]
    return pp, rp


def bellman_operator(P, R, pi, gamma, v) -> List:
    """(T^pi v)(s) = sum_a pi(a|s) [R(s, a) + gamma sum_t P(t|s, a) v(t)]. Cost O(n^2 m)."""
    n, m = len(P), len(P[0])
    return [sum(pi[s][a] * (R[s][a] + gamma * sum(P[s][a][t] * v[t] for t in range(n))) for a in range(m))
            for s in range(n)]


def bellman_operator_q(P, R, pi, gamma, q) -> List[List]:
    """(T^pi q)(s, a) = R(s, a) + gamma sum_t P(t|s, a) sum_b pi(b|t) q(t, b)."""
    n, m = len(P), len(P[0])
    vq = [sum(pi[t][b] * q[t][b] for b in range(m)) for t in range(n)]
    return [[R[s][a] + gamma * sum(P[s][a][t] * vq[t] for t in range(n)) for a in range(m)] for s in range(n)]


def solve(P, R, pi, gamma) -> List:
    """The unique solution V^pi = (I - gamma P^pi)^(-1) R^pi."""
    pp, rp = policy_model(P, R, pi)
    n = len(P)
    a = [[(1 if s == t else 0) - gamma * pp[s][t] for t in range(n)] for s in range(n)]
    return solve_linear(a, rp)


def iterate(P, R, pi, gamma, v0, sweeps: int) -> List:
    """Apply T^pi to v0 `sweeps` times: iterative policy evaluation."""
    v = list(v0)
    for _ in range(sweeps):
        v = bellman_operator(P, R, pi, gamma, v)
    return v


def truncated_by_paths(P, R, pi, gamma, s0: int, horizon: int):
    """E[sum_(k < horizon) gamma^k R_(k+1) | S_0 = s0] by enumeration of all
    action and next-state sequences. Cost O((n m)^horizon)."""
    n, m = len(P), len(P[0])
    total = Fraction(0)
    for seq in product(range(m), range(n), repeat=horizon):
        prob, ret, s = Fraction(1), Fraction(0), s0
        for i in range(horizon):
            a, t = seq[2 * i], seq[2 * i + 1]
            prob *= pi[s][a] * P[s][a][t]
            if prob == 0:
                break
            ret += gamma ** i * R[s][a]
            s = t
        total += prob * ret
    return total
