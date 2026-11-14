# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-trimmed-squares/. The authors are listed in prov/DQP8F6.jsonl.

import random
from fractions import Fraction
from itertools import combinations


def default_h(n, p):
    """h = floor((n + p + 1) / 2), the coverage with the best breakdown point."""
    return (n + p + 1) // 2


def solve(A, b):
    """Solve A z = b exactly by Gaussian elimination; None if A is singular."""
    m = len(A)
    M = [list(map(Fraction, row)) + [Fraction(v)] for row, v in zip(A, b)]
    for c in range(m):
        piv = next((r for r in range(c, m) if M[r][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(m):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [u - f * v for u, v in zip(M[r], M[c])]
    return [M[i][m] / M[i][i] for i in range(m)]


def ols(X, y, idx):
    """Least squares coefficients on the rows idx, by the normal equations."""
    p = len(X[0])
    A = [[sum(X[i][a] * X[i][c] for i in idx) for c in range(p)] for a in range(p)]
    rhs = [sum(X[i][a] * y[i] for i in idx) for a in range(p)]
    return solve(A, rhs)


def residuals2(X, y, b):
    return [(y[i] - sum(u * v for u, v in zip(X[i], b))) ** 2 for i in range(len(y))]


def objective(X, y, b, h):
    """Sum of the h smallest squared residuals."""
    return sum(sorted(residuals2(X, y, b))[:h])


def c_step(X, y, b, h):
    """One concentration step: refit least squares on the h points with the
    smallest squared residuals. The objective never increases."""
    r = residuals2(X, y, b)
    H = sorted(range(len(y)), key=lambda i: r[i])[:h]  # @line L8
    b_new = ols(X, y, H)  # @line L9
    return b if b_new is None else b_new


def fast_lts(X, y, h=None, starts=50, rng=None, max_steps=100):
    """FAST-LTS core: random p-subsets, then C-steps until the objective stops
    falling; keep the best. Returns (coefficients, objective)."""
    rng = rng or random.Random(0)
    X = [[Fraction(v) for v in row] for row in X]
    y = [Fraction(v) for v in y]
    n, p = len(X), len(X[0])
    h = h or default_h(n, p)
    best = None
    for _ in range(starts):  # @line L1
        b = ols(X, y, rng.sample(range(n), p))  # @line L2
        if b is None:
            continue
        q = objective(X, y, b, h)
        for _ in range(max_steps):  # @line L3
            b2 = c_step(X, y, b, h)  # @line L4
            q2 = objective(X, y, b2, h)
            if q2 >= q:  # @line L5
                break
            b, q = b2, q2
        if best is None or q < best[1]:  # @line L6
            best = (b, q)
    if best is None:
        raise ValueError("every random subset was singular")
    return best  # @line L7


def lts_exact(X, y, h=None):
    """Exact LTS by trying every h-subset (small n only). Returns
    (coefficients, objective)."""
    X = [[Fraction(v) for v in row] for row in X]
    y = [Fraction(v) for v in y]
    n, p = len(X), len(X[0])
    h = h or default_h(n, p)
    best = None
    for H in combinations(range(n), h):
        b = ols(X, y, H)
        if b is None:
            continue
        q = sum(residuals2([X[i] for i in H], [y[i] for i in H], b))
        if best is None or q < best[1]:
            best = (b, q)
    return best


def design(x):
    """Rows [1, x_i] for simple regression."""
    return [[1, v] for v in x]
