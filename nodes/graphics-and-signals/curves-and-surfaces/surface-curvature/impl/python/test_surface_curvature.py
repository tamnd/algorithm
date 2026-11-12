# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-curvature/. The authors are listed in prov/N0S7K8.jsonl.

import math
import random

import pytest

from surface_curvature import (forms_from_partials, gaussian_curvature, mean_curvature,
                               normal_curvature, principal_curvatures, principal_directions,
                               total_curvature)

R, A = 3.0, 1.0


def sphere(u, v):          # radius R, u the latitude
    cu, su, cv, sv = math.cos(u), math.sin(u), math.cos(v), math.sin(v)
    return ((-R * su * cv, -R * su * sv, R * cu), (-R * cu * sv, R * cu * cv, 0.0),
            (-R * cu * cv, -R * cu * sv, -R * su), (R * su * sv, -R * su * cv, 0.0),
            (-R * cu * cv, -R * cu * sv, 0.0))


def cylinder(u, v):        # (A cos u, A sin u, v)
    cu, su = math.cos(u), math.sin(u)
    return ((-A * su, A * cu, 0.0), (0.0, 0.0, 1.0), (-A * cu, -A * su, 0.0),
            (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))


def torus(u, v):           # ((R + A cos u) cos v, (R + A cos u) sin v, A sin u)
    cu, su, cv, sv = math.cos(u), math.sin(u), math.cos(v), math.sin(v)
    r = R + A * cu
    return ((-A * su * cv, -A * su * sv, A * cu), (-r * sv, r * cv, 0.0),
            (-A * cu * cv, -A * cu * sv, -A * su), (A * su * sv, -A * su * cv, 0.0),
            (-r * cv, -r * sv, 0.0))


def saddle(u, v):          # (u, v, uv)
    return ((1.0, 0.0, v), (0.0, 1.0, u), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0))


def pts(seed, lo, hi, n=30):
    rng = random.Random(seed)
    return [(rng.uniform(lo, hi), rng.uniform(lo, hi)) for _ in range(n)]


def near(a, b, tol=1e-12):
    return abs(a - b) <= tol * max(1.0, abs(b))


def test_sphere():
    for u, v in pts(201, -1.4, 1.4):
        f = forms_from_partials(*sphere(u, v))
        assert near(gaussian_curvature(f), 1 / R ** 2)
        assert near(mean_curvature(f), 1 / R)          # the normal points inward
        k1, k2 = principal_curvatures(f)
        assert near(k1, 1 / R, 1e-7) and near(k2, 1 / R, 1e-7)


def test_cylinder():
    for u, v in pts(202, -3.0, 3.0):
        f = forms_from_partials(*cylinder(u, v))
        assert gaussian_curvature(f) == 0
        assert near(mean_curvature(f), -1 / (2 * A))   # the normal points outward
        assert principal_curvatures(f) == pytest.approx((0.0, -1 / A), abs=1e-12)


def test_torus():
    for u, v in pts(203, -3.1, 3.1):
        f = forms_from_partials(*torus(u, v))
        r = R + A * math.cos(u)
        assert near(gaussian_curvature(f), math.cos(u) / (A * r))
        assert near(mean_curvature(f), (R + 2 * A * math.cos(u)) / (2 * A * r))
        k1, k2 = principal_curvatures(f)
        assert near(k1, 1 / A) and near(k2, math.cos(u) / r)


def test_saddle():
    for u, v in pts(204, -3.0, 3.0):
        f = forms_from_partials(*saddle(u, v))
        w = math.sqrt(1 + u * u + v * v)
        assert near(gaussian_curvature(f), -1 / w ** 4)
        assert near(mean_curvature(f), -u * v / w ** 3)
    f = forms_from_partials(*saddle(0.0, 0.0))
    (d1, k1), (d2, k2) = principal_directions(f)
    assert (k1, k2) == (1.0, -1.0)
    assert d1[0] == d1[1] and d2[0] == -d2[1]           # the diagonals (1, 1) and (1, -1)


def test_principal_directions_and_euler_formula():
    rng = random.Random(205)
    surfaces = (torus, saddle, cylinder)
    for _ in range(60):
        s = rng.choice(surfaces)
        u, v = rng.uniform(-2, 2), rng.uniform(-2, 2)
        f = forms_from_partials(*s(u, v))
        e, ff, g = f[:3]
        (d1, k1), (d2, k2) = principal_directions(f)
        assert near(normal_curvature(f, d1), k1, 1e-9) and near(normal_curvature(f, d2), k2, 1e-9)
        # d1 and d2 are orthogonal on the surface
        i12 = e * d1[0] * d2[0] + ff * (d1[0] * d2[1] + d1[1] * d2[0]) + g * d1[1] * d2[1]
        assert abs(i12) <= 1e-9 * math.sqrt(normal_len2(f, d1) * normal_len2(f, d2))
        # Euler: the direction at angle t from d1 has normal curvature k1 cos^2 t + k2 sin^2 t
        t = rng.uniform(0, math.pi)
        a1, a2 = math.sqrt(normal_len2(f, d1)), math.sqrt(normal_len2(f, d2))
        d = (math.cos(t) * d1[0] / a1 + math.sin(t) * d2[0] / a2,
             math.cos(t) * d1[1] / a1 + math.sin(t) * d2[1] / a2)
        assert near(normal_curvature(f, d), k1 * math.cos(t) ** 2 + k2 * math.sin(t) ** 2, 1e-9)
        # K and H are the product and the mean of the extreme normal curvatures
        assert near(k1 * k2, gaussian_curvature(f), 1e-9)
        assert near((k1 + k2) / 2, mean_curvature(f), 1e-12)


def normal_len2(f, d):
    e, ff, g = f[:3]
    return e * d[0] * d[0] + 2 * ff * d[0] * d[1] + g * d[1] * d[1]


def test_umbilic_directions():
    f = forms_from_partials(*sphere(0.4, 1.0))
    (d1, k1), (d2, k2) = principal_directions(f)
    assert d1 == (1.0, 0.0) and near(k1, 1 / R, 1e-7)


def test_gauss_bonnet():
    assert abs(total_curvature(sphere, -math.pi / 2, math.pi / 2, 0, 2 * math.pi) - 4 * math.pi) < 1e-6
    assert abs(total_curvature(torus, 0, 2 * math.pi, 0, 2 * math.pi)) < 1e-9
    outer = total_curvature(torus, -math.pi / 2, math.pi / 2, 0, 2 * math.pi)
    assert abs(outer - 4 * math.pi) < 1e-6       # the outer half carries +4 pi, the inner half -4 pi


def test_singular_point():
    with pytest.raises(ValueError):
        forms_from_partials((1.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
