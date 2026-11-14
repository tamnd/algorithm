# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iso-planar-toolpath/. The authors are listed in prov/4X99MA.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from iso_planar_toolpath import BilinearPatch, dist2_segment, dot, iso_planar, sub


def ramp(m):
    """The plane z = m x over 0 <= x <= 10, 0 <= y <= 4, with x = 10 v."""
    return BilinearPatch((0, 0, 0), (0, 4, 0), (10, 0, 10 * m), (10, 4, 10 * m))


def random_patch(rng):
    j = lambda: F(rng.randrange(-8, 9), 4)
    x10 = j()
    p00 = (0, 0, F(rng.randrange(-20, 21), 4))
    p10 = (x10, 10 + j(), F(rng.randrange(-20, 21), 4))
    p01 = (10 + j(), j(), F(rng.randrange(-20, 21), 4))
    p11 = (x10 + 10 + j(), 10 + j(), F(rng.randrange(-20, 21), 4))
    return BilinearPatch(p00, p10, p01, p11)


def normal_x(patch, u, v):
    p00, p10, p01, p11 = patch.p00, patch.p10, patch.p01, patch.p11
    su = [float((1 - v) * (b - a) + v * (d - c)) for a, b, c, d in zip(p00, p10, p01, p11)]
    sv = [float((1 - u) * (c - a) + u * (d - b)) for a, b, c, d in zip(p00, p10, p01, p11)]
    n = (su[1] * sv[2] - su[2] * sv[1], su[2] * sv[0] - su[0] * sv[2], su[0] * sv[1] - su[1] * sv[0])
    return n[0] / math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)


def fdist(p, pts):
    best = math.inf
    for a, b in zip(pts, pts[1:]):
        a, b = [float(x) for x in a], [float(x) for x in b]
        d = [y - x for x, y in zip(a, b)]
        dd = sum(x * x for x in d)
        t = 0.0 if dd == 0 else min(1.0, max(0.0, sum((float(pi) - ai) * di for pi, ai, di in zip(p, a, d)) / dd))
        best = min(best, math.dist([ai + t * di for ai, di in zip(a, d)], [float(x) for x in p]))
    return best


def test_ramp_example():
    passes = iso_planar(ramp(F(3, 4)), 1, F(1, 100))
    assert [c for c, _ in passes] == [F(2 * k + 1, 2) for k in range(10)]
    assert passes[0][1] == [(0, (F(1, 2), 0, F(3, 8))), (1, (F(1, 2), 4, F(3, 8)))]
    assert passes[1][1][0][1] == (F(3, 2), 4, F(9, 8))
    for (_, a), (_, b) in zip(passes, passes[1:]):
        d = sub(a[0][1], b[-1][1])
        assert dot(d, d) == F(25, 16)  # the spacing on the surface is 5/4 for g = 1


def test_points_are_on_the_plane_and_on_the_patch():
    rng = random.Random(1)
    for _ in range(25):
        patch = random_patch(rng)
        for c, pts in iso_planar(patch, F(rng.randrange(1, 9), 4), F(1, 50)):
            for u, p in pts:
                v = patch.v_on_plane(c, u)
                assert p[0] == c and 0 <= u <= 1 and 0 <= v <= 1
                assert p == patch.at(u, v)


def test_every_chord_passes_the_midpoint_test():
    rng = random.Random(2)
    for _ in range(25):
        patch = random_patch(rng)
        eps = F(1, rng.randrange(10, 200))
        for c, pts in iso_planar(patch, F(rng.randrange(1, 9), 4), eps):
            for (u0, a), (u1, b) in zip(pts, pts[1:]):
                um = (u0 + u1) / 2
                assert dist2_segment(patch.at(um, patch.v_on_plane(c, um)), a, b) <= eps * eps


def test_spacing_on_the_surface_matches_the_slope_estimate():
    """Measured, not proved: the gap on the surface is about g / sqrt(1 - n_x^2)."""
    rng = random.Random(3)
    g = F(1, 4)
    checked = 0
    for _ in range(6):
        patch = random_patch(rng)
        passes = iso_planar(patch, g, F(1, 1000))
        for (c, a), (_, b) in zip(passes[2:-3], passes[3:-2]):
            u, p = a[len(a) // 2]
            if not (F(1, 5) < u < F(4, 5)):
                continue
            v = patch.v_on_plane(c, u)
            est = float(g) / math.sqrt(1 - normal_x(patch, u, v) ** 2)
            got = fdist(p, [q for _, q in b])
            assert abs(got - est) <= 0.1 * est
            checked += 1
    assert checked > 50


def test_coverage_measured():
    """Measured, not proved: an inner sample point is within about half the local gap of a pass.

    Near a patch boundary that runs almost parallel to the planes, the passes
    end at a grazing angle and the distance can be larger, so the samples
    stay away from the boundary.
    """
    rng = random.Random(4)
    for _ in range(4):
        patch = random_patch(rng)
        g, eps = F(1, 2), F(1, 200)
        passes = iso_planar(patch, g, eps)
        polys = [[q for _, q in pts] for _, pts in passes]
        for _ in range(60):
            u, v = F(rng.randrange(10, 91), 100), F(rng.randrange(10, 91), 100)
            est = float(g) / math.sqrt(1 - normal_x(patch, u, v) ** 2)
            d = min(fdist(patch.at(u, v), poly) for poly in polys)
            assert d <= 0.55 * est + float(eps)


def test_a_wall_facing_the_planes_is_rejected():
    with pytest.raises(ValueError):
        BilinearPatch((5, 0, 0), (5, 4, 0), (5, 0, 3), (5, 4, 3))


def test_bad_input():
    with pytest.raises(ValueError):
        iso_planar(ramp(1), 0, 1)
    with pytest.raises(ValueError):
        iso_planar(ramp(1), 1, 0)
