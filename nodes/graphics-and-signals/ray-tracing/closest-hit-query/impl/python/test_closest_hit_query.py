# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closest-hit-query/. The authors are listed in prov/Q9V10R.jsonl.

import math
import random
from fractions import Fraction

from closest_hit_query import bounding_box, closest_hit_groups, closest_hit_scan

F = Fraction


def det3(c0, c1, c2):
    return (c0[0] * (c1[1] * c2[2] - c1[2] * c2[1])
            - c1[0] * (c0[1] * c2[2] - c0[2] * c2[1])
            + c2[0] * (c0[1] * c1[2] - c0[2] * c1[1]))


def tri_hit(tri, o, d, tmin, tmax):
    """Exact ray-triangle hit by Cramer's rule in Fraction."""
    a, b, c = tri
    e1 = [b[i] - a[i] for i in range(3)]
    e2 = [c[i] - a[i] for i in range(3)]
    md = [-x for x in d]
    r = [o[i] - a[i] for i in range(3)]
    den = det3(e1, e2, md)
    if den == 0:
        return None
    u = det3(r, e2, md) / den
    if u < 0 or u > 1:
        return None
    v = det3(e1, r, md) / den
    if v < 0 or u + v > 1:
        return None
    t = det3(e1, e2, r) / den
    if not (tmin < t < tmax):
        return None
    return t


def brute_force(objects, o, d, tmin, tmax, hit):
    """Reference: every hit of every object, then the minimum."""
    hits = [(hit(obj, o, d, tmin, tmax), k) for k, obj in enumerate(objects)]
    hits = [h for h in hits if h[0] is not None]
    return min(hits) if hits else None


def rand_q(rng, lo, hi):
    return F(rng.randint(lo * 8, hi * 8), 8)


def scene(rng, n, clusters):
    objects, groups = [], []
    for g in range(clusters):
        center = [rand_q(rng, -10, 10) for _ in range(3)]
        idx = []
        for _ in range(n // clusters):
            tri = tuple(tuple(center[i] + rand_q(rng, -2, 2) for i in range(3)) for _ in range(3))
            idx.append(len(objects))
            objects.append(tri)
        lo, hi = bounding_box([p for k in idx for p in objects[k]])
        groups.append((lo, hi, idx))
    return objects, groups


def test_small_example():
    # two parallel squares cut into triangles, at z = 1 and z = 2
    f1 = ((0, 0, 1), (4, 0, 1), (0, 4, 1))
    f2 = ((0, 0, 2), (4, 0, 2), (0, 4, 2))
    o, d = (F(1), F(1), F(5)), (F(0), F(0), F(-1))
    assert closest_hit_scan([f1, f2], o, d, 0, math.inf, tri_hit) == (3, 1)
    # the interval is open: a hit at t = tmin or t = tmax does not count
    assert closest_hit_scan([f1, f2], o, d, F(3), math.inf, tri_hit) == (4, 0)
    assert closest_hit_scan([f1, f2], o, d, 0, F(3), tri_hit) is None


def test_scan_and_groups_against_brute_force():
    rng = random.Random(1968)
    found = 0
    for _ in range(30):
        objects, groups = scene(rng, 16, 4)
        for _ in range(12):
            o = tuple(rand_q(rng, -15, 15) for _ in range(3))
            target = rng.choice(objects)[rng.randrange(3)]
            d = tuple(target[i] + rand_q(rng, -1, 1) - o[i] for i in range(3))
            if d == (0, 0, 0):
                continue
            tmin = F(rng.randint(0, 2), 4)
            tmax = rng.choice([math.inf, F(rng.randint(1, 8), 4)])
            want = brute_force(objects, o, d, tmin, tmax, tri_hit)
            for got in (closest_hit_scan(objects, o, d, tmin, tmax, tri_hit),
                        closest_hit_groups(groups, objects, o, d, tmin, tmax, tri_hit)):
                if want is None:
                    assert got is None
                    continue
                found += 1
                t, k = got
                assert t == want[0]
                assert tri_hit(objects[k], o, d, tmin, tmax) == t
            scan = closest_hit_scan(objects, o, d, tmin, tmax, tri_hit)
            assert scan == want          # the scan keeps the first object on ties
    assert found > 100


def test_groups_test_fewer_objects():
    calls = []

    def counted(tri, o, d, tmin, tmax):
        calls.append(1)
        return tri_hit(tri, o, d, tmin, tmax)

    rng = random.Random(5)
    objects, groups = scene(rng, 40, 8)
    total = 0
    for _ in range(50):
        o = tuple(rand_q(rng, -15, 15) for _ in range(3))
        target = rng.choice(objects)[0]
        d = tuple(target[i] - o[i] for i in range(3))
        calls.clear()
        closest_hit_groups(groups, objects, o, d, 0, math.inf, counted)
        total += len(calls)
    assert total < 50 * len(objects)


def test_float_spheres():
    rng = random.Random(9)

    def sphere_hit(s, o, d, tmin, tmax):
        c, r = s
        f = [o[i] - c[i] for i in range(3)]
        a = sum(x * x for x in d)
        b = sum(f[i] * d[i] for i in range(3))
        k = sum(x * x for x in f) - r * r
        disc = b * b - a * k
        if disc < 0:
            return None
        q = -(b + math.copysign(math.sqrt(disc), b))
        for t in sorted((k / q, q / a)):
            if tmin < t < tmax:
                return t
        return None

    for _ in range(300):
        spheres = [([rng.uniform(-5, 5) for _ in range(3)], rng.uniform(0.2, 1.5)) for _ in range(15)]
        o = [rng.uniform(-8, 8) for _ in range(3)]
        d = [rng.uniform(-1, 1) for _ in range(3)]
        assert closest_hit_scan(spheres, o, d, 0.0, math.inf, sphere_hit) == \
            brute_force(spheres, o, d, 0.0, math.inf, sphere_hit)
