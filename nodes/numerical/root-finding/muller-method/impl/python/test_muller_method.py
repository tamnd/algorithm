# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muller-method/. The authors are listed in prov/1KDQ2S.jsonl.

import cmath
import math
import random
from decimal import Decimal, getcontext

from muller_method import muller

ROOT = 1.5213797068045676  # real root of x^3 - x - 2


def cubic(x):
    return x ** 3 - x - 2


def test_example_cubic():
    r = muller(cubic, 0.0, 1.0, 2.0)
    assert r.root == ROOT and r.reason == "root"
    assert (r.iterations, r.evaluations) == (5, 8)
    assert isinstance(r.root, float)


def test_observed_order_and_rate_in_high_precision():
    getcontext().prec = 300
    x = Decimal("1.5")
    for _ in range(40):
        x -= (x ** 3 - x - 2) / (3 * x * x - 1)
    xs = [Decimal(0), Decimal(1), Decimal(2)]
    fs = [t ** 3 - t - 2 for t in xs]
    errs = [abs(t - x) for t in xs]
    for _ in range(8):
        x0, x1, x2 = xs
        f0, f1, f2 = fs
        h1, h2 = x1 - x0, x2 - x1
        d = ((f2 - f1) / h2 - (f1 - f0) / h1) / (h1 + h2)
        b = (f2 - f1) / h2 + h2 * d
        s = (b * b - 4 * f2 * d).sqrt()
        e = b + s if abs(b + s) >= abs(b - s) else b - s
        x3 = x2 - 2 * f2 / e
        xs, fs = [x1, x2, x3], [f1, f2, x3 ** 3 - x3 - 2]
        errs.append(abs(x3 - x))
    c = 1 / (3 * x * x - 1)  # |f'''/(6 f')|
    for k in range(7, 11):
        assert abs(errs[k] / (errs[k - 1] * errs[k - 2] * errs[k - 3]) - c) < Decimal("1e-6")
    q = (errs[10] / errs[9]).ln() / (errs[9] / errs[8]).ln()
    assert abs(q - Decimal("1.8393")) < Decimal("0.01")


def test_complex_root_from_real_starts():
    r = muller(lambda x: x * x + 1, 0.0, 1.0, 2.0)
    assert r.root == 1j and r.reason == "root" and r.evaluations == 4
    r = muller(lambda x: x ** 3 + 1, 0.0, 0.5, 1.0)
    assert r.converged
    assert abs(r.root - cmath.exp(1j * math.pi / 3)) < 1e-15


def test_root_at_a_starting_point():
    r = muller(cubic, 0.0, ROOT, 2.0)
    assert r.root == ROOT and r.reason == "root" and r.evaluations == 2
    r = muller(lambda x: x - 1, 1, 2, 3)
    assert r.root == 1 and r.evaluations == 1


def test_linear_function_one_step():
    r = muller(lambda x: 3 * x - 1.5, 0.0, 1.0, 2.0)
    assert r.root == 0.5 and r.reason == "root" and r.evaluations == 4


def test_equal_points_and_nan_and_kmax():
    assert muller(cubic, 1.0, 1.0, 2.0).reason == "failure"
    assert muller(cubic, 1.0, 2.0, 1.0).reason == "failure"
    assert muller(lambda x: float("nan"), 0.0, 1.0, 2.0).reason == "failure"
    r = muller(lambda x: math.log(x) if isinstance(x, float) and x > 0 else float("inf"),
               5.0, 6.0, 7.0)
    assert r.reason in ("failure", "converged", "root")
    r = muller(cubic, 0.0, 1.0, 2.0, max_iter=2)
    assert r.reason == "kmax reached" and r.evaluations == 5


def test_constant_function_fails():
    r = muller(lambda x: 1.0, 0.0, 1.0, 2.0)
    assert r.reason == "failure" and r.evaluations == 3


def test_double_root_is_slow_but_ends():
    r = muller(lambda x: (x - 1) ** 2 * (x + 3), 0.0, 0.5, 2.0, max_iter=200)
    assert r.evaluations <= 203
    assert abs(r.root - 1) < 1e-6


def test_random_polynomials():
    rng = random.Random(20261108)
    for _ in range(500):
        n = rng.randint(2, 6)
        zs = [complex(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(n)]

        def p(x, zs=zs):
            v = 1
            for z in zs:
                v *= x - z
            return v

        t = rng.choice(zs)
        r = muller(p, t + 0.1, t - 0.05j, t + 0.02 + 0.03j)
        assert r.converged
        assert min(abs(r.root - z) for z in zs) < 1e-10
        assert r.evaluations <= 3 + 100
