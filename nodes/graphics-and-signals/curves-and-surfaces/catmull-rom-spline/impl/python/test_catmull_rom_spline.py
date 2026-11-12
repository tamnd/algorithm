# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/catmull-rom-spline/. The authors are listed in prov/SBH6DE.jsonl.

import random
from fractions import Fraction as F

from catmull_rom_spline import (
    alpha_knots,
    barry_goldman,
    catmull_rom_curve,
    nonuniform_tangent,
    uniform_segment,
    uniform_tangents,
)


def hermite(p0, m0, p1, m1, u):
    """Reference: the cubic Hermite segment."""
    h0 = 2 * u ** 3 - 3 * u ** 2 + 1
    h1 = u ** 3 - 2 * u ** 2 + u
    h2 = u ** 3 - u ** 2
    h3 = -2 * u ** 3 + 3 * u ** 2
    return tuple(h0 * a + h1 * b + h2 * c + h3 * d for a, b, c, d in zip(p0, m0, m1, p1))


def lagrange_slope(p, ts):
    """Reference: derivative at ts[1] of the quadratic through (ts[k], p[k]), k = 0, 1, 2."""
    t0, t1, t2 = ts
    w0 = (t1 - t2) / ((t0 - t1) * (t0 - t2))
    w1 = (2 * t1 - t0 - t2) / ((t1 - t0) * (t1 - t2))
    w2 = (t1 - t0) / ((t2 - t0) * (t2 - t1))
    return tuple(w0 * a + w1 * b + w2 * c for a, b, c in zip(*p))


def rp(rng, d):
    return tuple(F(rng.randint(-30, 30), rng.randint(1, 6)) for _ in range(d))


def test_uniform_is_hermite_with_half_chord_tangents():
    rng = random.Random(1)
    for _ in range(500):
        d = rng.choice([2, 3])
        p = [rp(rng, d) for _ in range(4)]
        m1 = tuple((c - a) / 2 for a, c in zip(p[0], p[2]))
        m2 = tuple((c - a) / 2 for a, c in zip(p[1], p[3]))
        u = F(rng.randint(-5, 15), rng.randint(1, 10))
        assert uniform_segment(*p, u) == hermite(p[1], m1, p[2], m2, u)


def test_uniform_c1_joints_and_interpolation():
    rng = random.Random(2)
    jumps = 0
    for _ in range(150):
        n = rng.randint(4, 6)
        pts = [rp(rng, 2) for _ in range(n + 1)]
        tans = uniform_tangents(pts)
        for i in range(1, n - 1):
            seg = pts[i - 1 : i + 3]
            assert uniform_segment(*seg, F(0)) == pts[i]
            assert uniform_segment(*seg, F(1)) == pts[i + 1]
            assert uniform_segment(*seg, F(0), 1) == tans[i - 1]
            assert uniform_segment(*seg, F(1), 1) == tans[i]
        for i in range(1, n - 2):
            left = pts[i - 1 : i + 3]
            right = pts[i : i + 4]
            assert uniform_segment(*left, F(1)) == uniform_segment(*right, F(0))
            assert uniform_segment(*left, F(1), 1) == uniform_segment(*right, F(0), 1)
            if uniform_segment(*left, F(1), 2) != uniform_segment(*right, F(0), 2):
                jumps += 1
    assert jumps > 0


def test_reproduces_quadratics():
    rng = random.Random(3)
    for _ in range(500):
        a, b, c = rp(rng, 3), rp(rng, 3), rp(rng, 3)

        def q(s):
            return tuple(x + y * s + z * s * s for x, y, z in zip(a, b, c))

        i = rng.randint(-5, 5)
        pts = [q(F(i + k)) for k in range(-1, 3)]
        u = F(rng.randint(0, 20), 20)
        assert uniform_segment(*pts, u) == q(i + u)


def test_barry_goldman_uniform_knots_match_matrix_form():
    rng = random.Random(4)
    for _ in range(500):
        p = [rp(rng, 2) for _ in range(4)]
        u = F(rng.randint(0, 30), 30)
        assert barry_goldman(p, [F(-1), F(0), F(1), F(2)], u) == uniform_segment(*p, u)


def test_barry_goldman_nonuniform_is_hermite_with_lagrange_slopes():
    rng = random.Random(5)
    for _ in range(500):
        p = [rp(rng, 3) for _ in range(4)]
        ts = [F(0)]
        for _ in range(3):
            ts.append(ts[-1] + F(rng.randint(1, 12), rng.randint(1, 4)))
        h = ts[2] - ts[1]
        s1 = lagrange_slope(p[0:3], ts[0:3])
        s2 = lagrange_slope(p[1:4], ts[1:4])
        assert nonuniform_tangent(p[0:3], ts[0:3]) == s1
        t = ts[1] + h * F(rng.randint(0, 40), 40)
        u = (t - ts[1]) / h
        want = hermite(p[1], tuple(h * x for x in s1), p[2], tuple(h * x for x in s2), u)
        assert barry_goldman(p, ts, t) == want


def test_centripetal_curve_floats():
    rng = random.Random(6)
    for _ in range(200):
        pts = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(rng.randint(4, 8))]
        ts = alpha_knots(pts, 0.5)
        for i in range(1, len(pts) - 1):
            c = catmull_rom_curve(pts, ts, ts[i])
            assert max(abs(x - y) for x, y in zip(c, pts[i])) < 1e-9


def test_worked_example():
    p = [(F(0), F(0)), (F(1), F(1)), (F(2), F(1)), (F(3), F(0))]
    assert uniform_segment(*p, F(1, 2)) == (F(3, 2), F(9, 8))
    assert uniform_tangents(p) == [(F(1), F(1, 2)), (F(1), F(-1, 2))]
