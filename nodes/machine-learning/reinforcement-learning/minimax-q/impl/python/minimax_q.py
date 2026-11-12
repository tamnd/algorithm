# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimax-q/. The authors are listed in prov/ZSSWVB.jsonl.

"""Minimax-Q (Littman, 1994) for two-player zero-sum Markov games.

A game is (R, P, gamma): R[s][i][j] is the reward to the row player (the
maximizer) when it plays i and the column player plays j in state s, and
P[s][i][j] is a dict {next state: probability}. The value of a matrix game is
computed by the simplex method with Bland's rule; with Fraction entries the
result is exact.
"""

import random
from fractions import Fraction


def _pivot(t, r, c):
    piv = t[r][c]
    t[r] = [v / piv for v in t[r]]
    for k in range(len(t)):
        if k != r and t[k][c] != 0:
            f = t[k][c]
            t[k] = [a - f * b for a, b in zip(t[k], t[r])]


def matrix_game(M, eps=0):
    """Value and optimal strategies (value, x, y) of the zero-sum game M,
    where the row player maximizes x^T M y.

    Shift M to be positive. Then max sum(w) s.t. M w <= 1, w >= 0 has optimum
    1 / value, y = w * value, and the dual solution u (min sum(u) s.t.
    M^T u >= 1) gives x = u * value."""
    m, n = len(M), len(M[0])
    lo = min(min(row) for row in M)
    shift = 1 - lo if lo <= 0 else 0
    # tableau rows: m constraints [M + shift | I | 1], objective row [-1..., 0..., 0]
    t = [[M[i][j] + shift for j in range(n)] + [1 if k == i else 0 for k in range(m)] + [1]
         for i in range(m)]
    t.append([-1] * n + [0] * m + [0])
    if isinstance(M[0][0], Fraction):
        t = [[Fraction(v) for v in row] for row in t]
    basis = [n + i for i in range(m)]
    while True:
        col = next((c for c in range(n + m) if t[m][c] < -eps), None)  # Bland: lowest index
        if col is None:
            break
        best = None
        for r in range(m):
            if t[r][col] > eps:
                ratio = t[r][-1] / t[r][col]
                if best is None or ratio < best[0] or (ratio == best[0] and basis[r] < basis[best[1]]):
                    best = (ratio, r)
        _pivot(t, best[1], col)
        basis[best[1]] = col
    total = t[m][-1]
    value = 1 / total
    w = [0] * n
    for r, b in enumerate(basis):
        if b < n:
            w[b] = t[r][-1]
    y = [wj * value for wj in w]
    x = [t[m][n + i] * value for i in range(m)]
    return value - shift, x, y


def closed_form_2x2(M):
    """The 2 x 2 formula: a saddle point if there is one, else the mixed solution."""
    (a, b), (c, d) = M
    lower = max(min(a, b), min(c, d))
    upper = min(max(a, c), max(b, d))
    if lower == upper:
        return lower
    return (a * d - b * c) / (a + d - b - c)


def stage_matrix(game, s, v):
    R, P, gamma = game
    return [[R[s][i][j] + gamma * sum(p * v[t] for t, p in P[s][i][j].items())
             for j in range(len(R[s][0]))] for i in range(len(R[s]))]


def shapley(game, eps, v=None, max_sweeps=10000):
    """Shapley's value iteration v <- val M_s(v), stopped when the change is
    below eps (1 - gamma) / (2 gamma). Returns (v, sweeps)."""
    R, P, gamma = game
    v = list(v) if v is not None else [0 * R[0][0][0]] * len(R)
    for k in range(1, max_sweeps + 1):
        new = [matrix_game(stage_matrix(game, s, v))[0] for s in range(len(R))]
        delta = max(abs(a - b) for a, b in zip(new, v))
        v = new
        if delta < eps * (1 - gamma) / (2 * gamma):
            return v, k
    return v, max_sweeps


def worst_case_value(game, x, tol=1e-12):
    """The value to the row player of the stationary strategy x (x[s] a list of
    probabilities) against a best-responding column player, by value iteration
    on the column player's MDP."""
    R, _, _ = game
    w = [0.0] * len(R)
    while True:
        new = []
        for s in range(len(R)):
            M = stage_matrix(game, s, w)
            new.append(min(sum(x[s][i] * M[i][j] for i in range(len(M)))
                           for j in range(len(M[0]))))
        if max(abs(a - b) for a, b in zip(new, w)) < tol:
            return new
        w = new


def step(game, s, i, j, rng):
    R, P, _ = game
    u, acc = rng.random(), 0.0
    for t, p in P[s][i][j].items():
        acc += p
        if u < acc:
            return R[s][i][j], t
    return R[s][i][j], t


def minimax_q(game, n_steps, rng, explore=1.0, decay=0.6, opponent=None):
    """Minimax-Q. The row player acts uniformly at random with probability
    explore, else by its current strategy pi; the column player acts uniformly
    at random, or by opponent(s, rng). Step size n(s, i, j)^(-decay).
    Returns (Q, V, pi)."""
    R, P, gamma = game
    S = len(R)
    na, no = len(R[0]), len(R[0][0])
    Q = [[[0.0] * no for _ in range(na)] for _ in range(S)]  # @line L1
    V = [0.0] * S  # @line L1
    pi = [[1.0 / na] * na for _ in range(S)]  # @line L1
    count = [[[0] * no for _ in range(na)] for _ in range(S)]
    s = 0
    for _ in range(n_steps):  # @line L2
        if rng.random() < explore:  # @line L3
            i = rng.randrange(na)  # @line L3
        else:
            i = rng.choices(range(na), weights=pi[s])[0]  # @line L3
        j = opponent(s, rng) if opponent else rng.randrange(no)  # @line L4
        r, s2 = step(game, s, i, j, rng)  # @line L4
        count[s][i][j] += 1
        alpha = count[s][i][j] ** -decay  # @line L7
        Q[s][i][j] = (1 - alpha) * Q[s][i][j] + alpha * (r + gamma * V[s2])  # @line L5
        V[s], pi[s], _ = matrix_game(Q[s], eps=1e-12)  # @line L6
        s = s2
    return Q, V, pi  # @line L8


def example_game():
    """The two-state game of the Markov game page, with Fractions; v* = (29/4, 31/4)."""
    h = Fraction(1, 2)
    R = [[[3, -1], [-2, 2]], [[1, 0], [2, 1]]]
    P = [[[{0: 1}, {1: 1}], [{1: 1}, {0: 1}]],
         [[{0: h, 1: h}, {0: h, 1: h}], [{0: h, 1: h}, {0: h, 1: h}]]]
    R = [[[Fraction(x) for x in row] for row in Rs] for Rs in R]
    return R, P, Fraction(9, 10)


def float_game(game):
    R, P, gamma = game
    return ([[[float(x) for x in row] for row in Rs] for Rs in R],
            [[[{t: float(p) for t, p in d.items()} for d in row] for row in Ps] for Ps in P],
            float(gamma))
