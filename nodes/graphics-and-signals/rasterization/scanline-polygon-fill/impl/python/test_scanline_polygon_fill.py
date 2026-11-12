# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scanline-polygon-fill/. The authors are listed in prov/VS80AE.jsonl.

import random
from fractions import Fraction

import pytest

from scanline_polygon_fill import build_edge_table, scanline_polygon_fill, scanline_spans

K = 10**6  # the moved center c + (1/K, 1/K^2) stands for c + (e, e^2) with e infinitesimal


def winding(rings, px, py):
    """Winding number of the point (px, py) by the crossing test of Sunday, in exact arithmetic."""
    w = 0
    for ring in rings:
        n = len(ring)
        for k in range(n):
            (ax, ay), (bx, by) = ring[k], ring[(k + 1) % n]
            side = (bx - ax) * (py - ay) - (px - ax) * (by - ay)
            if ay <= py:
                if by > py and side > 0:
                    w += 1
            elif by <= py and side < 0:
                w -= 1
    return w


def brute_fill(rings, width, height, rule):
    """Test each pixel center, moved by (1/K, 1/K^2), with the fill rule."""
    out = set()
    for j in range(height):
        for i in range(width):
            w = winding(rings, Fraction(2 * i + 1, 2) + Fraction(1, K), Fraction(2 * j + 1, 2) + Fraction(1, K * K))
            if (w % 2 == 1) if rule == "evenodd" else (w != 0):
                out.add((i, j))
    return out


STAR = [(5, 0), (8, 10), (0, 4), (10, 4), (2, 10)]


def test_star_rules_differ():
    odd = scanline_polygon_fill([STAR], 11, 11, "evenodd")
    nonzero = scanline_polygon_fill([STAR], 11, 11, "nonzero")
    assert odd == brute_fill([STAR], 11, 11, "evenodd")
    assert nonzero == brute_fill([STAR], 11, 11, "nonzero")
    assert odd < nonzero
    # The center pentagon has winding number 2 (up to sign): only the nonzero rule fills it.
    assert (5, 5) in nonzero and (5, 5) not in odd


def test_page_example_spans():
    assert scanline_spans([STAR], 11, 11, "evenodd") == [
        (2, 4, 6), (3, 4, 6), (4, 1, 4), (4, 6, 9), (5, 2, 3), (5, 7, 8),
        (7, 3, 7), (8, 2, 4), (8, 6, 8), (9, 2, 3), (9, 7, 8),
    ]
    assert scanline_spans([STAR], 11, 11, "nonzero") == [
        (2, 4, 6), (3, 4, 6), (4, 1, 9), (5, 2, 8), (6, 3, 7),
        (7, 3, 7), (8, 2, 4), (8, 6, 8), (9, 2, 3), (9, 7, 8),
    ]
    # Row 6 (center line y = 6.5) has four crossings, near 3.05, 3.33, 6.67 and 6.95.
    # Under the even-odd rule both spans are shorter than one pixel and hold no center.
    assert not any(j == 6 for j, _, _ in scanline_spans([STAR], 11, 11, "evenodd"))


def test_square_and_shared_edge():
    square = [(1, 1), (5, 1), (5, 4), (1, 4)]
    assert scanline_polygon_fill([square], 8, 8) == {(i, j) for i in range(1, 5) for j in range(1, 4)}
    # Two triangles that share a diagonal split the square with no gap and no overlap.
    t1 = [(1, 1), (5, 1), (5, 4)]
    t2 = [(1, 1), (5, 4), (1, 4)]
    a = scanline_polygon_fill([t1], 8, 8)
    b = scanline_polygon_fill([t2], 8, 8)
    assert not (a & b)
    assert a | b == scanline_polygon_fill([square], 8, 8)


def test_hole_and_rules():
    outer = [(0, 0), (8, 0), (8, 8), (0, 8)]
    hole_same = [(2, 2), (6, 2), (6, 6), (2, 6)]  # same direction as the outer ring
    hole_rev = hole_same[::-1]
    ring_px = {(i, j) for i in range(8) for j in range(8)} - {(i, j) for i in range(2, 6) for j in range(2, 6)}
    assert scanline_polygon_fill([outer, hole_same], 8, 8, "evenodd") == ring_px
    assert scanline_polygon_fill([outer, hole_rev], 8, 8, "evenodd") == ring_px
    assert scanline_polygon_fill([outer, hole_rev], 8, 8, "nonzero") == ring_px
    # Under the nonzero rule a hole in the same direction adds to the winding and does not cut.
    assert scanline_polygon_fill([outer, hole_same], 8, 8, "nonzero") == {(i, j) for i in range(8) for j in range(8)}


def test_thin_and_clipped():
    # A sliver between two centers fills nothing, but its edges still cross rows.
    sliver = [(Fraction(3, 4), 0), (Fraction(5, 4), 0), (Fraction(5, 4), 6), (Fraction(3, 4), 6)]
    assert scanline_polygon_fill([sliver], 4, 6) == set()
    assert sum(len(b) for b in build_edge_table([sliver], 6)) == 2
    # Parts outside the image are cut off.
    big = [(-3, -3), (20, -3), (20, 20), (-3, 20)]
    assert scanline_polygon_fill([big], 4, 3) == {(i, j) for i in range(4) for j in range(3)}
    assert scanline_polygon_fill([[(0, 0), (4, 0), (2, 0)]], 4, 4) == set()


def test_bad_rule():
    with pytest.raises(ValueError):
        scanline_spans([STAR], 4, 4, "positive")


def random_ring(rng, n, lo, hi):
    return [(Fraction(rng.randint(4 * lo, 4 * hi), 4), Fraction(rng.randint(4 * lo, 4 * hi), 4)) for _ in range(n)]


def test_random_against_brute_force():
    rng = random.Random(1981)
    for trial in range(160):
        width, height = rng.randint(1, 14), rng.randint(1, 14)
        rings = [random_ring(rng, rng.randint(3, 8), -2, 16) for _ in range(rng.randint(1, 3))]
        if trial % 4 == 0:  # integer vertices: many centers lie on no edge, but many edges meet vertices on center lines
            rings = [[(int(x), int(y)) for x, y in ring] for ring in rings]
        if trial % 5 == 0:  # vertices on center lines
            rings = [[(x, Fraction(2 * int(y) + 1, 2)) for x, y in ring] for ring in rings]
        for rule in ("evenodd", "nonzero"):
            assert scanline_polygon_fill(rings, width, height, rule) == brute_fill(rings, width, height, rule)


def test_spans_are_sorted_and_disjoint():
    rng = random.Random(7)
    for _ in range(40):
        rings = [random_ring(rng, 7, -1, 12)]
        spans = scanline_spans(rings, 12, 12, "nonzero")
        for (j1, a1, b1), (j2, a2, b2) in zip(spans, spans[1:]):
            assert (j1, b1) < (j2, a2 + 1) and a1 < b1 and a2 < b2
            if j1 == j2:
                assert b1 < a2
