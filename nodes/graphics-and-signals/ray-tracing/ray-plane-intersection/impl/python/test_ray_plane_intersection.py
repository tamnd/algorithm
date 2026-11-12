# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-plane-intersection/. The authors are listed in prov/NVZ11Z.jsonl.

import random
from fractions import Fraction

from ray_plane_intersection import plane_through, ray_plane, ray_plane_point_normal


def det3(c0, c1, c2):
    return (c0[0] * (c1[1] * c2[2] - c1[2] * c2[1])
            - c1[0] * (c0[1] * c2[2] - c0[2] * c2[1])
            + c2[0] * (c0[1] * c1[2] - c0[2] * c1[1]))


def exact_t(o, d, p0, p1, p2):
    """Reference: solve o + t d = p0 + u (p1 - p0) + v (p2 - p0) by Cramer's rule."""
    o, d, p0, p1, p2 = ([Fraction(x) for x in p] for p in (o, d, p0, p1, p2))
    e1 = [p1[i] - p0[i] for i in range(3)]
    e2 = [p2[i] - p0[i] for i in range(3)]
    md = [-x for x in d]
    rhs = [o[i] - p0[i] for i in range(3)]
    den = det3(e1, e2, md)
    if den == 0:
        return None
    return det3(e1, e2, rhs) / den


def rand_q(rng):
    return Fraction(rng.randint(-30, 30), rng.randint(1, 9))


def test_floor_plane():
    # the plane z = 0 has n = (0, 0, 1) and h = 0
    n = (0, 0, 1)
    assert ray_plane((0.0, 0.0, 3.0), (1.0, 0.0, -2.0), n, 0) == 1.5
    assert ray_plane((0.0, 0.0, 3.0), (1.0, 0.0, 0.0), n, 0) is None          # parallel
    assert ray_plane((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), n, 0) is None          # in the plane
    assert ray_plane((0.0, 0.0, 3.0), (0.0, 0.0, 1.0), n, 0) is None          # behind
    assert ray_plane((0.0, 0.0, -3.0), (0.0, 0.0, 1.0), n, 0) == 3.0          # from the back
    assert ray_plane((0.0, 0.0, -3.0), (0.0, 0.0, 1.0), n, 0, cull_backfaces=True) is None
    assert ray_plane((0.0, 0.0, 3.0), (0.0, 0.0, -1.0), n, 0, tmax=2.0) is None


def test_random_rational_against_cramer():
    rng = random.Random(1980)
    hits = 0
    for _ in range(4000):
        o, d, p0, p1, p2 = (tuple(rand_q(rng) for _ in range(3)) for _ in range(5))
        n, h = plane_through(p0, p1, p2)
        if n == (0, 0, 0) or d == (0, 0, 0):
            continue
        want = exact_t(o, d, p0, p1, p2)
        if want is not None and not want > 0:
            want = None
        assert ray_plane(o, d, n, h) == want
        assert ray_plane_point_normal(o, d, n, p0) == want
        hits += want is not None
    assert hits > 1000


def exact_sub(o, d, n, p0):
    """Reference: exact substitution, t = n . (p0 - o) / (n . d) in Fraction."""
    o, d, n, p0 = ([Fraction(x) for x in p] for p in (o, d, n, p0))
    den = sum(n[i] * d[i] for i in range(3))
    return sum(n[i] * (p0[i] - o[i]) for i in range(3)) / den


def test_float_against_exact():
    rng = random.Random(3)
    for _ in range(3000):
        o, d, p0, n = ([rng.uniform(-10, 10) for _ in range(3)] for _ in range(4))
        cos = abs(sum(n[i] * d[i] for i in range(3))) / (sum(x * x for x in n) * sum(x * x for x in d)) ** 0.5
        if cos < 1e-3:
            continue                          # t is ill conditioned near parallel rays
        want = float(exact_sub(o, d, n, p0))
        got = ray_plane_point_normal(o, d, n, p0, tmin=-1e300)
        assert abs(got - want) <= 1e-12 * (1 + abs(want))
        h = sum(n[i] * p0[i] for i in range(3))
        got = ray_plane(o, d, n, h, tmin=-1e300)
        assert abs(got - want) <= 1e-12 * (1 + abs(want))


def test_point_normal_form_keeps_digits_far_from_the_origin():
    # a plane through p0 near (10^8, 10^8, 10^8), and a ray from just below it
    p0 = (1e8 + 0.2, 1e8 - 0.4, 1e8 + 0.1)
    n = (0.3, 0.7, 1.0)
    o = (1e8 + 0.3, 1e8 + 0.7, 1e8 - 1.0)
    d = (0.0, 0.0, 1.0)
    want = float(exact_sub(o, d, n, p0))
    h = n[0] * p0[0] + n[1] * p0[1] + n[2] * p0[2]
    t_h = ray_plane(o, d, n, h)
    t_pn = ray_plane_point_normal(o, d, n, p0)
    assert abs(t_pn - want) <= 1e-15
    assert abs(t_h - want) > 1e-9
