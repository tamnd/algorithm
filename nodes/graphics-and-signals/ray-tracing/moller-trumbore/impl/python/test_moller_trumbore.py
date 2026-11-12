# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moller-trumbore/. The authors are listed in prov/H67QFK.jsonl.

import random
from fractions import Fraction

from moller_trumbore import moller_trumbore


def det3(c0, c1, c2):
    """Determinant of the 3 by 3 matrix with the columns c0, c1, c2."""
    return (c0[0] * (c1[1] * c2[2] - c1[2] * c2[1])
            - c1[0] * (c0[1] * c2[2] - c0[2] * c2[1])
            + c2[0] * (c0[1] * c1[2] - c0[2] * c1[1]))


def exact_hit(o, d, a, b, c, tmin=0, tmax=None):
    """Reference: solve u (b - a) + v (c - a) - t d = o - a by Cramer's rule in Fraction."""
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
    if u < 0 or v < 0 or u + v > 1 or t <= tmin or (tmax is not None and t >= tmax):
        return None
    return (t, u, v)


def rand_q(rng):
    return Fraction(rng.randint(-20, 20), rng.randint(1, 8))


def rand_pt(rng):
    return tuple(rand_q(rng) for _ in range(3))


def test_simple_hit():
    hit = moller_trumbore((Fraction(1, 4), Fraction(1, 4), Fraction(1)), (0, 0, -1),
                          (0, 0, 0), (1, 0, 0), (0, 1, 0))
    assert hit == (1, Fraction(1, 4), Fraction(1, 4))


def test_parallel_and_interval():
    tri = ((0, 0, 0), (1, 0, 0), (0, 1, 0))
    assert moller_trumbore((0, 0, 1), (1, 0, 0), *tri) is None
    assert moller_trumbore((0.2, 0.2, 1.0), (0.0, 0.0, -1.0), *tri, tmax=0.5) is None
    assert moller_trumbore((0.2, 0.2, -1.0), (0.0, 0.0, -1.0), *tri) is None


def test_backface_culling():
    tri = ((0, 0, 0), (1, 0, 0), (0, 1, 0))
    # seen from above, the vertices run counterclockwise: det > 0, a front face
    o, down, up = (0.2, 0.2, 1.0), (0.0, 0.0, -1.0), (0.0, 0.0, 1.0)
    assert moller_trumbore(o, down, *tri, cull_backfaces=True) is not None
    below = (0.2, 0.2, -1.0)
    assert moller_trumbore(below, up, *tri, cull_backfaces=True) is None
    assert moller_trumbore(below, up, *tri) is not None


def test_random_rational_against_cramer():
    rng = random.Random(1997)
    hits = 0
    for _ in range(3000):
        o, a, b, c = rand_pt(rng), rand_pt(rng), rand_pt(rng), rand_pt(rng)
        if rng.random() < 0.7:
            # aim at a random point of the plane near the triangle
            w = [Fraction(rng.randint(-2, 10), 8) for _ in range(2)]
            p = [a[i] + w[0] * (b[i] - a[i]) + w[1] * (c[i] - a[i]) for i in range(3)]
            d = tuple(p[i] - o[i] for i in range(3))
        else:
            d = rand_pt(rng)
        if d == (0, 0, 0):
            continue
        got = moller_trumbore(o, d, a, b, c)
        want = exact_hit(o, d, a, b, c)
        assert got == want
        hits += got is not None
    assert hits > 500


def test_float_against_exact():
    rng = random.Random(21)
    for _ in range(3000):
        pts = [tuple(rng.uniform(-5, 5) for _ in range(3)) for _ in range(5)]
        o, d, a, b, c = pts
        want = exact_hit(o, d, a, b, c)
        got = moller_trumbore(o, d, a, b, c)
        if want is None:
            # a float hit is possible only next to the boundary
            if got is not None:
                t, u, v = got
                assert min(u, v, 1 - u - v) < 1e-9
            continue
        t, u, v = (float(x) for x in want)
        if min(u, v, 1 - u - v) < 1e-9:
            continue
        assert got is not None
        assert abs(got[0] - t) <= 1e-9 * max(1.0, abs(t))
        assert abs(got[1] - u) <= 1e-9 and abs(got[2] - v) <= 1e-9


def test_shared_edge_leak():
    # The example of the page: a ray through a shared edge misses both triangles.
    p, q = (0.1, 0.2, 0.3), (0.7, 0.9, 0.4)
    a, b = (0.9, 0.1, 0.2), (0.2, 0.8, 0.6)
    o = (1.0, 1.0, 2.0)
    target = tuple(p[i] + 0.1 * (q[i] - p[i]) for i in range(3))
    d = tuple(target[i] - o[i] for i in range(3))
    assert moller_trumbore(o, d, p, a, q) is None
    assert moller_trumbore(o, d, p, q, b) is None
    # exact arithmetic on the same float inputs finds the hit in the first triangle
    assert exact_hit(o, d, p, a, q) is not None
