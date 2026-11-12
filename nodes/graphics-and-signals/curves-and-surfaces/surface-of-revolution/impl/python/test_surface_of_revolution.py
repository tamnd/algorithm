# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-of-revolution/. The authors are listed in prov/R4J4XX.jsonl.

import math
import random
from fractions import Fraction

import pytest

from surface_of_revolution import (area, first_form, gaussian_curvature, mean_curvature,
                                   partials, revolve, revolve_point, second_form)


def rational_angle(w):
    """cos and sin of an angle as rational numbers, from the half-angle tangent w."""
    q = 1 + w * w
    return (1 - w * w) / q, 2 * w / q


def fr(rng, lo=-40, hi=40):
    return Fraction(rng.randint(lo, hi), 10)


def test_sphere_and_torus_exact():
    rng = random.Random(91)
    R, a = Fraction(3), Fraction(1)
    for _ in range(60):
        cu, su = rational_angle(fr(rng))
        cv, sv = rational_angle(fr(rng))
        x, y, z = revolve(cu, su, cv, sv)                 # unit sphere: r = cos u, z = sin u
        assert x * x + y * y + z * z == 1
        r = R + a * cu                                    # torus: r = R + a cos u, z = a sin u
        x, y, z = revolve(r, a * su, cv, sv)
        assert x * x + y * y == r * r and (r - R) ** 2 + z * z == a * a


def test_first_form_and_orthogonality_exact():
    rng = random.Random(92)
    for _ in range(40):
        r, dr, dz = fr(rng, 1, 40), fr(rng), fr(rng)
        c, s = rational_angle(fr(rng))
        su, sv = partials(r, dr, dz, c, s)
        e, f, g = first_form(r, dr, dz)
        assert sum(p * p for p in su) == e
        assert sum(p * q for p, q in zip(su, sv)) == f == 0
        assert sum(q * q for q in sv) == g


def test_gaussian_curvature_closed_forms_exact():
    rng = random.Random(93)
    R, a = Fraction(3), Fraction(1)
    for _ in range(40):
        c, s = rational_angle(fr(rng))
        if c == 0:
            continue                                      # the poles, where r = 0
        # sphere of radius 2: r = 2 cos u, z = 2 sin u, so r' = -2 sin u, z' = 2 cos u
        assert gaussian_curvature(2 * c, -2 * s, -2 * c, 2 * c, -2 * s) == Fraction(1, 4)
        # torus: K = cos u / (a (R + a cos u))
        k = gaussian_curvature(R + a * c, -a * s, -a * c, a * c, -a * s)
        assert k == c / (a * (R + a * c))
        # cylinder r = 2, z = u, and cone r = u, z = 2u: both flat
        assert gaussian_curvature(Fraction(2), 0, 0, 1, 0) == 0
        u = fr(rng, 1, 40)
        assert gaussian_curvature(u, 1, 0, 2, 0) == 0


def test_mean_curvature_and_second_form():
    for u in (0.0, 0.4, 1.0, 2.5, -2.0):
        c, s = math.cos(u), math.sin(u)
        R, a = 3.0, 1.0
        # torus with the normal of second_form, which points into the tube
        h = mean_curvature(R + a * c, -a * s, -a * c, a * c, -a * s)
        assert abs(h - (R + 2 * a * c) / (2 * a * (R + a * c))) < 1e-12
        ell, m, n = second_form(R + a * c, -a * s, -a * c, a * c, -a * s)
        e, f, g = first_form(R + a * c, -a * s, a * c)
        assert abs((ell * n - m * m) / (e * g - f * f) - c / (a * (R + a * c))) < 1e-12
    # unit sphere: the normal points inward, so H = +1
    for u in (-1.2, 0.0, 0.7):
        c, s = math.cos(u), math.sin(u)
        assert abs(mean_curvature(c, -s, -c, c, -s) - 1) < 1e-12


def test_areas_against_closed_forms():
    R, a, h, rc = 3.0, 1.0, 2.0, 1.5
    sphere = area(math.cos, lambda u: -math.sin(u), math.cos, -math.pi / 2, math.pi / 2)
    assert abs(sphere - 4 * math.pi) < 1e-8
    torus = area(lambda u: R + a * math.cos(u), lambda u: -a * math.sin(u),
                 lambda u: a * math.cos(u), 0, 2 * math.pi)
    assert abs(torus - 4 * math.pi ** 2 * R * a) < 1e-8
    cone = area(lambda u: rc * u, lambda u: rc, lambda u: h, 0, 1, n=2)
    assert abs(cone - math.pi * rc * math.hypot(rc, h)) < 1e-12
    cyl = area(lambda u: rc, lambda u: 0.0, lambda u: h, 0, 1, n=2)
    assert abs(cyl - 2 * math.pi * rc * h) < 1e-12


def test_axis_and_stationary_profile_raise():
    with pytest.raises(ValueError):
        gaussian_curvature(0, 1, 0, 0, 0)                 # a point on the axis
    with pytest.raises(ValueError):
        gaussian_curvature(Fraction(1), 0, 1, 0, 1)       # r' = z' = 0


def test_revolve_point_float():
    p = revolve_point(lambda u: 3 + math.cos(u), math.sin, 0.0, math.pi / 2)
    assert abs(p[0]) < 1e-15 and abs(p[1] - 4) < 1e-15 and p[2] == 0
