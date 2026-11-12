# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fundamental-forms/. The authors are listed in prov/XRW8YW.jsonl.

import math
import random

import pytest

from fundamental_forms import (area, cos, curve_length, first_form, fundamental_forms,
                               normal_curvature, partials, sin, sqrt)

TOL = 1e-12
R, A = 3.0, 1.0          # torus radii; also the sphere radius R


def sphere(u, v):        # u is the latitude, v the longitude
    return (R * cos(u) * cos(v), R * cos(u) * sin(v), R * sin(u))


def cylinder(u, v):      # radius A
    return (A * cos(u), A * sin(u), v)


def torus(u, v):
    r = R + A * cos(u)
    return (r * cos(v), r * sin(v), A * sin(u))


def saddle(u, v):
    return (u, v, u * v)


def stereo(u, v):        # the sphere of radius R from the stereographic map
    q = 1 + u * u + v * v
    return (R * 2 * u / q, R * 2 * v / q, R * (u * u + v * v - 1) / q)


def close(a, b, tol=TOL):
    return all(abs(x - y) <= tol * max(1.0, abs(y)) for x, y in zip(a, b))


def grid(rng, n=25, lo=-1.3, hi=1.3):
    return [(rng.uniform(lo, hi), rng.uniform(lo, hi)) for _ in range(n)]


def test_sphere():
    for u, v in grid(random.Random(101)):
        c = math.cos(u)
        assert close(fundamental_forms(sphere, u, v), (R * R, 0, R * R * c * c, R, 0, R * c * c))


def test_cylinder():
    for u, v in grid(random.Random(102)):
        assert close(fundamental_forms(cylinder, u, v), (A * A, 0, 1, -A, 0, 0))


def test_torus():
    for u, v in grid(random.Random(103), lo=-3.0, hi=3.0):
        r = R + A * math.cos(u)
        assert close(fundamental_forms(torus, u, v), (A * A, 0, r * r, A, 0, r * math.cos(u)))


def test_saddle():
    for u, v in grid(random.Random(104), lo=-3.0, hi=3.0):
        w = math.sqrt(1 + u * u + v * v)
        assert close(fundamental_forms(saddle, u, v), (1 + v * v, u * v, 1 + u * u, 0, 1 / w, 0))


def test_jet_partials_of_a_polynomial():
    f = lambda u, v: (u ** 3 * v, u + v * v, u * u * v * v)
    for u, v in grid(random.Random(105)):
        su, sv, suu, suv, svv = partials(f, u, v)
        assert close(su, (3 * u * u * v, 1, 2 * u * v * v))
        assert close(sv, (u ** 3, 2 * v, 2 * u * u * v))
        assert close(suu, (6 * u * v, 0, 2 * v * v))
        assert close(suv, (3 * u * u, 0, 4 * u * v))
        assert close(svv, (0, 2, 2 * u * u))


def test_normal_curvature_of_the_sphere_in_two_charts():
    rng = random.Random(106)
    for u, v in grid(rng, 15, -1.2, 1.2):
        d = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        assert abs(normal_curvature(fundamental_forms(sphere, u, v), d) - 1 / R) < 1e-12
        assert abs(abs(normal_curvature(fundamental_forms(stereo, u, v), d)) - 1 / R) < 1e-12


def test_lengths_and_areas():
    meridian = curve_length(sphere, lambda t: (t, 0.4), lambda t: (1.0, 0.0), -math.pi / 2, math.pi / 2)
    assert abs(meridian - math.pi * R) < 1e-9
    u0 = 0.7
    parallel = curve_length(torus, lambda t: (u0, t), lambda t: (0.0, 1.0), 0, 2 * math.pi)
    assert abs(parallel - 2 * math.pi * (R + A * math.cos(u0))) < 1e-9
    assert abs(area(sphere, -math.pi / 2, math.pi / 2, 0, 2 * math.pi) - 4 * math.pi * R * R) < 1e-5
    assert abs(area(torus, 0, 2 * math.pi, 0, 2 * math.pi) - 4 * math.pi ** 2 * R * A) < 1e-8


def test_first_form_gives_angles():
    # meridian and parallel directions are orthogonal on a surface of revolution
    forms = fundamental_forms(torus, 0.3, 1.1)
    assert abs(first_form(forms, (1, 0), (0, 1))) < 1e-12
    # on the saddle the two coordinate lines meet at an angle with cosine uv / sqrt((1+v^2)(1+u^2))
    u, v = 0.8, -0.5
    forms = fundamental_forms(saddle, u, v)
    cosang = first_form(forms, (1, 0), (0, 1)) / math.sqrt(forms[0] * forms[2])
    assert abs(cosang - u * v / math.sqrt((1 + v * v) * (1 + u * u))) < 1e-15


def test_singular_point():
    cone = lambda u, v: (u * cos(v), u * sin(v), u)
    with pytest.raises(ValueError):
        fundamental_forms(cone, 0.0, 0.7)             # the apex, where S_v = 0


def test_sqrt_jet():
    f = lambda u, v: (sqrt(u * u + v * v), 0, 0)
    su, sv, suu, suv, svv = partials(f, 3.0, 4.0)
    assert close((su[0], sv[0], suu[0], suv[0], svv[0]),
                 (0.6, 0.8, 16 / 125, -12 / 125, 9 / 125))
