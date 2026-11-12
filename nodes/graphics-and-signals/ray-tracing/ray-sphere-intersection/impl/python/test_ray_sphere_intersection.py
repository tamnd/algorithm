# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-sphere-intersection/. The authors are listed in prov/F1JA6J.jsonl.

import math
import random
from decimal import Decimal, getcontext
from fractions import Fraction

from ray_sphere_intersection import naive_roots, ray_sphere, sphere_roots

getcontext().prec = 60


def exact_roots(o, d, c, r):
    """Reference: the exact discriminant in Fraction, and roots to 60 digits."""
    o, d, c, r = [Fraction(x) for x in o], [Fraction(x) for x in d], [Fraction(x) for x in c], Fraction(r)
    f = [o[i] - c[i] for i in range(3)]
    a = sum(x * x for x in d)
    b = sum(f[i] * d[i] for i in range(3))
    k = sum(x * x for x in f) - r * r
    disc = b * b - a * k
    if disc < 0:
        return disc, None

    def dec(x):
        return Decimal(x.numerator) / Decimal(x.denominator)

    sq = dec(disc).sqrt()
    return disc, ((-dec(b) - sq) / dec(a), (-dec(b) + sq) / dec(a))


def test_unit_sphere():
    assert sphere_roots((0.0, 0.0, -5.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1.0) == (4.0, 6.0)
    assert ray_sphere((0.0, 0.0, -5.0), (0.0, 0.0, 2.0), (0.0, 0.0, 0.0), 1.0) == 2.0
    # from inside, the first root is behind the origin
    assert ray_sphere((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1.0) == 1.0
    # behind the ray and beyond tmax
    assert ray_sphere((0.0, 0.0, 5.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1.0) is None
    assert ray_sphere((0.0, 0.0, -5.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1.0, tmax=3.0) is None
    # tangent and miss
    assert sphere_roots((1.0, 0.0, -5.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1.0) == (5.0, 5.0)
    assert sphere_roots((1.5, 0.0, -5.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1.0) is None


def test_random_against_exact():
    rng = random.Random(1968)
    hits = 0
    for _ in range(3000):
        o = [rng.randint(-400, 400) / 16 for _ in range(3)]
        c = [rng.randint(-400, 400) / 16 for _ in range(3)]
        r = rng.randint(1, 200) / 16
        aim = [c[i] + rng.uniform(-1.5, 1.5) * r for i in range(3)]
        d = [aim[i] - o[i] for i in range(3)]
        disc, ex = exact_roots(o, d, c, r)
        got = sphere_roots(o, d, c, r)
        a = sum(x * x for x in d)
        if abs(disc) <= 1e-9 * a * r * r:
            continue
        assert (got is None) == (ex is None)
        if ex is None:
            continue
        hits += 1
        f = math.dist(o, c)
        scale = f / math.sqrt(a)
        for t, e in zip(got, ex):
            assert abs(Decimal(t) - e) <= Decimal(1e-13) * (abs(e) + Decimal(scale))
    assert hits > 1000


def rel(x, e):
    return abs((Decimal(x) - e) / e)


def test_near_root_where_the_naive_formula_cancels():
    # A sphere of radius 10^6; the ray starts 1 unit outside it.
    case = ((0.0, 0.5, -1000001.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1e6)
    _, ex = exact_roots(*case)
    stable, naive = sphere_roots(*case), naive_roots(*case)
    assert rel(stable[0], ex[0]) < 1e-15
    assert rel(naive[0], ex[0]) > 1e-12
    assert rel(stable[1], ex[1]) < 1e-15


def test_discriminant_of_a_far_sphere():
    # A unit sphere seen from 10^8 away: b^2 - a k rounds to 0.
    case = ((0.0, 0.5, -1e8), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1.0)
    _, ex = exact_roots(*case)
    stable, naive = sphere_roots(*case), naive_roots(*case)
    assert naive == (1e8, 1e8)
    assert all(rel(t, e) < 1e-15 for t, e in zip(stable, ex))
    # a ray that misses: the naive formula reports a touch, the stable one a miss
    miss = ((0.0, 1.1, -1e8), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1.0)
    assert exact_roots(*miss)[1] is None
    assert naive_roots(*miss) is not None
    assert sphere_roots(*miss) is None


def test_random_far_spheres():
    rng = random.Random(7)
    for _ in range(500):
        dist = 10.0 ** rng.uniform(5, 9)
        o = (rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.9), -dist)
        if o[0] ** 2 + o[1] ** 2 > 0.81:
            continue
        case = (o, (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 1.0)
        _, ex = exact_roots(*case)
        got = sphere_roots(*case)
        assert got is not None
        for t, e in zip(got, ex):
            assert abs(Decimal(t) - e) <= Decimal(4e-16) * abs(e)
