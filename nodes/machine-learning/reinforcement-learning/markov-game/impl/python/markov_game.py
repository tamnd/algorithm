# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-game/. The authors are listed in prov/VR68TW.jsonl.
"""Shapley value iteration for a two-player zero-sum discounted Markov game
in which each player has two actions in each state.

P[s][i][j][t] = Pr(next state t | state s, row action i, column action j)
R[s][i][j]    = expected reward to the row player (the column player gets -R)
The row player maximizes and the column player minimizes.
"""

from typing import List, Tuple


def solve_2x2(M):
    """Value and optimal mixed strategies of the 2x2 matrix game M (row maximizes).
    Returns (value, p, q): the row player plays row 0 with probability p and the
    column player plays column 0 with probability q.
    A saddle point (pure solution) is checked first. Without one, both players
    mix and value = (ad - bc) / (a + d - b - c)."""
    (a, b), (c, d) = M
    row_min = [min(a, b), min(c, d)]
    col_max = [max(a, c), max(b, d)]
    lower, upper = max(row_min), min(col_max)
    if lower == upper:
        p = 1 if row_min[0] == lower else 0
        q = 1 if col_max[0] == upper else 0
        return lower, p, q
    den = a + d - b - c  # nonzero when there is no saddle point
    return (a * d - b * c) / den, (d - c) / den, (d - b) / den


def stage_matrix(P, R, gamma, v, s):
    """The matrix game in state s: R(s, i, j) + gamma sum_t P(t | s, i, j) v(t)."""
    n = len(P)
    return [[R[s][i][j] + gamma * sum(P[s][i][j][t] * v[t] for t in range(n)) for j in range(2)]
            for i in range(2)]


def shapley_operator(P, R, gamma, v):
    """(T v)(s) = val[stage matrix of s]. Returns (T v, row strategies, column strategies)."""
    out, xs, ys = [], [], []
    for s in range(len(P)):
        val, p, q = solve_2x2(stage_matrix(P, R, gamma, v, s))
        out.append(val)
        xs.append(p)
        ys.append(q)
    return out, xs, ys


def shapley_value_iteration(P, R, gamma, eps, v0=None, max_sweeps=100000):
    """Iterate T until ||v_(k+1) - v_k|| < eps (1 - gamma) / (2 gamma).
    Then ||v_(k+1) - v*|| < eps / 2 by the contraction. Returns (v, x, y, sweeps),
    where x and y are the stationary strategies of the last stage games."""
    v = list(v0) if v0 is not None else [0 * R[0][0][0]] * len(P)
    threshold = eps * (1 - gamma) / (2 * gamma) if gamma > 0 else 1
    for k in range(1, max_sweeps + 1):
        w, x, y = shapley_operator(P, R, gamma, v)
        if max(abs(p - q) for p, q in zip(w, v)) < threshold:
            return w, x, y, k
        v = w
    raise RuntimeError("no convergence within max_sweeps")


def _solve_linear(a, b):
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def pair_value(P, R, gamma, x, y) -> List:
    """Value to the row player when both use stationary strategies x and y."""
    n = len(P)
    px = lambda s, i: x[s] if i == 0 else 1 - x[s]
    qy = lambda s, j: y[s] if j == 0 else 1 - y[s]
    a = [[(1 if s == t else 0) - gamma * sum(px(s, i) * qy(s, j) * P[s][i][j][t]
                                               for i in range(2) for j in range(2)) for t in range(n)]
         for s in range(n)]
    r = [sum(px(s, i) * qy(s, j) * R[s][i][j] for i in range(2) for j in range(2)) for s in range(n)]
    return _solve_linear(a, r)


def best_response_values(P, R, gamma, x, y) -> Tuple[List, List]:
    """With y fixed, the row player faces an MDP; with x fixed, so does the column
    player. Returns (the best row value, the best column value, for the row
    player's reward), found by enumeration of the deterministic policies."""
    from itertools import product
    n = len(P)
    best_row, best_col = None, None
    for d in product((1, 0), repeat=n):
        pure = [d[s] for s in range(n)]
        vr = pair_value(P, R, gamma, pure, y)
        vc = pair_value(P, R, gamma, x, pure)
        best_row = vr if best_row is None else [max(p, q) for p, q in zip(best_row, vr)]
        best_col = vc if best_col is None else [min(p, q) for p, q in zip(best_col, vc)]
    return best_row, best_col
