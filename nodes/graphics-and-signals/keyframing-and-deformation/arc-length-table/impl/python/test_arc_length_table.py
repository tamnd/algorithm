# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-length-table/. The authors are listed in prov/JYYH1E.jsonl.
import math
import random

import pytest

from arc_length_table import ArcLengthTable, adaptive_gauss, gauss5


def parabola_d(u):
    return (1.0, 2.0 * u)


def parabola_s(u):
    # Closed form of the arc length of c(u) = (u, u^2) from 0 to u.
    return u * math.sqrt(1.0 + 4.0 * u * u) / 2.0 + math.asinh(2.0 * u) / 4.0


def invert(f, target, lo, hi):
    # Reference inverse of an increasing function by bisection.
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def test_gauss5_is_exact_for_degree_nine(rng=random.Random(1)):
    for _ in range(10):
        c = [rng.uniform(-1, 1) for _ in range(10)]
        f = lambda x: sum(ck * x**k for k, ck in enumerate(c))
        x, y = rng.uniform(-2, 0), rng.uniform(0, 2)
        exact = sum(ck * (y ** (k + 1) - x ** (k + 1)) / (k + 1) for k, ck in enumerate(c))
        assert abs(gauss5(f, x, y) - exact) < 1e-12


def test_adaptive_gauss_on_a_hard_integrand():
    val = adaptive_gauss(lambda x: math.sqrt(x), 0.0, 1.0, 1e-10)
    assert abs(val - 2.0 / 3.0) < 1e-9


def test_parabola_length_and_table_values():
    t = ArcLengthTable(parabola_d, 0.0, 1.0, 16)
    assert abs(t.length() - (2 * math.sqrt(5) + math.asinh(2)) / 4) < 1e-12
    assert abs(t.length() - 1.4789428575445975) < 1e-12
    for uk, sk in zip(t.u, t.s):
        assert abs(sk - parabola_s(uk)) < 1e-12
    for k in range(101):
        assert abs(t.arc_length(k / 100) - parabola_s(k / 100)) < 1e-10


def test_linear_inverse_error_is_second_order():
    errs = []
    for m in (8, 16, 32, 64):
        t = ArcLengthTable(parabola_d, 0.0, 1.0, m)
        worst = 0.0
        for j in range(401):
            s = t.length() * j / 400
            worst = max(worst, abs(t.param(s) - invert(parabola_s, s, 0.0, 1.0)))
        errs.append(worst)
    for e0, e1 in zip(errs, errs[1:]):
        assert 3.0 < e0 / e1 < 5.0
    assert errs[1] < 1e-3


def test_newton_refinement(rng=random.Random(2)):
    t = ArcLengthTable(parabola_d, 0.0, 1.0, 8)
    for _ in range(200):
        s = rng.uniform(0.0, t.length())
        ref = invert(parabola_s, s, 0.0, 1.0)
        e0 = abs(t.param(s) - ref)
        e1 = abs(t.param(s, newton=1) - ref)
        e2 = abs(t.param(s, newton=2) - ref)
        assert e1 <= max(10 * e0 * e0, 1e-12)
        assert e2 < 1e-11


def test_against_a_fine_polyline(rng=random.Random(3)):
    # A random planar cubic Bezier curve; the reference is a polyline of 20000 chords.
    p = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(4)]

    def point(u):
        b = ((1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u**3)
        return tuple(sum(bk * pk[i] for bk, pk in zip(b, p)) for i in range(2))

    def deriv(u):
        b = (-3 * (1 - u) ** 2, 3 * (1 - u) ** 2 - 6 * u * (1 - u), 6 * u * (1 - u) - 3 * u * u, 3 * u * u)
        return tuple(sum(bk * pk[i] for bk, pk in zip(b, p)) for i in range(2))

    n = 20000
    pts = [point(k / n) for k in range(n + 1)]
    poly = [0.0]
    for a, b in zip(pts, pts[1:]):
        poly.append(poly[-1] + math.dist(a, b))
    t = ArcLengthTable(deriv, 0.0, 1.0, 32)
    assert abs(t.length() - poly[-1]) < 1e-6
    for k in range(0, n + 1, 500):
        assert abs(t.arc_length(k / n) - poly[k]) < 1e-6
        u = t.param(poly[k], newton=2)
        assert abs(u - k / n) < 1e-5


def test_constant_speed_curve_is_inverted_exactly():
    r = 2.5
    t = ArcLengthTable(lambda u: (-r * math.sin(u), r * math.cos(u)), 0.0, math.pi, 10)
    assert abs(t.length() - r * math.pi) < 1e-12
    for j in range(50):
        s = t.length() * j / 49
        assert abs(t.param(s) - s / r) < 1e-12


def test_param_is_monotone_and_clamped():
    t = ArcLengthTable(parabola_d, 0.0, 1.0, 5)
    prev = -1.0
    for j in range(1001):
        u = t.param(t.length() * j / 1000)
        assert u >= prev
        prev = u
    assert t.param(-1.0) == 0.0 and abs(t.param(10.0) - 1.0) < 1e-15
    with pytest.raises(ValueError):
        ArcLengthTable(parabola_d, 1.0, 0.0, 4)
