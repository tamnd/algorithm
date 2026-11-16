# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-newton-algorithm/. The authors are listed in prov/77QE67.jsonl.

import math
import random

import pytest

from gauss_newton_algorithm import cholesky_solve, cost, gauss_newton, normal_equations

T = [0.0, 1.0, 2.0, 3.0]
Y = [2.0 * math.exp(-0.5 * t) for t in T]


def exp_r(x):
    return [x[0] * math.exp(x[1] * t) - y for t, y in zip(T, Y)]


def exp_j(x):
    return [[math.exp(x[1] * t), x[0] * t * math.exp(x[1] * t)] for t in T]


def mnt_r(lam):
    return lambda x: [x[0] + 1.0, lam * x[0] ** 2 + x[0] - 1.0]


def mnt_j(lam):
    return lambda x: [[1.0], [2.0 * lam * x[0] + 1.0]]


def fd_jacobian(f, x, h=1e-6):
    cols = []
    for i in range(len(x)):
        xp = list(x)
        xm = list(x)
        xp[i] += h
        xm[i] -= h
        cols.append([(a - b) / (2 * h) for a, b in zip(f(xp), f(xm))])
    return [[cols[i][k] for i in range(len(x))] for k in range(len(cols[0]))]


def test_jacobian_against_finite_differences():
    rng = random.Random(5)
    for _ in range(20):
        x = [rng.uniform(0.5, 3.0), rng.uniform(-1.0, 0.5)]
        a, b = exp_j(x), fd_jacobian(exp_r, x)
        for ra, rb in zip(a, b):
            for u, v in zip(ra, rb):
                assert abs(u - v) <= 1e-6 * max(1.0, abs(u))


def test_zero_residual_exact_recovery_and_quadratic_rate():
    x, path = gauss_newton(exp_r, exp_j, [1.0, 0.0], eps=1e-15)
    assert abs(x[0] - 2.0) < 1e-10 and abs(x[1] + 0.5) < 1e-10
    errs = [math.hypot(p[0] - 2.0, p[1] + 0.5) for p in path]
    # quadratic: e_{k+1} <= C e_k^2 once e_k is small
    for e0, e1 in zip(errs[1:], errs[2:]):
        if 1e-9 < e0 < 0.2:
            assert e1 <= 2.0 * e0 * e0


def test_linear_residual_one_step_is_least_squares():
    rng = random.Random(11)
    ts = [rng.uniform(-2, 2) for _ in range(12)]
    ys = [0.7 * t - 1.3 + rng.gauss(0, 0.1) for t in ts]
    r = lambda x: [x[0] * t + x[1] - y for t, y in zip(ts, ys)]
    j = lambda x: [[t, 1.0] for t in ts]
    x, path = gauss_newton(r, j, [5.0, 5.0], eps=1e-13)
    # closed form of the line fit
    n = len(ts)
    st, sy = sum(ts), sum(ys)
    stt, sty = sum(t * t for t in ts), sum(t * y for t, y in zip(ts, ys))
    a = (n * sty - st * sy) / (n * stt - st * st)
    b = (sy - a * st) / n
    assert abs(path[1][0] - a) < 1e-10 and abs(path[1][1] - b) < 1e-10
    assert abs(x[0] - a) < 1e-10 and abs(x[1] - b) < 1e-10


def test_nonzero_residual_linear_rate():
    lam = 0.5
    _, path = gauss_newton(mnt_r(lam), mnt_j(lam), [0.1], max_iter=12, eps=1e-300)
    ratios = [p1[0] / p0[0] for p0, p1 in zip(path[3:], path[4:])]
    for q in ratios:
        assert abs(q - lam) < 0.01  # e_{k+1} / e_k tends to lambda


def test_nonzero_residual_failure_near_a_minimum():
    lam = -2.0  # x* = 0 is a strict minimizer (F''(0) = 2 - 2 lambda > 0)
    _, path = gauss_newton(mnt_r(lam), mnt_j(lam), [0.1], max_iter=8, eps=1e-300)
    expect = [0.1, -0.302941, 0.136764, -0.467990, 0.066387]
    for p, e in zip(path, expect):
        assert abs(p[0] - e) < 1e-6
    _, path = gauss_newton(mnt_r(lam), mnt_j(lam), [1e-3], max_iter=40, eps=1e-300)
    assert max(abs(p[0]) for p in path) > 0.1  # the iterates leave the neighborhood


def test_against_grid_minimum_on_one_parameter():
    rate = -0.5
    r = lambda x: [2.0 * math.exp(x[0] * t) - y + 0.01 * (k % 2) for k, (t, y) in enumerate(zip(T, Y))]
    j = lambda x: [[2.0 * t * math.exp(x[0] * t)] for t in T]
    x, _ = gauss_newton(r, j, [-0.3], eps=1e-14)
    grid = min((cost(r([rate + i * 1e-5])), rate + i * 1e-5) for i in range(-3000, 3001))
    assert abs(x[0] - grid[1]) < 2e-5
    assert cost(r(x)) <= grid[0] + 1e-12


def test_rank_deficient_jacobian_raises():
    r = lambda x: [x[0] + x[1] - 1.0, 2 * x[0] + 2 * x[1] - 2.5]
    j = lambda x: [[1.0, 1.0], [2.0, 2.0]]
    with pytest.raises(ValueError):
        gauss_newton(r, j, [0.0, 0.0])


def test_cholesky_solve_and_normal_equations():
    jac = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    a, g = normal_equations(jac, [1.0, 0.0, -1.0])
    assert a == [[35.0, 44.0], [44.0, 56.0]] and g == [-4.0, -4.0]
    x = cholesky_solve(a, g)
    assert abs(35 * x[0] + 44 * x[1] + 4) < 1e-12 and abs(44 * x[0] + 56 * x[1] + 4) < 1e-12
