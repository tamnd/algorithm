# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/action-value-function/. The authors are listed in prov/VRH12A.jsonl.
"""The action value function Q^pi of a finite discounted MDP.

P[s][a][t] is the transition probability, R[s][a] the expected reward and
pi[s][a] the probability of action a in state s. Use Fractions for exact values.
"""

from fractions import Fraction
from itertools import product
from typing import List, Tuple


def solve_linear(a, b):
    """Solve a x = b by Gaussian elimination with row pivoting. Cost O(k^3)."""
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
    """V^pi = (I - gamma P^pi)^(-1) R^pi. Cost O(n^3)."""
    n, m = len(P), len(P[0])
    a = [[(1 if s == t else 0) - gamma * sum(pi[s][b] * P[s][b][t] for b in range(m)) for t in range(n)] for s in range(n)]
    return solve_linear(a, [sum(pi[s][b] * R[s][b] for b in range(m)) for s in range(n)])


def q_from_v(P, R, gamma, v) -> List[List]:
    """Q(s, a) = R(s, a) + gamma sum_t P(t | s, a) v(t). Cost O(n^2 m)."""
    n, m = len(P), len(P[0])
    return [[R[s][a] + gamma * sum(P[s][a][t] * v[t] for t in range(n)) for a in range(m)] for s in range(n)]


def action_value(P, R, pi, gamma) -> List[List]:
    """Q^pi as the solution of its own linear system on the n m pairs:
    Q(s, a) = R(s, a) + gamma sum_t P(t | s, a) sum_b pi(b | t) Q(t, b).
    Cost O((n m)^3)."""
    n, m = len(P), len(P[0])
    idx = lambda s, a: s * m + a
    k = n * m
    a_mat = [[Fraction(0)] * k for _ in range(k)]
    rhs = [Fraction(0)] * k
    for s in range(n):
        for a in range(m):
            i = idx(s, a)
            a_mat[i][i] += 1
            rhs[i] = R[s][a]
            for t in range(n):
                for b in range(m):
                    a_mat[i][idx(t, b)] -= gamma * P[s][a][t] * pi[t][b]
    x = solve_linear(a_mat, rhs)
    return [[x[idx(s, a)] for a in range(m)] for s in range(n)]


def v_from_q(pi, q) -> List:
    """V^pi(s) = sum_a pi(a | s) Q^pi(s, a)."""
    return [sum(p * x for p, x in zip(pi[s], q[s])) for s in range(len(q))]


def greedy(q) -> Tuple[int, ...]:
    """A deterministic policy that picks a maximizing action in each state (the first one on ties)."""
    return tuple(max(range(len(row)), key=lambda a, row=row: row[a]) for row in q)


def optimal_action_value(P, R, gamma):
    """Q* from V* = the statewise max of V^d over all deterministic policies d."""
    n, m = len(P), len(P[0])
    vstar = None
    for d in product(range(m), repeat=n):
        pi = [[Fraction(1 if b == d[s] else 0) for b in range(m)] for s in range(n)]
        v = state_value(P, R, pi, gamma)
        vstar = v if vstar is None else [max(x, y) for x, y in zip(vstar, v)]
    return q_from_v(P, R, gamma, vstar), vstar
