# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/any-hit-query/. The authors are listed in prov/SSJP31.jsonl.

import math
import random
from fractions import Fraction

from any_hit_query import any_hit, visible

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
    return t if tmin < t < tmax else None


def brute_force(objects, o, d, tmin, tmax, accept=None):
    """Reference: test every object and collect all accepted hits."""
    hits = []
    for k, tri in enumerate(objects):
        t = tri_hit(tri, o, d, tmin, tmax)
        if t is not None and (accept is None or accept(tri, t)):
            hits.append(k)
    return hits


def rand_q(rng, lo, hi):
    return F(rng.randint(lo * 8, hi * 8), 8)


def random_scene(rng, n):
    objs = []
    for _ in range(n):
        c = [rand_q(rng, -6, 6) for _ in range(3)]
        objs.append(tuple(tuple(c[i] + rand_q(rng, -2, 2) for i in range(3)) for _ in range(3)))
    return objs


def test_blocker_between_point_and_light():
    floor = ((-10, -10, 0), (10, -10, 0), (0, 10, 0))
    blocker = ((-1, -1, 2), (1, -1, 2), (0, 1, 2))
    p, light = (F(0), F(0), F(0)), (F(0), F(0), F(4))
    # the point p lies on the floor; eps = 0 and the open interval keep the floor out
    assert not visible([floor, blocker], p, light, tri_hit)
    assert visible([floor], p, light, tri_hit)
    # a blocker behind the light does not count
    far = ((-1, -1, 6), (1, -1, 6), (0, 1, 6))
    assert visible([floor, far], p, light, tri_hit)


def test_against_brute_force():
    rng = random.Random(1968)
    yes = no = 0
    for _ in range(40):
        objs = random_scene(rng, 12)
        for _ in range(10):
            o = tuple(rand_q(rng, -10, 10) for _ in range(3))
            tri = rng.choice(objs)
            aim = [sum(p[i] for p in tri) / 3 for i in range(3)]       # the centroid
            d = tuple(aim[i] - o[i] + rand_q(rng, -1, 1) for i in range(3))
            if d == (0, 0, 0):
                continue
            tmin = F(rng.randint(0, 3), 4)
            tmax = rng.choice([math.inf, F(rng.randint(1, 12), 4)])
            hits = brute_force(objs, o, d, tmin, tmax)
            k = any_hit(objs, o, d, tmin, tmax, tri_hit)
            if hits:
                yes += 1
                assert k == hits[0]          # the scan stops at the first hit in order
            else:
                no += 1
                assert k is None
    assert yes > 50 and no > 50


def test_stops_at_the_first_hit():
    calls = []

    def counted(tri, o, d, tmin, tmax):
        calls.append(tri)
        return tri_hit(tri, o, d, tmin, tmax)

    wall = ((-5, -5, 1), (5, -5, 1), (0, 5, 1))
    others = [((-5, -5, z), (5, -5, z), (0, 5, z)) for z in range(2, 10)]
    o, d = (F(0), F(0), F(0)), (F(0), F(0), F(1))
    assert any_hit([wall] + others, o, d, 0, math.inf, counted) == 0
    assert len(calls) == 1


def test_accept_filter_skips_rejected_hits():
    rng = random.Random(4)
    for _ in range(200):
        objs = random_scene(rng, 10)
        o = tuple(rand_q(rng, -10, 10) for _ in range(3))
        target = rng.choice(objs)[0]
        d = tuple(target[i] - o[i] for i in range(3))
        if d == (0, 0, 0):
            continue
        holes = set(rng.sample(range(10), 5))

        def accept(tri, t):
            return objs.index(tri) not in holes

        hits = brute_force(objs, o, d, 0, math.inf, accept)
        k = any_hit(objs, o, d, 0, math.inf, tri_hit, accept)
        assert (k is None) == (not hits)
        if k is not None:
            assert k not in holes and tri_hit(objs[k], o, d, 0, math.inf) is not None
