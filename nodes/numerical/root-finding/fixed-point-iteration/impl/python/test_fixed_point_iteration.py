# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fixed-point-iteration/. The authors are listed in prov/KFHFSG.jsonl.

import math
import random

import pytest

from fixed_point_iteration import fixed_point_iteration

DOTTIE = 0.7390851332151607
CUBIC_ROOT = 1.5213797068045676


def test_worked_example_cosine():
    r = fixed_point_iteration(math.cos, 1.0, tol=1e-12, lipschitz=math.sin(1.0))
    assert r.converged and abs(r.root - DOTTIE) <= 1e-12
    xs = r.iterates
    assert abs(xs[1] - 0.540302305868) < 1e-12 and abs(xs[12] - 0.741425086610) < 1e-12
    # the ratio of errors tends to g'(x*) = -sin(x*)
    ratio = (xs[40] - DOTTIE) / (xs[39] - DOTTIE)
    assert abs(ratio - (-math.sin(DOTTIE))) < 1e-4


def test_steps_to_1e_minus_10():
    xs = fixed_point_iteration(math.cos, 1.0, tol=0.0, max_iter=200).iterates
    first = next(k for k, x in enumerate(xs) if abs(x - DOTTIE) <= 1e-10)
    assert first == 55


def test_a_posteriori_bound_holds_for_each_step():
    L = math.sin(1.0)
    xs = fixed_point_iteration(math.cos, 0.0, tol=0.0, max_iter=60).iterates
    for k in range(1, len(xs)):
        assert abs(xs[k] - DOTTIE) <= L / (1 - L) * abs(xs[k] - xs[k - 1]) + 1e-15


def test_good_and_bad_rewrites_of_a_cubic():
    good = fixed_point_iteration(lambda x: (x + 2) ** (1 / 3), 1.0, tol=1e-13, lipschitz=0.2)
    assert abs(good.root - CUBIC_ROOT) <= 1e-13
    with pytest.raises(ArithmeticError):
        fixed_point_iteration(lambda x: x ** 3 - 2 if abs(x) < 1e100 else math.inf, 1.6)


def test_observed_linear_rate():
    xs = fixed_point_iteration(lambda x: (x + 2) ** (1 / 3), 1.0, tol=0.0, max_iter=12).iterates
    rate = 1 / (3 * (CUBIC_ROOT + 2) ** (2 / 3))
    for k in range(4, 10):
        q = (xs[k + 1] - CUBIC_ROOT) / (xs[k] - CUBIC_ROOT)
        assert abs(q - rate) < 2e-3


def test_order_two_for_the_newton_map():
    f = lambda x: math.exp(x) - 2
    g = lambda x: x - f(x) / math.exp(x)
    xs = fixed_point_iteration(g, 0.0, tol=0.0, max_iter=5).iterates
    e = [abs(x - math.log(2)) for x in xs[:5]]
    order = math.log(e[3] / e[2]) / math.log(e[2] / e[1])
    assert abs(order - 2) < 0.1


def test_double_root_makes_newton_linear_with_rate_one_half():
    f, df = (lambda x: (x - 1) ** 2), (lambda x: 2 * (x - 1))
    g = lambda x: x - f(x) / df(x) if x != 1 else 1.0
    xs = fixed_point_iteration(g, 3.0, tol=0.0, max_iter=20).iterates
    for k in range(1, 15):
        assert abs((xs[k + 1] - 1) / (xs[k] - 1) - 0.5) < 1e-12


def test_start_at_the_fixed_point():
    r = fixed_point_iteration(lambda x: 2 * x - x * x, 1.0)
    assert r.root == 1.0 and r.evaluations == 1


def test_zero_derivative_constant_map():
    r = fixed_point_iteration(lambda x: 0.25, 7.0, tol=1e-12)
    assert r.root == 0.25 and r.evaluations == 2


def test_max_iterations_and_cycle():
    r = fixed_point_iteration(lambda x: 1 - x, 0.2, tol=1e-12, max_iter=50)
    assert not r.converged and r.evaluations == 50
    r = fixed_point_iteration(math.cos, 1.0, tol=1e-15, max_iter=10)
    assert not r.converged


def test_nan_is_reported():
    with pytest.raises(ArithmeticError):
        fixed_point_iteration(lambda x: math.sqrt(x - 3) if x >= 3 else math.nan, 1.0)


def test_tiny_tolerance_stops_by_max_iter_or_exact_repeat():
    r = fixed_point_iteration(math.cos, 1.0, tol=0.0, max_iter=500)
    assert abs(r.root - DOTTIE) <= 2e-16


def test_random_contractions_meet_the_tolerance():
    rng = random.Random(2024)
    for _ in range(500):
        c = rng.uniform(-10, 10)
        L = rng.uniform(0.05, 0.9)
        g = lambda x: c + L * math.sin(x - c)  # Lipschitz L, fixed point c
        x0 = c + rng.uniform(-20, 20)
        tol = 10.0 ** rng.randint(-12, -4)
        r = fixed_point_iteration(g, x0, tol=tol, lipschitz=L)
        assert r.converged
        assert abs(r.root - c) <= tol + 1e-14
