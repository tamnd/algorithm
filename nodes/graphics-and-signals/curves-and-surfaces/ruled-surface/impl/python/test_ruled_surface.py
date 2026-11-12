# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ruled-surface/. The authors are listed in prov/TB1NXX.jsonl.

import random
from fractions import Fraction

import pytest

from ruled_surface import (cross, developability_value, dot, gaussian_curvature,
                           ruled_partials, ruled_point)

C, S = Fraction(3, 5), Fraction(4, 5)      # cos and sin of the twist angle


def circ(t):
    """A rational point of the unit circle."""
    q = 1 + t * t
    return ((1 - t * t) / q, 2 * t / q)


def dcirc(t):
    q = (1 + t * t) ** 2
    return (-4 * t / q, 2 * (1 - t * t) / q)


def rot(p):
    return (C * p[0] - S * p[1], S * p[0] + C * p[1])


def hyp_a(t):
    x, y = circ(t)
    return (x, y, Fraction(-1))


def hyp_b(t):
    x, y = rot(circ(t))
    return (x, y, Fraction(1))


def hyp_da(t):
    return dcirc(t) + (0,)


def hyp_db(t):
    return rot(dcirc(t)) + (0,)


def par(rng):
    return Fraction(rng.randint(-30, 30), 10)


def test_saddle_exact():
    a = lambda u: (u, 0, 0)
    b = lambda u: (u, 1, u)
    da = lambda u: (1, 0, 0)
    db = lambda u: (1, 0, 1)
    rng = random.Random(81)
    for _ in range(50):
        u, v = par(rng), par(rng)
        x, y, z = ruled_point(a, b, u, v)
        assert z == x * y
        assert gaussian_curvature(a, da, b, db, u, v) == -1 / (1 + x * x + y * y) ** 2


def test_hyperboloid_exact():
    rng = random.Random(82)
    a2 = (1 + C) / 2                         # x^2 / a2 + y^2 / a2 - z^2 / c2 = 1
    c2 = (1 + C) / (1 - C)
    assert (a2, c2) == (Fraction(4, 5), 4)
    for _ in range(50):
        u, v = par(rng), Fraction(rng.randint(0, 20), 20)
        x, y, z = ruled_point(hyp_a, hyp_b, u, v)
        assert x * x / a2 + y * y / a2 - z * z / c2 == 1
        k = gaussian_curvature(hyp_a, hyp_da, hyp_b, hyp_db, u, v)
        assert k == -1 / (a2 * a2 * c2 * (x * x / a2 ** 2 + y * y / a2 ** 2 + z * z / c2 ** 2) ** 2)
        assert k < 0
        assert developability_value(hyp_a, hyp_da, hyp_b, hyp_db, u) != 0


def test_cylinder_and_cone_are_developable():
    rng = random.Random(83)
    cyl_a = lambda t: circ(t) + (0,)
    cyl_b = lambda t: circ(t) + (1,)
    dc = lambda t: dcirc(t) + (0,)
    apex = lambda t: (0, 0, 2)
    zero = lambda t: (0, 0, 0)
    for _ in range(30):
        u, v = par(rng), Fraction(rng.randint(1, 19), 20)
        assert developability_value(cyl_a, dc, cyl_b, dc, u) == 0
        assert gaussian_curvature(cyl_a, dc, cyl_b, dc, u, v) == 0
        assert developability_value(apex, zero, cyl_a, dc, u) == 0
        x, y, z = ruled_point(apex, cyl_a, u, v)
        assert x * x + y * y == (z - 2) ** 2 / 4          # the cone of half-angle atan(1/2)


def test_tangent_developable():
    c = lambda u: (u, u * u, u ** 3)
    dc = lambda u: (1, 2 * u, 3 * u * u)
    ddc = lambda u: (0, 2, 6 * u)
    b = lambda u: tuple(x + y for x, y in zip(c(u), dc(u)))
    db = lambda u: tuple(x + y for x, y in zip(dc(u), ddc(u)))
    rng = random.Random(84)
    for _ in range(30):
        u = par(rng)
        assert developability_value(c, dc, b, db, u) == 0


def test_curvature_against_second_form():
    """K from the general form (LN - M^2) / (EG - F^2), with S_vv = 0."""
    a = lambda u: (u, u * u, u ** 3)
    da = lambda u: (1, 2 * u, 3 * u * u)
    dda = lambda u: (0, 2, 6 * u)
    b = lambda u: (u * u, u, 1 + u)
    db = lambda u: (2 * u, 1, 1)
    ddb = lambda u: (2, 0, 0)
    rng = random.Random(85)
    for _ in range(40):
        u, v = par(rng), par(rng)
        su, sv = ruled_partials(a, da, b, db, u, v)
        suu = tuple((1 - v) * x + v * y for x, y in zip(dda(u), ddb(u)))
        suv = tuple(y - x for x, y in zip(da(u), db(u)))
        n = cross(su, sv)
        w2 = dot(n, n)
        if w2 == 0:
            continue
        svv = (0, 0, 0)
        k_ref = (dot(suu, n) * dot(svv, n) - dot(suv, n) ** 2) / (w2 * w2)
        assert gaussian_curvature(a, da, b, db, u, v) == k_ref


def test_end_curves_and_singular_point():
    rng = random.Random(86)
    for _ in range(20):
        u = par(rng)
        assert ruled_point(hyp_a, hyp_b, u, 0) == hyp_a(u)
        assert ruled_point(hyp_a, hyp_b, u, 1) == hyp_b(u)
    apex = lambda t: (0, 0, 2)
    zero = lambda t: (0, 0, 0)
    with pytest.raises(ValueError):
        gaussian_curvature(apex, zero, lambda t: circ(t) + (0,), lambda t: dcirc(t) + (0,), 0, 0)
