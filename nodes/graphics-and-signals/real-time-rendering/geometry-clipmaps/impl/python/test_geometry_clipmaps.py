# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometry-clipmaps/. The authors are listed in prov/03429S.jsonl.

import random
from fractions import Fraction

from geometry_clipmaps import Level, mesh, origin, points

N, LEVELS = 15, 4
W = Fraction(N, 10)


def make_height(rng):
    a, b, c = rng.randrange(1, 97), rng.randrange(1, 97), rng.randrange(1, 97)
    return lambda p: (a * p[0] + b * p[1] + c * p[0] * p[1]) % 97


def viewers(rng, k):
    return [(Fraction(rng.randint(-4000, 4000), 16), Fraction(rng.randint(-4000, 4000), 16)) for _ in range(k)]


def test_every_edge_is_shared_by_two_triangles():
    rng = random.Random(1)
    for v in viewers(rng, 10):
        tris, degenerate, _, wins = mesh(v, N, LEVELS, make_height(rng), W)
        x0, y0, x1, y1 = wins[-1]
        directed = {}
        for t in tris + degenerate:
            for k in range(3):
                e = (t[k][1], t[(k + 1) % 3][1])
                directed[e] = directed.get(e, 0) + 1
        assert max(directed.values()) == 1
        for (p, q) in directed:
            if (q, p) not in directed:
                assert (p[0] == q[0] and p[0] in (x0, x1)) or (p[1] == q[1] and p[1] in (y0, y1))


def test_triangles_cover_the_coarsest_window_once():
    rng = random.Random(2)
    for v in viewers(rng, 10):
        tris, _, _, wins = mesh(v, N, LEVELS, make_height(rng), W)
        area2 = 0
        for (_, a), (_, b), (_, c) in tris:
            d = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
            assert d > 0
            area2 += d
        x0, y0, x1, y1 = wins[-1]
        assert area2 == 2 * (x1 - x0) * (y1 - y0)


def test_no_gaps_when_the_border_is_fully_morphed():
    rng = random.Random(3)
    for v in viewers(rng, 10):
        tris, degenerate, z, _ = mesh(v, N, LEVELS, make_height(rng), W)
        for (la, a), (lb, b), (lo, o) in degenerate:
            assert z[(lo, o)] == (z[(la, a)] + z[(lb, b)]) / 2
        seen = {}
        for t in tris + degenerate:
            for key in t:
                p = key[1]
                if p in seen:
                    assert seen[p] == z[key]
                else:
                    seen[p] = z[key]


def test_toroidal_update_equals_a_fresh_fill():
    rng = random.Random(4)
    height = make_height(rng)
    v = (Fraction(0), Fraction(0))
    levels = [Level(N, l, height, origin(v, N, l)) for l in range(LEVELS)]
    for _ in range(40):
        v = (v[0] + Fraction(rng.randint(-40, 40), 8), v[1] + Fraction(rng.randint(-40, 40), 8))
        for lev in levels:
            o = origin(v, N, lev.l)
            new = set(points(o, N, lev.l)) - set(points(lev.o, N, lev.l))
            assert lev.move(o) == len(new)
            fresh = Level(N, lev.l, height, o)
            for p in points(o, N, lev.l):
                assert lev.get(p) == height(p) == fresh.get(p)


def test_the_smallest_window_step_writes_two_columns():
    height = make_height(random.Random(5))
    lev = Level(N, 1, height, origin((0, 0), N, 1))
    o = (lev.o[0] + 4, lev.o[1])
    assert lev.move(o) == 2 * N
