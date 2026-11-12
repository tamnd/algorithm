# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/state-value-function/. The authors are listed in prov/ZWKZEG.jsonl.
"""The state value function V^pi of a finite discounted MDP, three ways.

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


def state_value(P, R, pi, gamma) -> List:
    """V^pi = (I - gamma P^pi)^(-1) R^pi, exact. Cost O(n^2 m + n^3)."""
    n, m = len(P), len(P[0])
    a = [[(1 if s == t else 0) - gamma * sum(pi[s][b] * P[s][b][t] for b in range(m)) for t in range(n)] for s in range(n)]
    r = [sum(pi[s][b] * R[s][b] for b in range(m)) for s in range(n)]
    return solve_linear(a, r)


def truncated_value_by_paths(P, R, pi, gamma, s0: int, horizon: int):
    """E[sum_(t < horizon) gamma^t R_(t+1) | S_0 = s0] by a sum over all
    (action, next state) sequences of length horizon. Cost O((n m)^horizon)."""
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


def sample_return(P, R, pi, gamma: float, s0: int, horizon: int, rng) -> float:
    """One sampled discounted return of `horizon` steps. Rewards are R(s, a)."""
    n, m = len(P), len(P[0])
    s, g, w = s0, 0.0, 1.0
    for _ in range(horizon):
        a = rng.choices(range(m), weights=[float(x) for x in pi[s]])[0]
        g += w * float(R[s][a])
        w *= gamma
        s = rng.choices(range(n), weights=[float(x) for x in P[s][a]])[0]
    return g


def optimal_state_value(P, R, gamma) -> List:
    """V*(s) = max over the deterministic stationary policies d of V^d(s)."""
    n, m = len(P), len(P[0])
    best = None
    for d in product(range(m), repeat=n):
        pi = [[Fraction(1 if b == d[s] else 0) for b in range(m)] for s in range(n)]
        v = state_value(P, R, pi, gamma)
        best = v if best is None else [max(x, y) for x, y in zip(best, v)]
    return best
