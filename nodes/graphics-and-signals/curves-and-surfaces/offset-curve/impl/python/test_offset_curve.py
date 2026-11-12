# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offset-curve/. The authors are listed in prov/CF6X62.jsonl.

import math
import random
from fractions import Fraction as F

from offset_curve import (
    cusp_parameters,
    offset_curvature,
    offset_derivative,
    offset_point,
    ph_curve,
    ph_offset_point,
    signed_curvature,
)


def cubic(coef):
    C = lambda t: tuple(c[0] + c[1] * t + c[2] * t * t + c[3] * t ** 3 for c in coef)
    d1 = lambda t: tuple(c[1] + 2 * c[2] * t + 3 * c[3] * t * t for c in coef)
    d2 = lambda t: tuple(2 * c[2] + 6 * c[3] * t for c in coef)
    return C, d1, d2


def test_circle_offsets_to_concentric_circles():
    for r in (1.0, 2.5):
        for d in (-1.0, 0.3, 0.9 * r):
            for t in (0.0, 1.0, 2.0, 5.0):
                p = (r * math.cos(t), r * math.sin(t))
                v = (-r * math.sin(t), r * math.cos(t))
                q = offset_point(p, v, d)
                assert abs(math.hypot(*q) - (r - d)) < 1e-12
                # the curvature of the circle of radius r - d
                k = signed_curvature(v, (-p[0], -p[1]))
                assert abs(offset_curvature(k, d) - 1 / (r - d)) < 1e-12


def test_distance_and_derivative_on_random_cubics():
    rng = random.Random(1)
    for _ in range(40):
        coef = [[rng.uniform(-2, 2) for _ in range(4)] for _ in range(2)]
        C, d1, d2 = cubic(coef)
        d = rng.uniform(-0.5, 0.5)
        t = rng.uniform(-1, 1)
        if math.hypot(*d1(t)) < 0.1:
            continue
        q = offset_point(C(t), d1(t), d)
        diff = (q[0] - C(t)[0], q[1] - C(t)[1])
        assert abs(math.hypot(*diff) - abs(d)) < 1e-12
        assert abs(diff[0] * d1(t)[0] + diff[1] * d1(t)[1]) < 1e-12
        # C_d' = (1 - d k) C' against a central difference
        h = 1e-6
        a = offset_point(C(t - h), d1(t - h), d)
        b = offset_point(C(t + h), d1(t + h), d)
        num = ((b[0] - a[0]) / (2 * h), (b[1] - a[1]) / (2 * h))
        ref = offset_derivative(d1(t), d2(t), d)
        assert math.dist(num, ref) < 1e-6 * (1 + math.hypot(*ref))


def test_offset_curvature_against_numeric():
    rng = random.Random(2)
    count = backwards = 0
    for _ in range(60):
        coef = [[rng.uniform(-2, 2) for _ in range(4)] for _ in range(2)]
        C, d1, d2 = cubic(coef)
        d = rng.uniform(-0.3, 0.3)
        t = rng.uniform(-1, 1)
        k = signed_curvature(d1(t), d2(t))
        if math.hypot(*d1(t)) < 0.2 or abs(1 - d * k) < 0.2:
            continue
        h = 1e-4
        P = [offset_point(C(t + j * h), d1(t + j * h), d) for j in (-1, 0, 1)]
        v = ((P[2][0] - P[0][0]) / (2 * h), (P[2][1] - P[0][1]) / (2 * h))
        acc = ((P[2][0] - 2 * P[1][0] + P[0][0]) / h ** 2, (P[2][1] - 2 * P[1][1] + P[0][1]) / h ** 2)
        assert abs(signed_curvature(v, acc) - offset_curvature(k, d)) < 1e-4 * (1 + abs(k))
        count += 1
        backwards += d * k > 1
    assert count > 20 and backwards > 0


def test_parabola_cusps():
    d1 = lambda t: (1.0, 2 * t)
    d2 = lambda t: (0.0, 2.0)
    # d k = 1 with k = 2 / (1 + 4 t^2)^(3/2): t = +-sqrt((2^(2/3) - 1) / 4) for d = 1
    r = cusp_parameters(d1, d2, 1.0, -2.0, 2.0)
    t = math.sqrt((2 ** (2 / 3) - 1) / 4)
    assert len(r) == 2 and abs(r[0] + t) < 1e-12 and abs(r[1] - t) < 1e-12
    assert abs(t - 0.3832104682704) < 1e-12
    # the offset speed factor changes sign at the cusps
    f = lambda s: 1 - signed_curvature(d1(s), d2(s))
    assert f(0.0) < 0 < f(1.0)
    # no cusp when d is below the smallest radius of curvature, 1/2 at the vertex
    assert cusp_parameters(d1, d2, 0.4, -5.0, 5.0) == []
    # offsets to the convex side never have cusps
    assert cusp_parameters(d1, d2, -3.0, -5.0, 5.0) == []
    # the two branches cross on the axis at t = +-sqrt(3)/2, at the point (0, 5/4)
    s = math.sqrt(3) / 2
    for u in (s, -s):
        q = offset_point((u, u * u), d1(u), 1.0)
        assert abs(q[0]) < 1e-15 and abs(q[1] - 1.25) < 1e-15


def test_ph_offset_is_rational_and_exact():
    rng = random.Random(3)
    for _ in range(40):
        u = [F(rng.randint(-3, 3)), F(rng.randint(-3, 3))]
        v = [F(rng.randint(-3, 3)), F(rng.randint(-3, 3))]
        curve = ph_curve(u, v, (F(0), F(0)))
        x, y, sigma, dx, dy = curve
        d = F(rng.randint(-5, 5), rng.randint(1, 3))
        for _ in range(4):
            t = F(rng.randint(-6, 6), rng.randint(1, 4))
            ev = lambda p: sum(c * t ** i for i, c in enumerate(p))
            s = ev(sigma)
            if s == 0:
                continue
            # the hodograph is Pythagorean: x'^2 + y'^2 = sigma^2
            assert ev(dx) ** 2 + ev(dy) ** 2 == s * s
            q = ph_offset_point(curve, t, d)
            assert isinstance(q[0], F) and isinstance(q[1], F)
            diff = (q[0] - ev(x), q[1] - ev(y))
            assert diff[0] ** 2 + diff[1] ** 2 == d * d
            assert diff[0] * ev(dx) + diff[1] * ev(dy) == 0


def test_page_ph_example():
    # u = 1, v = t: C(t) = (t - t^3/3, t^2), sigma = 1 + t^2, k = 2 / (1 + t^2)^2
    curve = ph_curve([F(1)], [F(0), F(1)], (F(0), F(0)))
    x, y, sigma, dx, dy = curve
    assert x == [0, 1, 0, F(-1, 3)] and y == [0, 0, 1] and sigma == [1, 0, 1]
    assert ph_offset_point(curve, F(1), F(1)) == (F(-1, 3), F(1))
    pd1 = lambda t: (1 - t * t, 2 * t)
    pd2 = lambda t: (-2 * t, 2.0)
    r = cusp_parameters(pd1, pd2, 1.0, -2.0, 2.0)
    t = math.sqrt(math.sqrt(2) - 1)
    assert len(r) == 2 and abs(r[1] - t) < 1e-12
