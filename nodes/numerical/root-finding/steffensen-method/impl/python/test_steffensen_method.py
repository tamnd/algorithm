# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steffensen-method/. The authors are listed in prov/ZF9XZ7.jsonl.

import math
import random
from fractions import Fraction

from steffensen_method import steffensen, steffensen_fixed_point

DOTTIE = 0.7390851332151607  # root of cos x - x


def test_example_cos():
    r = steffensen(lambda x: math.cos(x) - x, 1.0)
    assert r.root == DOTTIE and r.reason == "root"
    assert (r.iterations, r.evaluations) == (5, 9)


def test_fixed_point_form_matches():
    r = steffensen_fixed_point(math.cos, 1.0)
    assert abs(r.root - DOTTIE) <= 1.2e-16 and r.converged
    assert r.evaluations <= 10


def test_observed_quadratic_order_exact():
    # f(x) = x^2 - 2 in rationals: e_{k+1} / e_k^2 tends to |f''(1 + f')/(2 f')|
    from decimal import Decimal, getcontext
    getcontext().prec = 120
    f = lambda x: x * x - 2
    r2 = Decimal(2).sqrt()
    x = Fraction(3, 2)
    e = []
    for _ in range(6):
        e.append(abs(Decimal(x.numerator) / Decimal(x.denominator) - r2))
        fx = f(x)
        x = x - fx * fx / (f(x + fx) - fx)
    c = (1 + 2 * r2) / (2 * r2)  # f'' = 2 and f' = 2 sqrt 2 at the root
    assert abs(e[5] / e[4] ** 2 - c) < Decimal("1e-6")
    q = (e[5] / e[4]).ln() / (e[4] / e[3]).ln()
    assert abs(q - 2) < Decimal("0.01")


def test_sqrt2_and_far_start():
    r = steffensen(lambda x: x * x - 2, 1.5)
    assert r.converged and abs(r.root - math.sqrt(2)) <= 2.3e-16 and r.evaluations == 10
    r = steffensen(lambda x: x * x - 2, 10.0)
    assert r.converged and abs(r.root - math.sqrt(2)) <= 2.3e-16 and r.iterations == 19


def test_exact_rational_root():
    r = steffensen(lambda x: 3 * x - 1, Fraction(5))
    assert r.root == Fraction(1, 3) and r.reason == "root" and r.evaluations == 3


def test_start_at_root_and_kmax():
    r = steffensen(lambda x: x - 2.0, 2.0)
    assert r.reason == "root" and r.evaluations == 1
    r = steffensen(lambda x: math.exp(x) - 1, 3.0)
    assert r.reason == "kmax reached" and r.evaluations == 200 and r.root > 2.99


def test_zero_slope_and_residual():
    # a flat step function: f(x + f(x)) = f(x), so the slope is 0
    r = steffensen(lambda x: -1.0 if x < 5 else 1.0, 0.0)
    assert r.reason == "failure" and r.evaluations == 2
    # |f(x)| below half an ulp of x: x + f(x) rounds to x
    r = steffensen(lambda x: 2.0 ** -60 * (x - 1), 0.5)
    assert r.reason == "residual" and r.evaluations == 1


def test_double_root_linear():
    r = steffensen(lambda x: (x - 1) ** 2, 3.0)
    assert r.reason == "residual" and abs(r.root - 1) < 1e-7 and r.iterations == 31


def test_nan_and_divergence():
    assert steffensen(lambda x: float("nan"), 1.0).reason == "failure"
    r = steffensen(math.atan, 2.0)
    assert r.reason == "failure" and r.evaluations <= 200


def test_random_cubics():
    rng = random.Random(20261108)
    for _ in range(500):
        z = rng.uniform(-3, 3)
        a = rng.uniform(0.5, 2)
        c = rng.uniform(-1, 1)
        f = lambda x, z=z, a=a, c=c: a * (x - z) + c * (x - z) ** 2 + 0.1 * (x - z) ** 3
        x0 = z + rng.uniform(-0.2, 0.2)
        r = steffensen(f, x0)
        assert r.converged and abs(r.root - z) <= 1e-14 * max(1, abs(z))
        assert r.evaluations <= 20
