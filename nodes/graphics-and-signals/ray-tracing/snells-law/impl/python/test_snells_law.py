# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snells-law/. The authors are listed in prov/DYEFKR.jsonl.

import math
import random

from snells_law import critical_angle, dot, refract, refract_at_surface, refracted_angle


def norm(v):
    s = math.sqrt(dot(v, v))
    return (v[0] / s, v[1] / s, v[2] / s)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def fermat_crossing(a, b, n1, n2):
    """Reference: minimize the travel time n1 |a - p| + n2 |p - b| over p = (x, 0).

    a is above the interface y = 0 and b is below it. The time is a strictly convex function of x,
    so its minimum is the one zero of its increasing derivative, which bisection finds to full
    precision. This uses no part of Snell's law.
    """
    def slope(x):
        return n1 * (x - a[0]) / math.hypot(x - a[0], a[1]) - n2 * (b[0] - x) / math.hypot(b[0] - x, b[1])

    lo, hi = min(a[0], b[0]), max(a[0], b[0])
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if slope(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def test_against_fermat_least_time():
    # 600 random pairs of points on the two sides of the plane y = 0. The incident ray goes from
    # a to the least-time crossing p, and the reference refracted ray goes from p to b.
    rng = random.Random(1)
    for _ in range(600):
        n1 = rng.uniform(1.0, 2.5)
        n2 = rng.uniform(1.0, 2.5)
        a = (rng.uniform(-2, 2), rng.uniform(0.2, 2), 0.0)
        b = (rng.uniform(-2, 2), -rng.uniform(0.2, 2), 0.0)
        x = fermat_crossing(a, b, n1, n2)
        d = norm((x - a[0], -a[1], 0.0))
        want = norm((b[0] - x, b[1], 0.0))
        t = refract(d, (0.0, 1.0, 0.0), n1 / n2)
        assert t is not None
        assert all(abs(t[i] - want[i]) < 1e-7 for i in range(3))


def test_unit_length_coplanar_and_snell_scalar_form():
    rng = random.Random(2)
    for _ in range(1000):
        n = norm((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
        d = norm((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
        if dot(n, d) > 0:
            d = (-d[0], -d[1], -d[2])
        n1, n2 = rng.uniform(1.0, 2.5), rng.uniform(1.0, 2.5)
        t = refract(d, n, n1 / n2)
        sin1 = math.sqrt(max(0.0, 1.0 - dot(n, d) ** 2))
        if t is None:
            assert n1 * sin1 > n2 - 1e-12
            continue
        assert abs(dot(t, t) - 1.0) < 1e-12
        assert abs(dot(t, cross(d, n))) < 1e-12
        assert dot(t, n) <= 0.0
        sin2 = math.sqrt(max(0.0, 1.0 - dot(n, t) ** 2))
        assert abs(n1 * sin1 - n2 * sin2) < 1e-9


def test_total_internal_reflection_matches_critical_angle():
    n1, n2 = 1.5, 1.0
    tc = critical_angle(n1, n2)
    assert abs(math.degrees(tc) - 41.8103148958) < 1e-9
    assert critical_angle(1.0, 1.5) is None
    rng = random.Random(3)
    for _ in range(1000):
        th = rng.uniform(0.0, math.pi / 2)
        if abs(th - tc) < 1e-9:
            continue
        d = (math.sin(th), -math.cos(th), 0.0)
        t = refract(d, (0.0, 1.0, 0.0), n1 / n2)
        assert (t is None) == (th > tc)
        assert (refracted_angle(n1, n2, th) is None) == (th > tc)


def test_vector_form_matches_angle_form():
    rng = random.Random(4)
    for _ in range(1000):
        n1, n2 = rng.uniform(1.0, 2.5), rng.uniform(1.0, 2.5)
        th = rng.uniform(0.0, math.pi / 2)
        t = refract((math.sin(th), -math.cos(th), 0.0), (0.0, 1.0, 0.0), n1 / n2)
        th2 = refracted_angle(n1, n2, th)
        assert (t is None) == (th2 is None)
        if t is not None:
            assert abs(t[0] - math.sin(th2)) < 1e-12
            assert abs(-t[1] - math.cos(th2)) < 1e-12


def test_reversibility():
    # Light runs the same path backward: refracting -t from the far side gives -d.
    rng = random.Random(5)
    for _ in range(1000):
        n = norm((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
        d = norm((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
        if dot(n, d) > 0:
            d = (-d[0], -d[1], -d[2])
        n1, n2 = rng.uniform(1.0, 2.5), rng.uniform(1.0, 2.5)
        t = refract(d, n, n1 / n2)
        if t is None:
            continue
        back = refract((-t[0], -t[1], -t[2]), (-n[0], -n[1], -n[2]), n2 / n1)
        assert back is not None
        assert all(abs(back[i] + d[i]) < 1e-9 for i in range(3))


def test_whitted_1980_formula_agrees():
    # Whitted's form: V' = V / |V . N|, kf = (kn^2 |V'|^2 - |V' + N|^2)^(-1/2), P = kf (N + V') - N,
    # with kn = n2 / n1. P is not unit length; its direction must equal refract.
    rng = random.Random(6)
    for _ in range(1000):
        n = norm((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
        v = norm((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
        if dot(n, v) > -1e-3:
            continue
        n1, n2 = rng.uniform(1.0, 2.5), rng.uniform(1.0, 2.5)
        vn = abs(dot(v, n))
        vp = (v[0] / vn, v[1] / vn, v[2] / vn)
        s = (vp[0] + n[0], vp[1] + n[1], vp[2] + n[2])
        q = (n2 / n1) ** 2 * dot(vp, vp) - dot(s, s)
        t = refract(v, n, n1 / n2)
        if q <= 0:
            assert t is None or abs(q) < 1e-9
            continue
        kf = q ** -0.5
        p = norm((kf * s[0] - n[0], kf * s[1] - n[1], kf * s[2] - n[2]))
        assert t is not None
        assert all(abs(p[i] - t[i]) < 1e-9 for i in range(3))


def test_worked_example_and_both_sides():
    s = math.sqrt(0.5)
    t = refract((s, -s, 0.0), (0.0, 1.0, 0.0), 1.0 / 1.5)
    assert abs(t[0] - 0.4714045207910316) < 1e-12
    assert abs(t[1] + 0.881917103688197) < 1e-12
    assert abs(math.degrees(math.asin(t[0])) - 28.1255057020557) < 1e-9
    # normal incidence goes straight through
    assert refract((0.0, -1.0, 0.0), (0.0, 1.0, 0.0), 1.0 / 1.5) == (0.0, -1.0, 0.0)
    # a ray leaving a glass ball of index 1.5 at 60 degrees from the normal is reflected
    out = (math.sin(math.radians(60)), math.cos(math.radians(60)), 0.0)
    assert refract_at_surface(out, (0.0, 1.0, 0.0), 1.0, 1.5) is None
    inn = (math.sin(math.radians(60)), -math.cos(math.radians(60)), 0.0)
    assert refract_at_surface(inn, (0.0, 1.0, 0.0), 1.0, 1.5) is not None
