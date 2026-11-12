# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-contraction/. The authors are listed in prov/Z62P7P.jsonl.
"""The Bellman operators T^pi and T* of a finite discounted MDP, the max norm,
and value iteration with the stopping rule that the contraction gives.

P[s][a][t] is the transition probability and R[s][a] the expected reward.
Use Fractions for exact checks of the bounds.
"""

from itertools import product
from typing import List, Tuple


def max_norm(u, w=None):
    """||u - w||_inf, or ||u||_inf if w is None."""
    if w is None:
        return max(abs(x) for x in u)
    return max(abs(x - y) for x, y in zip(u, w))


def q_values(P, R, gamma, v):
    n, m = len(P), len(P[0])
    return [[R[s][a] + gamma * sum(P[s][a][t] * v[t] for t in range(n)) for a in range(m)] for s in range(n)]


def t_policy(P, R, pi, gamma, v) -> List:
    """(T^pi v)(s) = sum_a pi(a|s) [R(s, a) + gamma sum_t P(t|s, a) v(t)]."""
    q = q_values(P, R, gamma, v)
    return [sum(p * x for p, x in zip(pi[s], q[s])) for s in range(len(P))]


def t_opt(P, R, gamma, v) -> List:
    """(T* v)(s) = max_a [R(s, a) + gamma sum_t P(t|s, a) v(t)]."""
    return [max(row) for row in q_values(P, R, gamma, v)]


def greedy(P, R, gamma, v) -> Tuple[int, ...]:
    return tuple(max(range(len(row)), key=lambda a, row=row: row[a]) for row in q_values(P, R, gamma, v))


def solve_linear(a, b):
    """Gaussian elimination with row pivoting. Cost O(n^3)."""
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


def policy_value(P, R, gamma, d) -> List:
    """V^d of a deterministic stationary policy d."""
    n = len(P)
    a = [[(1 if s == t else 0) - gamma * P[s][d[s]][t] for t in range(n)] for s in range(n)]
    return solve_linear(a, [R[s][d[s]] for s in range(n)])


def optimal_value(P, R, gamma) -> List:
    """V* as the statewise max over all deterministic policies (brute force)."""
    best = None
    for d in product(range(len(P[0])), repeat=len(P)):
        v = policy_value(P, R, gamma, d)
        best = v if best is None else [max(x, y) for x, y in zip(best, v)]
    return best


def value_iteration(P, R, gamma, eps, v0=None, max_sweeps=100000):
    """Value iteration with the stopping rule ||v_(k+1) - v_k|| < eps (1 - gamma) / (2 gamma).
    Returns (v_(k+1), the greedy policy for v_(k+1), the number of sweeps).
    The greedy policy is eps-optimal and ||v_(k+1) - V*|| < eps / 2 (Puterman, Theorem 6.3.1)."""
    if gamma == 0:
        v = t_opt(P, R, gamma, v0 or [0] * len(P))
        return v, greedy(P, R, gamma, v), 1
    v = list(v0) if v0 is not None else [0 * R[0][0]] * len(P)
    threshold = eps * (1 - gamma) / (2 * gamma)
    for k in range(1, max_sweeps + 1):
        w = t_opt(P, R, gamma, v)
        if max_norm(w, v) < threshold:
            return w, greedy(P, R, gamma, w), k
        v = w
    raise RuntimeError("no convergence within max_sweeps")
