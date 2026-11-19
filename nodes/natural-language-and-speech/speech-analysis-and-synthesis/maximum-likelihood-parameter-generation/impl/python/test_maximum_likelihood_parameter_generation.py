# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-parameter-generation/. The authors are listed in prov/5JS7A5.jsonl.

import random
import time
from fractions import Fraction as F

import pytest

from maximum_likelihood_parameter_generation import (
    DELTA,
    DELTA2,
    STATIC,
    banded_ldl_solve,
    expand_states,
    half_bandwidth,
    log_likelihood_quadratic,
    mlpg,
    normal_equations,
    window_rows,
)

FSTATIC = {0: F(1)}
FDELTA = {-1: F(-1, 2), 1: F(1, 2)}
FDELTA2 = {-1: F(1), 0: F(-2), 1: F(1)}
FWIDE = {-2: F(-1, 5), -1: F(-1, 10), 1: F(1, 10), 2: F(1, 5)}


def dense_solve(A, y):
    """Gaussian elimination with exact pivot search, for Fraction matrices."""
    n = len(A)
    M = [list(A[i]) + [y[i]] for i in range(n)]
    for col in range(n):
        piv = next(i for i in range(col, n) if M[i][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        for i in range(n):
            if i != col and M[i][col] != 0:
                f = M[i][col] / M[col][col]
                M[i] = [a - f * b for a, b in zip(M[i], M[col])]
    return [M[i][n] / M[i][i] for i in range(n)]


def dense_normal_equations(mu, var, windows, edge="clamp"):
    """W, then W^T U^-1 W and W^T U^-1 mu, with W built as a full matrix."""
    T = len(mu)
    W, m, u = [], [], []
    for t in range(T):
        for d, w in enumerate(windows):
            row = [F(0)] * T
            for tau, coef in w.items():
                if 0 <= t + tau < T:
                    row[t + tau] += coef
                elif edge == "clamp":
                    row[0 if t + tau < 0 else T - 1] += coef
            W.append(row)
            m.append(mu[t][d])
            u.append(var[t][d])
    A = [[sum(W[k][i] * W[k][j] / u[k] for k in range(len(W))) for j in range(T)] for i in range(T)]
    y = [sum(W[k][i] * m[k] / u[k] for k in range(len(W))) for i in range(T)]
    return A, y


def random_frames(rng, T, D):
    mu = [[F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(D)] for _ in range(T)]
    var = [[F(rng.randint(1, 9), rng.randint(1, 4)) for _ in range(D)] for _ in range(T)]
    return mu, var


WINDOW_SETS = [
    [FSTATIC],
    [FSTATIC, FDELTA],
    [FSTATIC, FDELTA, FDELTA2],
    [FSTATIC, FWIDE],
    [FSTATIC, FWIDE, FDELTA2],
]


@pytest.mark.parametrize("edge", ["clamp", "zero"])
@pytest.mark.parametrize("k", range(len(WINDOW_SETS)))
def test_exact_against_dense_gaussian_elimination(k, edge):
    windows = WINDOW_SETS[k]
    rng = random.Random(100 + k)
    for T in range(1, 9):
        mu, var = random_frames(rng, T, len(windows))
        A, y = dense_normal_equations(mu, var, windows, edge)
        assert mlpg(mu, var, windows, edge) == dense_solve(A, y)


@pytest.mark.parametrize("edge", ["clamp", "zero"])
def test_banded_matrix_matches_dense_and_band(edge):
    rng = random.Random(7)
    windows = [FSTATIC, FWIDE, FDELTA2]
    T = 9
    mu, var = random_frames(rng, T, 3)
    P, r, b = normal_equations(mu, var, windows, edge)
    A, y = dense_normal_equations(mu, var, windows, edge)
    assert b == 4 == half_bandwidth(windows)
    for i in range(T):
        for j in range(T):
            if abs(i - j) > b:
                assert A[i][j] == 0
            elif i >= j:
                assert P.get((i, j), 0) == A[i][j]
    assert r == y


def test_static_window_alone_returns_the_means():
    rng = random.Random(3)
    mu, var = random_frames(rng, 7, 1)
    assert mlpg(mu, var, [FSTATIC]) == [row[0] for row in mu]


def test_gradient_is_zero_and_perturbations_lower_the_likelihood():
    rng = random.Random(9)
    windows = [FSTATIC, FDELTA, FDELTA2]
    for T in (2, 5, 8):
        mu, var = random_frames(rng, T, 3)
        c = mlpg(mu, var, windows)
        P, r, b = normal_equations(mu, var, windows)
        for i in range(T):
            pc = sum(P.get((max(i, j), min(i, j)), 0) * c[j] for j in range(T))
            assert pc == r[i]
        best = log_likelihood_quadratic(c, mu, var, windows)
        for _ in range(10):
            e = [F(rng.randint(-3, 3), 7) for _ in range(T)]
            if all(x == 0 for x in e):
                continue
            moved = [a + x for a, x in zip(c, e)]
            assert log_likelihood_quadratic(moved, mu, var, windows) < best


def test_float_matches_fraction():
    rng = random.Random(21)
    for T in (1, 4, 12):
        mu, var = random_frames(rng, T, 3)
        exact = mlpg(mu, var, [FSTATIC, FDELTA, FDELTA2])
        fl = mlpg([[float(x) for x in row] for row in mu], [[float(x) for x in row] for row in var], [STATIC, DELTA, DELTA2])
        for a, b in zip(exact, fl):
            assert b == pytest.approx(float(a), rel=1e-9, abs=1e-9)


def test_singular_system_raises():
    # Delta alone: with clamped ends a constant trajectory has every delta 0,
    # and with zero ends on 3 frames the rows are c1 / 2, (c2 - c0) / 2 and
    # -c1 / 2, so c0 + c2 is not determined. W^T U^-1 W is singular in both.
    mu = [[F(0)], [F(1)], [F(0)]]
    var = [[F(1)]] * 3
    for edge in ("clamp", "zero"):
        with pytest.raises(ValueError):
            mlpg(mu, var, [FDELTA], edge)
    with pytest.raises(ValueError):
        mlpg(mu, var, [FDELTA], "mirror")


def test_bad_input_raises():
    with pytest.raises(ValueError):
        mlpg([[0.0, 0.0]], [[1.0, 0.0]], [STATIC, DELTA])
    with pytest.raises(ValueError):
        mlpg([[0.0]], [[1.0]], [STATIC, DELTA])
    assert mlpg([], [], [STATIC, DELTA]) == []


def test_window_rows_at_the_ends():
    rows = window_rows(3, [FSTATIC, FDELTA], "zero")
    assert rows[1] == (0, 1, [(1, F(1, 2))])
    assert rows[5] == (2, 1, [(1, F(-1, 2))])
    rows = window_rows(3, [FSTATIC, FDELTA], "clamp")
    assert rows[1] == (0, 1, [(0, F(-1, 2)), (1, F(1, 2))])
    assert rows[5] == (2, 1, [(1, F(-1, 2)), (2, F(1, 2))])


def test_two_state_example():
    # The example of the page: states with static means 0 and 1, 3 frames each,
    # delta mean 0, static variance 1 and delta variance 1/4, clamped ends.
    mu, var = expand_states([[F(0), F(0)], [F(1), F(0)]], [[F(1), F(1, 4)], [F(1), F(1, 4)]], [3, 3])
    windows = [FSTATIC, FDELTA]
    c = mlpg(mu, var, windows)
    assert c == [F(1, 5), F(3, 10), F(3, 10), F(7, 10), F(7, 10), F(4, 5)]
    assert log_likelihood_quadratic(c, mu, var, windows) == F(-2, 5)
    assert log_likelihood_quadratic([row[0] for row in mu], mu, var, windows) == -1
    c3 = mlpg(*expand_states([[F(0)] * 3, [F(1), F(0), F(0)]], [[F(1), F(1, 4), F(1, 4)]] * 2, [3, 3]), [FSTATIC, FDELTA, FDELTA2])
    assert c3 == [F(163, 693), F(409, 1386), F(577, 1386), F(809, 1386), F(977, 1386), F(530, 693)]
    # With zero ends the delta-delta window pulls the last frame toward 0.
    cz = mlpg(*expand_states([[F(0)] * 3, [F(1), F(0), F(0)]], [[F(1), F(1, 4), F(1, 4)]] * 2, [3, 3]), [FSTATIC, FDELTA, FDELTA2], "zero")
    assert cz[5] < cz[4]


def test_long_float_run_is_linear_and_solves_the_system():
    rng = random.Random(5)
    T = 3000
    mu = [[rng.uniform(-1, 1), rng.uniform(-0.1, 0.1), rng.uniform(-0.1, 0.1)] for _ in range(T)]
    var = [[rng.uniform(0.5, 2), rng.uniform(0.05, 0.2), rng.uniform(0.05, 0.2)] for _ in range(T)]
    start = time.perf_counter()
    c = mlpg(mu, var, [STATIC, DELTA, DELTA2])
    assert time.perf_counter() - start < 5
    P, r, b = normal_equations(mu, var, [STATIC, DELTA, DELTA2])
    for i in range(0, T, 97):
        pc = sum(P.get((max(i, j), min(i, j)), 0.0) * c[j] for j in range(max(0, i - b), min(T, i + b + 1)))
        assert pc == pytest.approx(r[i], abs=1e-9)
    assert banded_ldl_solve(P, r, b) == c
