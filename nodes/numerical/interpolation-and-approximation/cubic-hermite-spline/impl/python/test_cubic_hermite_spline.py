# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cubic-hermite-spline/. The authors are listed in prov/667FMQ.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from cubic_hermite_spline import cubic_hermite_spline, hermite_eval_sorted, three_point_slopes


def oracle_piece(a, b, ya, yb, da, db, t):
    """Independent oracle: Newton form on the nodes a, a, b, b with divided differences."""
    f_ab = (yb - ya) / (b - a)
    f_aab = (f_ab - da) / (b - a)
    f_abb = (db - f_ab) / (b - a)
    f_aabb = (f_abb - f_aab) / (b - a)
    return ya + da * (t - a) + f_aab * (t - a) ** 2 + f_aabb * (t - a) ** 2 * (t - b)


def oracle(xs, ys, ds, t):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    xs, ys, ds = [xs[i] for i in order], [ys[i] for i in order], [ds[i] for i in order]
    k = 0
    while k < len(xs) - 2 and t >= xs[k + 1]:
        k += 1
    return oracle_piece(xs[k], xs[k + 1], ys[k], ys[k + 1], ds[k], ds[k + 1], t)


def test_example_page():
    d = [math.pi / 2, 0.0, -math.pi / 2]
    v = cubic_hermite_spline([0.0, 1.0, 2.0], [0.0, 1.0, 0.0], d, 0.5)
    assert abs(v - (0.5 + math.pi / 16)) < 1e-15
    assert abs(v - math.sin(math.pi / 4)) < (math.pi / 2) ** 4 / 384


def test_random_against_oracle():
    rng = random.Random(1964)
    for _ in range(600):
        n1 = rng.randint(2, 8)
        xs = [F(v, 3) for v in rng.sample(range(-40, 41), n1)]
        ys = [F(rng.randint(-30, 30), rng.randint(1, 5)) for _ in range(n1)]
        ds = [F(rng.randint(-30, 30), rng.randint(1, 5)) for _ in range(n1)]
        lo, hi = min(xs), max(xs)
        for _ in range(3):
            t = lo + (hi - lo) * F(rng.randint(-20, 120), 100)
            assert cubic_hermite_spline(xs, ys, ds, t) == oracle(xs, ys, ds, t)


def test_interpolates_values_and_slopes():
    rng = random.Random(1878)
    for _ in range(100):
        n1 = rng.randint(2, 7)
        xs = sorted(F(v, 2) for v in rng.sample(range(-20, 21), n1))
        ys = [F(rng.randint(-9, 9)) for _ in xs]
        ds = [F(rng.randint(-9, 9)) for _ in xs]
        eps = F(1, 10 ** 6)
        for k, x in enumerate(xs):
            assert hermite_eval_sorted(xs, ys, ds, x) == ys[k]
            if k > 0:  # left slope
                q = (ys[k] - hermite_eval_sorted(xs, ys, ds, x - eps)) / eps
                assert abs(q - ds[k]) < F(1, 1000)
            if k < len(xs) - 1:  # right slope
                q = (hermite_eval_sorted(xs, ys, ds, x + eps) - ys[k]) / eps
                assert abs(q - ds[k]) < F(1, 1000)


def test_cubics_reproduced_and_bessel_exact_on_quadratics():
    xs = [F(3), F(-1), F(7, 2), F(0), F(1, 3)]
    def q(x):
        return 2 * x ** 3 - x ** 2 + 5 * x - 7
    def dq(x):
        return 6 * x ** 2 - 2 * x + 5
    for t in [F(-1), F(-1, 2), F(2), F(17, 5), F(5)]:
        assert cubic_hermite_spline(xs, [q(x) for x in xs], [dq(x) for x in xs], t) == q(t)
    sx = sorted(xs)
    ys = [3 * x * x - x + 1 for x in sx]
    ds = three_point_slopes(sx, ys)
    assert ds == [6 * x - 1 for x in sx]
    for t in [F(-1, 3), F(2), F(13, 4)]:
        assert hermite_eval_sorted(sx, ys, ds, t) == 3 * t * t - t + 1


def test_edges():
    assert cubic_hermite_spline([F(0), F(2)], [F(1), F(5)], [F(2), F(2)], F(1)) == 3
    assert three_point_slopes([F(0), F(2)], [F(1), F(5)]) == [2, 2]
    with pytest.raises(ValueError):
        cubic_hermite_spline([1.0], [1.0], [0.0], 1.0)
    with pytest.raises(ValueError):
        cubic_hermite_spline([0.0, 1.0, 0.0], [1.0, 2.0, 3.0], [0.0, 0.0, 0.0], 0.5)
    with pytest.raises(ValueError):
        cubic_hermite_spline([0.0, 1.0], [1.0, 2.0], [0.0], 0.5)
    xs, ys, ds = [0.0, 0.3, 1.1, 2.0], [1.5, -2.25, 3.0, 0.125], [1.0, -7.0, 2.5, 0.0]
    for x, y in zip(xs, ys):
        assert hermite_eval_sorted(xs, ys, ds, x) == y


def test_error_bound_exact_slopes():
    for f, df, d4 in [(math.exp, math.exp, math.e), (math.sin, math.cos, 1.0)]:
        for n in (1, 2, 4, 8, 16, 32):
            xs = [k / n for k in range(n + 1)]
            ys, ds = [f(x) for x in xs], [df(x) for x in xs]
            bound = d4 / (384 * n ** 4)
            err = max(abs(f(t) - hermite_eval_sorted(xs, ys, ds, t)) for t in [j / 2000 for j in range(2001)])
            assert err <= bound + 1e-15


def test_observed_orders():
    f = math.exp
    grid = [j / 3000 for j in range(3001)]
    e_exact, e_bessel = [], []
    for n in (8, 16, 32, 64):
        xs = [k / n for k in range(n + 1)]
        ys = [f(x) for x in xs]
        e_exact.append(max(abs(f(t) - hermite_eval_sorted(xs, ys, ys, t)) for t in grid))
        d = three_point_slopes(xs, ys)
        e_bessel.append(max(abs(f(t) - hermite_eval_sorted(xs, ys, d, t)) for t in grid))
    for a, b in zip(e_exact, e_exact[1:]):
        assert 14 < a / b < 18
    for a, b in zip(e_bessel, e_bessel[1:]):
        assert 6.5 < a / b < 9.5
