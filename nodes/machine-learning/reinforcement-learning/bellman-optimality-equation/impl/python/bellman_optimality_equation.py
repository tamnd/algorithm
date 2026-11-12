# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-optimality-equation/. The authors are listed in prov/R9MX23.jsonl.
"""The Bellman optimality equation V = max_a [R(., a) + gamma P(. | ., a) V].

The exact solution comes from policy iteration in rational arithmetic, and a
brute force check from the enumeration of all deterministic policies.
P[s][a][t] is the transition probability and R[s][a] the expected reward.
"""

from itertools import product
from typing import List, Tuple


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


def q_values(P, R, gamma, v) -> List[List]:
    """(R(s, a) + gamma sum_t P(t|s, a) v(t)) for all pairs. Cost O(n^2 m)."""
    n, m = len(P), len(P[0])
    return [[R[s][a] + gamma * sum(P[s][a][t] * v[t] for t in range(n)) for a in range(m)] for s in range(n)]


def optimality_operator(P, R, gamma, v) -> List:
    """(T* v)(s) = max_a [R(s, a) + gamma sum_t P(t|s, a) v(t)]."""
    return [max(row) for row in q_values(P, R, gamma, v)]


def optimality_operator_q(P, R, gamma, q) -> List[List]:
    """(T* q)(s, a) = R(s, a) + gamma sum_t P(t|s, a) max_b q(t, b)."""
    return q_values(P, R, gamma, [max(row) for row in q])


def greedy(P, R, gamma, v) -> Tuple[int, ...]:
    """A deterministic policy that is greedy for v (first maximizer on ties)."""
    return tuple(max(range(len(row)), key=lambda a, row=row: row[a]) for row in q_values(P, R, gamma, v))


def policy_value(P, R, gamma, d) -> List:
    """V^d for a deterministic stationary policy d, by a linear solve."""
    n = len(P)
    a = [[(1 if s == t else 0) - gamma * P[s][d[s]][t] for t in range(n)] for s in range(n)]
    return solve_linear(a, [R[s][d[s]] for s in range(n)])


def solve_exact(P, R, gamma):
    """Policy iteration in exact arithmetic. Each step strictly improves the
    value until the greedy policy repeats, so it ends after at most m^n steps.
    Returns (V*, an optimal deterministic policy)."""
    d = tuple(0 for _ in P)
    while True:
        v = policy_value(P, R, gamma, d)
        q = q_values(P, R, gamma, v)
        # keep the current action on ties, so the loop stops
        new = tuple(d[s] if q[s][d[s]] == max(q[s]) else q[s].index(max(q[s])) for s in range(len(P)))
        if new == d:
            return v, d
        d = new


def brute_force(P, R, gamma):
    """The statewise max of V^d over all m^n deterministic policies."""
    best = None
    for d in product(range(len(P[0])), repeat=len(P)):
        v = policy_value(P, R, gamma, d)
        best = v if best is None else [max(x, y) for x, y in zip(best, v)]
    return best


def value_iteration(P, R, gamma, v0, sweeps: int) -> List:
    """Apply T* `sweeps` times."""
    v = list(v0)
    for _ in range(sweeps):
        v = optimality_operator(P, R, gamma, v)
    return v
