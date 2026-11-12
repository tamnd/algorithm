# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantile-regression/. The authors are listed in prov/HBFAEF.jsonl.

import itertools
import random
from fractions import Fraction as F

from quantile_regression import interpolating_solution, objective, quantile_regression


def solve(A, b):
    """Exact Gaussian elimination; None when A is singular."""
    n = len(A)
    M = [[F(a) for a in row] + [F(c)] for row, c in zip(A, b)]
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * q for a, q in zip(M[i], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def brute_force(X, y, tau):
    """The least objective over all fits that interpolate d points with independent rows."""
    d = len(X[0])
    best = None
    for S in itertools.combinations(range(len(X)), d):
        w = solve([X[i] for i in S], [y[i] for i in S])
        if w is not None:
            v = objective(X, y, tau, w)
            if best is None or v < best:
                best = v
    return best


def rank(rows, d):
    M = [[F(a) for a in r] for r in rows]
    k = 0
    for c in range(d):
        p = next((i for i in range(k, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[k], M[p] = M[p], M[k]
        for i in range(k + 1, len(M)):
            f = M[i][c] / M[k][c]
            M[i] = [a - f * q for a, q in zip(M[i], M[k])]
        k += 1
    return k


EX_X = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6]]
EX_Y = [1, 3, 2, 5, 4, 9]


def test_example_median() -> None:
    w = quantile_regression(EX_X, EX_Y, F(1, 2))
    assert w == [F(-1, 3), F(4, 3)]
    assert objective(EX_X, EX_Y, F(1, 2), w) == 3
    assert brute_force(EX_X, EX_Y, F(1, 2)) == 3


def test_example_quartiles() -> None:
    for tau, want in [(F(1, 4), F(35, 16)), (F(3, 4), F(15, 8))]:
        w = quantile_regression(EX_X, EX_Y, tau)
        assert objective(EX_X, EX_Y, tau, w) == want == brute_force(EX_X, EX_Y, tau)


def test_intercept_only_is_a_sample_quantile() -> None:
    y = [7, 1, 4, 9, 3]
    X = [[1]] * 5
    assert quantile_regression(X, y, F(1, 2)) == [4]
    w = quantile_regression(X, y, F(1, 5))
    assert 1 <= w[0] <= 3  # every value in [y_(1), y_(2)] is a 0.2-quantile


def test_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(500):
        n = rng.randrange(2, 7)
        d = rng.randrange(1, 3)
        X = [[1] + [rng.randrange(-3, 4) for _ in range(d - 1)] for _ in range(n)]
        if rank(X, d) < d:
            continue
        y = [rng.randrange(-5, 6) for _ in range(n)]
        tau = F(rng.randrange(0, 5), 4)
        w = quantile_regression(X, y, tau)
        val = objective(X, y, tau, w)
        assert val == brute_force(X, y, tau)
        # The interpolation theorem: an optimum with zero residuals of rank d.
        v = interpolating_solution(X, y, w)
        assert objective(X, y, tau, v) == val
        res = [F(yi) - sum(F(a) * b for a, b in zip(xi, v)) for xi, yi in zip(X, y)]
        assert rank([X[i] for i in range(n) if res[i] == 0], d) == d
        # With an intercept: #(negative residuals) <= n tau <= n - #(positive residuals).
        neg = sum(1 for xi, yi in zip(X, y) if F(yi) - sum(F(a) * b for a, b in zip(xi, w)) < 0)
        pos = sum(1 for xi, yi in zip(X, y) if F(yi) - sum(F(a) * b for a, b in zip(xi, w)) > 0)
        assert neg <= n * tau <= n - pos


def test_three_features() -> None:
    rng = random.Random(9)
    for _ in range(60):
        X = [[1, rng.randrange(-2, 3), rng.randrange(-2, 3)] for _ in range(6)]
        if rank(X, 3) < 3:
            continue
        y = [rng.randrange(-4, 5) for _ in range(6)]
        tau = F(rng.randrange(1, 4), 4)
        w = quantile_regression(X, y, tau)
        assert objective(X, y, tau, w) == brute_force(X, y, tau)
