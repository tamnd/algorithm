# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reward-function/. The authors are listed in prov/AMCRZY.jsonl.
"""The forms of the reward function of a finite MDP and the maps between them.

P[s][a][t] is the transition probability. A reward can be given as
R3[s][a][t] (it depends on the next state), as R[s][a] (its expectation), or
through the joint dynamics p4[s][a] = {(t, r): probability}.
Use fractions.Fraction entries for exact answers.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, List, Tuple


def expected_from_next_state(P, R3) -> List[List[Fraction]]:
    """R(s, a) = sum_t P(t | s, a) R(s, a, t). Cost O(n^2 m)."""
    n, m = len(P), len(P[0])
    return [[sum(P[s][a][t] * R3[s][a][t] for t in range(n)) for a in range(m)] for s in range(n)]


def from_dynamics(p4) -> Tuple[list, list]:
    """Split p(t, r | s, a) into P(t | s, a) and R(s, a) = sum r p(t, r | s, a)."""
    n, m = len(p4), len(p4[0])
    P = [[[Fraction(0)] * n for _ in range(m)] for _ in range(n)]
    R = [[Fraction(0)] * m for _ in range(n)]
    for s in range(n):
        for a in range(m):
            table: Dict[Tuple[int, Fraction], Fraction] = p4[s][a]
            if sum(table.values()) != 1 or min(table.values()) < 0:
                raise ValueError("p(., . | s, a) must be a probability distribution")
            for (t, r), q in table.items():
                P[s][a][t] += q
                R[s][a] += q * r
    return P, R


def affine(R, c, b):
    """The reward c R + b. For c > 0 it keeps the optimal policies of a
    continuing discounted MDP."""
    return [[c * x + b for x in row] for row in R]


def k_step_value_expected(P, R, d, gamma, k: int) -> List[Fraction]:
    """E[sum_(t<k) gamma^t R_(t+1)] under the deterministic stationary policy d,
    from the expected rewards, by k backups. Cost O(k n^2)."""
    n = len(P)
    v = [Fraction(0)] * n
    for _ in range(k):
        v = [R[s][d[s]] + gamma * sum(P[s][d[s]][t] * v[t] for t in range(n)) for s in range(n)]
    return v


def k_step_value_by_paths(P, R3, d, gamma, k: int) -> List[Fraction]:
    """The same quantity from R(s, a, s') by a sum over all n^k state paths."""
    n = len(P)
    out = []
    for s0 in range(n):
        total = Fraction(0)
        for path in product(range(n), repeat=k):
            prob, ret, s = Fraction(1), Fraction(0), s0
            for i, t in enumerate(path):
                prob *= P[s][d[s]][t]
                ret += gamma ** i * R3[s][d[s]][t]
                s = t
            total += prob * ret
        out.append(total)
    return out


def policy_value(P, R, d, gamma) -> List[Fraction]:
    """Exact V^d by Gaussian elimination on (I - gamma P^d) V = R^d."""
    n = len(P)
    m = [[(1 if s == t else 0) - gamma * P[s][d[s]][t] for t in range(n)] + [R[s][d[s]]] for s in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def optimal_deterministic(P, R, gamma):
    """All deterministic stationary policies that are optimal in every state."""
    n, m = len(P), len(P[0])
    vals = {d: policy_value(P, R, d, gamma) for d in product(range(m), repeat=n)}
    top = [max(v[s] for v in vals.values()) for s in range(n)]
    return sorted(d for d, v in vals.items() if v == top)
