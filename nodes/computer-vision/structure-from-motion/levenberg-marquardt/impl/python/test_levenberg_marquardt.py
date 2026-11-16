# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levenberg-marquardt/. The authors are listed in prov/MSS87Z.jsonl.

import math
import random

from levenberg_marquardt import cost, damped_step, levenberg_marquardt, normal_equations

T = [0.0, 1.0, 2.0, 3.0]
Y = [2.0 * math.exp(-0.5 * t) for t in T]


def exp_r(x):
    return [x[0] * math.exp(x[1] * t) - y for t, y in zip(T, Y)]


def exp_j(x):
    return [[math.exp(x[1] * t), x[0] * t * math.exp(x[1] * t)] for t in T]


def rosen_r(x):
    return [10.0 * (x[1] - x[0] ** 2), 1.0 - x[0]]


def rosen_j(x):
    return [[-20.0 * x[0], 10.0], [-1.0, 0.0]]


def mnt_r(lam):
    return lambda x: [x[0] + 1.0, lam * x[0] ** 2 + x[0] - 1.0]


def mnt_j(lam):
    return lambda x: [[1.0], [2.0 * lam * x[0] + 1.0]]


def fd_jacobian(f, x, h=1e-6):
    cols = []
    for i in range(len(x)):
        xp, xm = list(x), list(x)
        xp[i] += h
        xm[i] -= h
        cols.append([(a - b) / (2 * h) for a, b in zip(f(xp), f(xm))])
    return [[cols[i][k] for i in range(len(x))] for k in range(len(cols[0]))]


def test_jacobians_against_finite_differences():
    rng = random.Random(3)
    for f, jf in ((exp_r, exp_j), (rosen_r, rosen_j)):
        for _ in range(10):
            x = [rng.uniform(-1.5, 2.0), rng.uniform(-1.0, 1.0)]
            for ra, rb in zip(jf(x), fd_jacobian(f, x)):
                for u, v in zip(ra, rb):
                    assert abs(u - v) <= 1e-5 * max(1.0, abs(u))


def test_rosenbrock_from_standard_start():
    for tau in (1e-3, 1.0):
        for marq in (False, True):
            x, info = levenberg_marquardt(rosen_r, rosen_j, [-1.2, 1.0], tau=tau, marquardt=marq)
            assert abs(x[0] - 1.0) < 1e-6 and abs(x[1] - 1.0) < 1e-6
            costs = info["costs"]
            assert all(c1 < c0 for c0, c1 in zip(costs, costs[1:]))


def test_zero_residual_exact_recovery():
    x, info = levenberg_marquardt(exp_r, exp_j, [1.0, 0.0])
    assert abs(x[0] - 2.0) < 1e-8 and abs(x[1] + 0.5) < 1e-8
    assert info["costs"][-1] < 1e-20


def test_converges_where_gauss_newton_fails():
    # with lambda = -2 the full Gauss-Newton step does not converge to x* = 0
    x, info = levenberg_marquardt(mnt_r(-2.0), mnt_j(-2.0), [0.1], tau=1.0)
    assert abs(x[0]) < 1e-6
    costs = info["costs"]
    assert all(c1 < c0 for c0, c1 in zip(costs, costs[1:]))
    assert abs(costs[-1] - 1.0) < 1e-10  # F(0) = 1, the residual is not zero


def test_step_limits():
    # large mu: the step tends to -g / mu (steepest descent); mu -> 0: Gauss-Newton
    x = [-1.2, 1.0]
    a, g = normal_equations(rosen_j(x), rosen_r(x))
    h = damped_step(a, g, 1e8)
    for hi, gi in zip(h, g):
        assert abs(hi * 1e8 + gi) < 1e-4 * max(1.0, abs(gi))
    h0 = damped_step(a, g, 0.0)
    h1 = damped_step(a, g, 1e-12)
    assert all(abs(u - v) < 1e-8 for u, v in zip(h0, h1))


def test_step_length_decreases_with_mu_and_model_decrease_is_positive():
    rng = random.Random(17)
    for _ in range(20):
        x = [rng.uniform(-2, 2), rng.uniform(-1, 3)]
        a, g = normal_equations(rosen_j(x), rosen_r(x))
        last = float("inf")
        for mu in (1e-3, 1e-1, 1.0, 10.0, 100.0):
            h = damped_step(a, g, mu)
            n = math.sqrt(sum(v * v for v in h))
            assert n <= last + 1e-12
            last = n
            pred = 0.5 * sum(hi * (mu * hi - gi) for hi, gi in zip(h, g))
            jh = [sum(row[i] * h[i] for i in range(2)) for row in rosen_j(x)]
            lin = cost([ri + ji for ri, ji in zip(rosen_r(x), jh)])
            assert pred > 0 and abs(pred - (cost(rosen_r(x)) - lin)) < 1e-9 * max(1.0, pred)


def test_against_grid_minimum():
    x, _ = levenberg_marquardt(mnt_r(0.5), mnt_j(0.5), [0.7], tau=1e-2)
    f = lambda v: cost(mnt_r(0.5)([v]))
    best = min((f(-1.0 + i * 1e-4), -1.0 + i * 1e-4) for i in range(20001))
    assert abs(x[0] - best[1]) < 2e-4 and f(x[0]) <= best[0] + 1e-12
