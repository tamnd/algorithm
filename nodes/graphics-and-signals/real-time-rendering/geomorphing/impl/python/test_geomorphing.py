# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geomorphing/. The authors are listed in prov/N3KQ0C.jsonl.

import random
from fractions import Fraction

from geomorphing import geomorph, surface


def heights(rng, m):
    return {(x, y): rng.randint(-20, 20) for x in range(m + 1) for y in range(m + 1)}


def points(rng, m, k):
    return [(Fraction(rng.randint(0, 64 * m), 64), Fraction(rng.randint(0, 64 * m), 64)) for _ in range(k)]


def test_alpha_zero_is_the_coarse_mesh():
    rng = random.Random(1)
    for m in (2, 4, 8):
        h = heights(rng, m)
        g = geomorph(h, m, Fraction(0))
        coarse = {v: z for v, z in h.items() if v[0] % 2 == 0 and v[1] % 2 == 0}
        for p in points(rng, m, 300):
            assert surface(g, 1, p) == surface(coarse, 2, p)


def test_alpha_one_is_the_fine_mesh():
    rng = random.Random(2)
    for m in (2, 4, 8):
        h = heights(rng, m)
        g = geomorph(h, m, Fraction(1))
        assert g == h
        for p in points(rng, m, 100):
            assert surface(g, 1, p) == surface(h, 1, p)


def test_every_point_moves_linearly_in_alpha():
    rng = random.Random(3)
    m = 8
    h = heights(rng, m)
    g0, g1 = geomorph(h, m, Fraction(0)), geomorph(h, m, Fraction(1))
    for _ in range(20):
        a = Fraction(rng.randint(0, 100), 100)
        ga = geomorph(h, m, a)
        for p in points(rng, m, 50):
            assert surface(ga, 1, p) == (1 - a) * surface(g0, 1, p) + a * surface(g1, 1, p)


def test_coarse_vertices_never_move():
    rng = random.Random(4)
    h = heights(rng, 6)
    for a in (Fraction(0), Fraction(1, 3), Fraction(1)):
        g = geomorph(h, 6, a)
        assert all(g[v] == h[v] for v in h if v[0] % 2 == 0 and v[1] % 2 == 0)
