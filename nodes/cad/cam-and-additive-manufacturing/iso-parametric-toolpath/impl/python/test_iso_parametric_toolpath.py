# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iso-parametric-toolpath/. The authors are listed in prov/SQ9VDF.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from iso_parametric_toolpath import BilinearPatch, dot, iso_parametric, pass_count, path_segments, sub

TRAPEZOID = BilinearPatch((0, 0, 0), (4, 0, 0), (0, 1, 0), (4, 4, 0))


def dist2(p, a, b):
    """Exact squared distance from p to the segment ab in space."""
    d = sub(b, a)
    dd = dot(d, d)
    t = 0 if dd == 0 else min(F(1), max(F(0), dot(sub(p, a), d) / dd))
    q = tuple(x + t * y - z for x, y, z in zip(a, d, p))
    return dot(q, q)


def random_patch(rng):
    return BilinearPatch(*[tuple(rng.randrange(-10, 11) for _ in range(3)) for _ in range(4)])


def test_trapezoid_example():
    assert pass_count(TRAPEZOID, 1) == 4
    path = iso_parametric(TRAPEZOID, 1)
    assert path[:4] == [(0, 0, 0), (4, 0, 0), (4, 1, 0), (0, F(1, 4), 0)]
    assert len(path) == 10 and path[-2:] == [(0, 1, 0), (4, 4, 0)]
    gap0 = TRAPEZOID.at(0, F(1, 4))[1] - TRAPEZOID.at(0, 0)[1]
    gap1 = TRAPEZOID.at(1, F(1, 4))[1] - TRAPEZOID.at(1, 0)[1]
    assert (gap0, gap1) == (F(1, 4), 1)
    length = sum(math.dist(a, b) for a, b in path_segments(path))
    assert abs(length - 24.43) < 0.01


def test_gap_formula_and_its_maximum():
    rng = random.Random(1)
    for _ in range(40):
        patch = random_patch(rng)
        w = F(rng.randrange(1, 13), 2)
        n = pass_count(patch, w)
        ends = max(dot(patch.s_v(0), patch.s_v(0)), dot(patch.s_v(1), patch.s_v(1)))
        for _ in range(10):
            u = F(rng.randrange(0, 101), 100)
            j = rng.randrange(0, n)
            g = sub(patch.at(u, F(j + 1, n)), patch.at(u, F(j, n)))
            sv = patch.s_v(u)
            assert dot(g, g) * n * n == dot(sv, sv)
            assert dot(sv, sv) <= ends
            assert dot(g, g) <= w * w


def test_pass_count_is_minimal():
    rng = random.Random(2)
    for _ in range(60):
        patch = random_patch(rng)
        w = F(rng.randrange(1, 13), 2)
        n = pass_count(patch, w)
        if n > 1:
            worst = max(dot(g, g) for g in (sub(patch.at(u, F(1, n - 1)), patch.at(u, 0)) for u in (0, 1)))
            assert worst > w * w


def test_every_surface_point_is_near_the_path():
    """Brute force: the exact distance from sample points of the patch to the path is at most w/2."""
    rng = random.Random(3)
    for _ in range(25):
        patch = random_patch(rng)
        w = F(rng.randrange(2, 13), 2)
        segs = path_segments(iso_parametric(patch, w))
        samples = [(F(i, 6), F(j, 6)) for i in range(7) for j in range(7)]
        samples += [(F(rng.randrange(0, 1001), 1000), F(rng.randrange(0, 1001), 1000)) for _ in range(30)]
        for u, v in samples:
            p = patch.at(u, v)
            assert min(dist2(p, a, b) for a, b in segs) <= w * w / 4


def test_path_lies_on_the_patch():
    rng = random.Random(4)
    for _ in range(20):
        patch = random_patch(rng)
        path = iso_parametric(patch, F(rng.randrange(1, 9)))
        n = len(path) // 2 - 1
        for (a, b), j in zip(zip(path[::2], path[1::2]), range(n + 1)):
            v = F(j, n)
            for t in (F(0), F(1, 3), F(1)):
                q = tuple(x + t * (y - x) for x, y in zip(a, b))
                u = t if j % 2 == 0 else 1 - t
                assert q == patch.at(u, v)


def test_bad_input():
    with pytest.raises(ValueError):
        pass_count(TRAPEZOID, 0)
    with pytest.raises(ValueError):
        BilinearPatch((0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0))
