# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shooting-method/. The authors are listed in prov/XXZ87A.jsonl.

import math

import pytest

from shooting_method import multiple_shooting, profile, rk4, single_shooting

g3 = lambda x, y, p: 2 * y ** 3  # y = 1/(1 + x): y(0) = 1, y(1) = 1/2, y'(0) = -1
g3y = lambda x, y, p: 6 * y * y
zero = lambda x, y, p: 0.0


def test_newton_trace_quadratic():
    r = single_shooting(g3, 0.0, 1.0, 1.0, 0.5, 0.0, n=50, gy=g3y, gp=zero)
    assert abs(r.slope + 1) < 1e-7 and r.iterations <= 6


def test_observed_order_four():
    errs = [abs(single_shooting(g3, 0.0, 1.0, 1.0, 0.5, 0.0, n=n, gy=g3y, gp=zero).slope + 1)
            for n in (5, 10, 20, 40)]
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert all(3.7 < q < 4.3 for q in orders)


def test_secant_matches_newton():
    r1 = single_shooting(g3, 0.0, 1.0, 1.0, 0.5, 0.0, n=40)
    r2 = single_shooting(g3, 0.0, 1.0, 1.0, 0.5, 0.0, n=40, gy=g3y, gp=zero)
    assert abs(r1.slope - r2.slope) < 1e-10


def test_linear_problem_one_newton_step():
    g = lambda x, y, p: y  # y(0) = 0, y(1) = sinh(1): y = sinh x, s = 1
    r = single_shooting(g, 0.0, 1.0, 0.0, math.sinh(1.0), 5.0, n=100, gy=lambda *a: 1.0, gp=zero)
    assert r.iterations <= 2 and abs(r.slope - 1) < 1e-9


def test_bratu_two_solutions():
    lam = 1.0
    g = lambda x, y, p: -lam * math.exp(y)
    gy = lambda x, y, p: -lam * math.exp(y)
    lo = single_shooting(g, 0.0, 1.0, 0.0, 0.0, 0.0, n=100, gy=gy, gp=zero).slope
    hi = single_shooting(g, 0.0, 1.0, 0.0, 0.0, 10.0, n=100, gy=gy, gp=zero).slope

    def exact_slope(t):
        for _ in range(60):  # Newton on t = sqrt(2 lam) cosh(t/4)
            t -= (t - math.sqrt(2 * lam) * math.cosh(t / 4)) / (1 - math.sqrt(2 * lam) * math.sinh(t / 4) / 4)
        return t * math.tanh(t / 4)
    assert abs(lo - exact_slope(1.0)) < 1e-8
    assert abs(hi - exact_slope(10.0)) < 1e-4


def test_single_shooting_unstable_multiple_shooting_fine():
    lam = 40.0
    g = lambda x, y, p: lam * lam * y
    gy = lambda x, y, p: lam * lam
    beta = math.exp(-lam)
    r = single_shooting(g, 0.0, 1.0, 1.0, beta, 0.0, n=400, gy=gy, gp=zero)
    assert abs(r.slope + lam) < 1e-9  # the slope is right ...
    err_single = max(abs(y - math.exp(-lam * x)) for x, y in profile(g, 0.0, 1.0, r.slope, 1.0, 400))
    assert err_single > 1.0  # ... but the computed profile is destroyed by growth e^(40)
    xs, ys, ps, it = multiple_shooting(g, gy, zero, 0.0, 1.0, 1.0, beta, 10, 40)
    assert max(abs(y - math.exp(-lam * x)) for x, y in zip(xs, ys)) < 1e-6


def test_multiple_shooting_nonlinear():
    xs, ys, ps, it = multiple_shooting(g3, g3y, zero, 0.0, 1.0, 1.0, 0.5, 4, 25)
    assert max(abs(y - 1 / (1 + x)) for x, y in zip(xs, ys)) < 1e-8
    assert max(abs(p + 1 / (1 + x) ** 2) for x, p in zip(xs, ps)) < 1e-7
    xs, ys, ps, it = multiple_shooting(g3, g3y, zero, 0.0, 1.0, 1.0, 0.5, 1, 100)  # K = 1 is single shooting
    assert abs(ps[0] + 1) < 1e-7


def test_rk4_and_edge_cases():
    assert abs(rk4(lambda x, u: [u[0]], 0.0, [1.0], 1.0, 20)[0] - math.e) < 1e-6
    with pytest.raises(ValueError):
        rk4(lambda x, u: u, 0.0, [1.0], 1.0, 0)
    with pytest.raises(ValueError):
        multiple_shooting(g3, g3y, zero, 0.0, 1.0, 1.0, 0.5, 0, 10)
    with pytest.raises((ZeroDivisionError, RuntimeError)):  # y'' = -pi^2 y, y(0) = 0: dy(1)/ds = sin(pi)/pi is about 0
        single_shooting(lambda x, y, p: -math.pi ** 2 * y, 0.0, 1.0, 0.0, 1.0, 0.0, n=1000,
                        gy=lambda *a: -math.pi ** 2, gp=zero, tol=1e-15, max_iter=3)
