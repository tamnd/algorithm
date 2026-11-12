# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-length-parametrization/. The authors are listed in prov/ZB4VYJ.jsonl.

import math
import random
from fractions import Fraction as F

from arc_length import (
    arc_length,
    gauss,
    legendre_rule,
    length_table,
    param_at_length,
    speed_of,
    uniform_samples,
)


def simpson(f, a, b, n=4000):
    """Reference: composite Simpson rule with n (even) intervals."""
    h = (b - a) / n
    acc = f(a) + f(b)
    for i in range(1, n):
        acc += (4 if i % 2 else 2) * f(a + i * h)
    return acc * h / 3


def cubic_bezier(P):
    def curve(t):
        s = 1 - t
        return tuple(s ** 3 * a + 3 * s * s * t * b + 3 * s * t * t * c + t ** 3 * d for a, b, c, d in zip(*P))

    def deriv(t):
        s = 1 - t
        return tuple(3 * (s * s * (b - a) + 2 * s * t * (c - b) + t * t * (d - c)) for a, b, c, d in zip(*P))

    return curve, deriv


def test_rule_is_exact_to_degree_2n_minus_1():
    for n in range(1, 9):
        xs, ws = legendre_rule(n)
        assert xs == sorted(xs)
        for deg in range(2 * n):
            exact = F(2, deg + 1) if deg % 2 == 0 else F(0)
            got = sum(w * x ** deg for x, w in zip(xs, ws))
            assert abs(got - float(exact)) < 1e-13
        # and not exact one degree higher
        deg = 2 * n
        got = sum(w * x ** deg for x, w in zip(xs, ws))
        assert abs(got - 2 / (deg + 1)) > 1e-6


def test_circle_and_helix_closed_forms():
    for r in (0.5, 1.0, 3.0):
        speed = speed_of(lambda t, r=r: (-r * math.sin(t), r * math.cos(t)))
        for b in (0.3, math.pi, 2 * math.pi):
            assert abs(arc_length(speed, 0.0, b) - r * b) < 1e-11
    a, c = 2.0, 0.5
    speed = speed_of(lambda t: (-a * math.sin(t), a * math.cos(t), c))
    assert abs(arc_length(speed, 0.0, 4 * math.pi) - 4 * math.pi * math.hypot(a, c)) < 1e-10


def test_parabola_closed_form():
    speed = speed_of(lambda t: (1.0, 2 * t))
    for t in (0.1, 0.5, 1.0, 2.5):
        exact = t * math.sqrt(1 + 4 * t * t) / 2 + math.asinh(2 * t) / 4
        assert abs(arc_length(speed, 0.0, t) - exact) < 1e-11


def test_cusp_needs_subdivision():
    # (t^2, t^3) has zero speed at t = 0; the length on [-1, 1] is 2 (13^(3/2) - 8) / 27
    speed = speed_of(lambda t: (2 * t, 3 * t * t))
    exact = 2 * (13 ** 1.5 - 8) / 27
    ts, ss = length_table(speed, -1.0, 1.0, 1e-10)
    assert abs(ss[-1] - exact) < 1e-9
    assert len(ts) > 3
    # a single 5-point rule is visibly worse
    assert abs(gauss(speed, -1.0, 1.0) - exact) > 1e-4


def test_cubic_bezier_against_dense_simpson():
    rng = random.Random(7)
    for _ in range(15):
        P = [(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in range(4)]
        curve, deriv = cubic_bezier(P)
        speed = speed_of(deriv)
        ref = simpson(speed, 0.0, 1.0)
        assert abs(arc_length(speed, 0.0, 1.0, 1e-11) - ref) < 1e-7 * max(1.0, ref)


def test_inverse_on_circle_and_bezier():
    r = 2.0
    speed = speed_of(lambda t: (-r * math.sin(t), r * math.cos(t)))
    ts, ss = length_table(speed, 0.0, 2 * math.pi)
    for s in (0.0, 0.1, 1.0, 5.0, 4 * math.pi - 1e-3):
        assert abs(param_at_length(speed, ts, ss, s) - s / r) < 1e-10
    rng = random.Random(8)
    for _ in range(10):
        P = [(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in range(4)]
        curve, deriv = cubic_bezier(P)
        speed = speed_of(deriv)
        ts, ss = length_table(speed, 0.0, 1.0)
        for _ in range(5):
            t = rng.random()
            s = simpson(speed, 0.0, t, 2000)
            assert abs(param_at_length(speed, ts, ss, s) - t) < 1e-7


def test_uniform_samples_have_equal_lengths():
    P = [(0.0, 0.0), (0.0, 2.0), (1.0, 2.0), (3.0, 0.0)]
    curve, deriv = cubic_bezier(P)
    speed = speed_of(deriv)
    params, pts = uniform_samples(curve, deriv, 0.0, 1.0, 8)
    total = simpson(speed, 0.0, 1.0)
    for k in range(8):
        piece = simpson(speed, params[k], params[k + 1], 400)
        assert abs(piece - total / 8) < 1e-8
    # the unit-speed curve: |dC/ds| = |C'(t)| dt/ds = 1, checked by a central difference in s
    ts, ss = length_table(speed, 0.0, 1.0)
    h = 1e-5
    for s in (0.3, 1.0, 2.0, total - 0.3):
        a = curve(param_at_length(speed, ts, ss, s - h))
        b = curve(param_at_length(speed, ts, ss, s + h))
        assert abs(math.dist(a, b) / (2 * h) - 1) < 1e-6


def test_page_example():
    # the cubic of the page: C(t) = (t, t^3) on [0, 1]
    speed = speed_of(lambda t: (1.0, 3 * t * t))
    L = arc_length(speed, 0.0, 1.0)
    assert abs(L - simpson(speed, 0.0, 1.0, 20000)) < 1e-11
    assert round(L, 6) == 1.547866
    ts, ss = length_table(speed, 0.0, 1.0)
    quarters = [round(param_at_length(speed, ts, ss, L * k / 4), 6) for k in range(5)]
    assert quarters == [0.0, 0.380009, 0.671363, 0.861289, 1.0]
