# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plucker-ray-triangle-test/. The authors are listed in prov/C4PQD6.jsonl.

import math
import random
from fractions import Fraction

from plucker_ray_triangle_test import plucker_intersect, plucker_line, ray_line, side


def det3(c0, c1, c2):
    return (c0[0] * (c1[1] * c2[2] - c1[2] * c2[1])
            - c1[0] * (c0[1] * c2[2] - c0[2] * c2[1])
            + c2[0] * (c0[1] * c1[2] - c0[2] * c1[1]))


def exact_hit(o, d, a, b, c):
    """Reference: Cramer's rule in Fraction for o + t d = a + u (b - a) + v (c - a)."""
    o, d, a, b, c = ([Fraction(x) for x in p] for p in (o, d, a, b, c))
    e1 = [b[i] - a[i] for i in range(3)]
    e2 = [c[i] - a[i] for i in range(3)]
    md = [-x for x in d]
    r = [o[i] - a[i] for i in range(3)]
    den = det3(e1, e2, md)
    if den == 0:
        return None
    u = det3(r, e2, md) / den
    v = det3(e1, r, md) / den
    t = det3(e1, e2, r) / den
    if u < 0 or v < 0 or u + v > 1 or t <= 0:
        return None
    return (t, 1 - u - v, u, v)


def rand_q(rng):
    return Fraction(rng.randint(-20, 20), rng.randint(1, 8))


def test_side_is_a_triple_product():
    rng = random.Random(3)
    for _ in range(200):
        o, d, p, q = ([rand_q(rng) for _ in range(3)] for _ in range(4))
        s = side(ray_line(o, d), plucker_line(p, q))
        pa = [p[i] - o[i] for i in range(3)]
        qa = [q[i] - o[i] for i in range(3)]
        assert s == det3(d, pa, qa)


def test_simple_hit():
    f = Fraction
    hit = plucker_intersect((f(1, 4), f(1, 4), f(1)), (f(0), f(0), f(-1)),
                            (0, 0, 0), (1, 0, 0), (0, 1, 0))
    assert hit == (1, f(1, 2), f(1, 4), f(1, 4))


def test_random_rational_against_cramer():
    rng = random.Random(1995)
    hits = 0
    for _ in range(3000):
        o, a, b, c = (tuple(rand_q(rng) for _ in range(3)) for _ in range(4))
        w = [Fraction(rng.randint(-2, 10), 8) for _ in range(2)]
        p = [a[i] + w[0] * (b[i] - a[i]) + w[1] * (c[i] - a[i]) for i in range(3)]
        d = tuple(p[i] - o[i] for i in range(3))
        if rng.random() < 0.3:
            d = tuple(rand_q(rng) for _ in range(3))
        if d == (0, 0, 0):
            continue
        got = plucker_intersect(o, d, a, b, c)
        want = exact_hit(o, d, a, b, c)
        assert got == want
        hits += got is not None
    assert hits > 500


def test_float_against_exact():
    rng = random.Random(4)
    for _ in range(3000):
        o, d, a, b, c = ([rng.uniform(-5, 5) for _ in range(3)] for _ in range(5))
        got = plucker_intersect(o, d, a, b, c)
        want = exact_hit(o, d, a, b, c)
        if want is None or min(want[1:]) < 1e-9:
            if want is None and got is not None:
                assert min(got[1:]) < 1e-9
            continue
        assert got is not None
        assert abs(got[0] - float(want[0])) <= 1e-9 * max(1.0, float(want[0]))
        for x, y in zip(got[1:], want[1:]):
            assert abs(x - float(y)) <= 1e-9


def test_shared_edges_do_not_leak():
    # A fan of triangles around a center vertex. Each edge is computed once,
    # and its reverse is the exact negation, so the two triangles of an edge
    # see opposite signs and a ray through the edge hits one of them.
    rng = random.Random(1997)
    for _ in range(2000):
        n = 6
        c = (0.0, 0.0, rng.uniform(-0.3, 0.3))
        ring = []
        for k in range(n):
            ang = 2 * math.pi * k / n + rng.uniform(-0.2, 0.2)
            rad = rng.uniform(0.5, 1.5)
            ring.append((rad * math.cos(ang), rad * math.sin(ang), rng.uniform(-0.3, 0.3)))
        spokes = [plucker_line(c, r) for r in ring]
        rims = [plucker_line(ring[k], ring[(k + 1) % n]) for k in range(n)]

        def neg(line):
            return (tuple(-x for x in line[0]), tuple(-x for x in line[1]))

        o = (rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(5, 10))
        k = rng.randrange(n)
        s = rng.uniform(0.05, 0.95)
        tgt = tuple(c[i] + s * (ring[k][i] - c[i]) for i in range(3))
        d = tuple(tgt[i] - o[i] for i in range(3))
        hit = False
        for j in (k - 1, k):
            j %= n
            tri = (c, ring[j], ring[(j + 1) % n])
            edges = (spokes[j], rims[j], neg(spokes[(j + 1) % n]))
            hit = hit or plucker_intersect(o, d, *tri, edges=edges) is not None
        assert hit
