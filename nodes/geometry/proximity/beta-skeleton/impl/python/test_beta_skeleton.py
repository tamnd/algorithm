# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beta-skeleton/. The authors are listed in prov/8WP4AF.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from beta_skeleton import BetaSkeleton, dist2

EXAMPLE = [(1, 3), (1, 11), (2, 8), (5, 1), (9, 6), (11, 1), (11, 4)]
BETAS = [Fraction(1, 3), Fraction(1, 2), Fraction(9, 10), 1, Fraction(3, 2), 2, Fraction(5, 2), 4]


def float_region_margin(p, q, r, beta):
    """Signed margin by an independent float computation with explicit circle centers:
    positive inside the region, negative outside."""
    px, py = map(float, p)
    qx, qy = map(float, q)
    rx, ry = map(float, r)
    b = float(beta)
    L = math.hypot(qx - px, qy - py)
    if b >= 1:
        rad = b * L / 2
        c1 = (px + b / 2 * (qx - px), py + b / 2 * (qy - py))
        c2 = (qx + b / 2 * (px - qx), qy + b / 2 * (py - qy))
    else:
        rad = L / (2 * b)
        mx, my = (px + qx) / 2, (py + qy) / 2
        off = math.sqrt(max(rad * rad - L * L / 4, 0.0))
        nx, ny = -(qy - py) / L, (qx - px) / L
        c1 = (mx + off * nx, my + off * ny)
        c2 = (mx - off * nx, my - off * ny)
    return min(rad - math.hypot(rx - c1[0], ry - c1[1]), rad - math.hypot(rx - c2[0], ry - c2[1]))


def gabriel(P):
    n = len(P)
    return {
        (i, j)
        for i, j in itertools.combinations(range(n), 2)
        if all((P[i][0] - P[k][0]) * (P[j][0] - P[k][0]) + (P[i][1] - P[k][1]) * (P[j][1] - P[k][1]) > 0 for k in range(n) if k not in (i, j))
    }


def rng_edges(P):
    n = len(P)
    return {
        (i, j)
        for i, j in itertools.combinations(range(n), 2)
        if not any(max(dist2(P[i], P[k]), dist2(P[j], P[k])) < dist2(P[i], P[j]) for k in range(n) if k not in (i, j))
    }


def test_example() -> None:
    counts = {b: len(BetaSkeleton(EXAMPLE, b).edges()) for b in [Fraction(9, 10), 1, Fraction(3, 2), 2, Fraction(5, 2), 10]}
    assert counts == {Fraction(9, 10): 11, 1: 9, Fraction(3, 2): 8, 2: 7, Fraction(5, 2): 5, 10: 4}
    assert len(BetaSkeleton(EXAMPLE, 1, closed=True).edges()) == 8
    g = BetaSkeleton(EXAMPLE, Fraction(9, 10))
    assert g.has_edge(0, 4) and g.has_edge(2, 3)  # (1,3)(9,6) crosses (2,8)(5,1): not planar


def test_special_values() -> None:
    rng = random.Random(1985)
    for _ in range(150):
        pts = list({(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(rng.randint(0, 11))})
        assert set(BetaSkeleton(pts, 1, closed=True).edges()) == gabriel(pts)
        assert set(BetaSkeleton(pts, 2).edges()) == rng_edges(pts)


def test_small_and_errors() -> None:
    assert BetaSkeleton([], 1).edges() == []
    assert BetaSkeleton([(0, 0)], 3).edges() == []
    assert BetaSkeleton([(0, 0), (1, 2)], 100).edges() == [(0, 1)]
    with pytest.raises(ValueError):
        BetaSkeleton([(0, 0), (1, 1)], 0)
    with pytest.raises(ValueError):
        BetaSkeleton([(2, 2), (2, 2)], 1)


def test_collinear_points() -> None:
    # A point on the open segment pq is in every region, so only consecutive points are joined.
    pts = [(0, 0), (2, 1), (4, 2), (8, 4)]
    for b in BETAS:
        assert BetaSkeleton(pts, b).edges() == [(0, 1), (1, 2), (2, 3)]


def test_large_beta_disconnects() -> None:
    # Each corner is inside the slab-like region of the opposite side once beta is large.
    assert BetaSkeleton([(0, 0), (4, 0), (2, 3)], 3).edges() == []
    assert BetaSkeleton([(0, 0), (4, 0), (2, 3)], 2).edges() == [(0, 2), (1, 2)]  # the RNG is a path


def test_random_monotone_and_float_oracle() -> None:
    rng = random.Random(42)
    for _ in range(500):
        n = rng.randint(0, 8)
        r = rng.choice([3, 10, 1000])
        pts = list({(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)})
        graphs = [set(BetaSkeleton(pts, b).edges()) for b in BETAS]
        for small, large in zip(graphs, graphs[1:]):
            assert large <= small  # a larger beta gives a larger region and fewer edges
        b = rng.choice(BETAS)
        E = graphs[BETAS.index(b)]
        for i, j in itertools.combinations(range(len(pts)), 2):
            margins = [float_region_margin(pts[i], pts[j], pts[k], b) for k in range(len(pts)) if k not in (i, j)]
            scale = 1e-9 * max(1.0, math.sqrt(dist2(pts[i], pts[j])) * float(max(b, 1 / b)))
            if all(abs(m) > scale for m in margins):
                assert ((i, j) in E) == all(m < 0 for m in margins)
