# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/voronoi-pocket-machining/. The authors are listed in prov/MEJQSV.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from voronoi_pocket_machining import (
    convex_hull,
    cross,
    half_planes,
    medial_axis,
    offset_from_axis,
    voronoi_pocket,
)


def unit_vectors():
    base = {(F(1), F(0))}
    for m in range(2, 5):
        for n in range(1, m):
            k = m * m + n * n
            base.add((F(m * m - n * n, k), F(2 * m * n, k)))
    out = set()
    for a, b in base:
        for x, y in ((a, b), (b, a)):
            for sx in (1, -1):
                for sy in (1, -1):
                    out.add((sx * x, sy * y))
    return sorted(out)


UNITS = unit_vectors()


def clip(poly, a, b, c):
    """Reference: clip a convex polygon by a x + b y <= c (Sutherland-Hodgman)."""
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = c - a * p[0] - b * p[1], c - a * q[0] - b * q[1]
        if fp >= 0:
            out.append(p)
        if fp * fq < 0:
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def reference_offset(poly, d):
    """The offset by clipping with all moved half-planes, a method that does not use the axis."""
    _, planes = half_planes(poly)
    q = [(F(x), F(y)) for x, y in poly]
    for a, b, c in planes:
        q = clip(q, a, b, c - d)
        if not q:
            return []
    return convex_hull(q)


def random_convex(rng):
    while True:
        normals = rng.sample(UNITS, rng.randrange(3, 9))
        poly = [(F(-500), F(-500)), (F(500), F(-500)), (F(500), F(500)), (F(-500), F(500))]
        for a, b in normals:
            poly = clip(poly, a, b, F(rng.randrange(2, 16)))
            if not poly:
                break
        if len(poly) < 3 or any(abs(x) == 500 or abs(y) == 500 for x, y in poly):
            continue
        poly = convex_hull(poly)
        if len(poly) >= 3:
            return poly


def depth(planes, p):
    return min(c - a * p[0] - b * p[1] for a, b, c in planes)


def brute_inradius(poly):
    """Largest inscribed circle by trying every triple of edge lines."""
    _, planes = half_planes(poly)
    best = None
    for i, j, k in itertools.combinations(range(len(planes)), 3):
        m = [planes[i], planes[j], planes[k]]
        a = [[x[0], x[1], F(1)] for x in m]
        det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
               + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
        if det == 0:
            continue
        # solve by elimination
        rows = [a[t] + [m[t][2]] for t in range(3)]
        for col in range(3):
            piv = next(r for r in range(col, 3) if rows[r][col] != 0)
            rows[col], rows[piv] = rows[piv], rows[col]
            for r in range(3):
                if r != col and rows[r][col] != 0:
                    f = rows[r][col] / rows[col][col]
                    rows[r] = [x - f * y for x, y in zip(rows[r], rows[col])]
        x, y, t = (rows[r][3] / rows[r][r] for r in range(3))
        if t >= 0 and depth(planes, (x, y)) == t and (best is None or t > best):
            best = t
    return best


RECT = [(0, 0), (8, 0), (8, 4), (0, 4)]
PENTAGON = [(0, 0), (20, 0), (20, 9), (8, 25), (0, 10)]
TRIANGLE = [(0, 0), (12, 0), (0, 9)]


def test_triangle_has_one_node():
    arcs, (node, t) = medial_axis(TRIANGLE)
    assert node == (3, 3) and t == 3
    assert len(arcs) == 3 and all(a.p1 == (3, 3) for a in arcs)


def test_rectangle_axis_and_offsets():
    arcs, (node, t) = medial_axis(RECT)
    assert t == 2
    ends = sorted({a.p1 for a in arcs})
    assert ends == [(2, 2), (6, 2)]
    assert offset_from_axis(arcs, 1) == [(1, 1), (7, 1), (7, 3), (1, 3)]
    assert offset_from_axis(arcs, 2) == [(2, 2), (6, 2)]
    assert offset_from_axis(arcs, F(5, 2)) == []


def test_arcs_are_on_the_medial_axis():
    rng = random.Random(5)
    for poly in [RECT, PENTAGON, TRIANGLE] + [random_convex(rng) for _ in range(40)]:
        _, planes = half_planes(poly)
        arcs, _ = medial_axis(poly)
        assert len(arcs) == 2 * len(poly) - 3
        for a in arcs:
            assert a.t0 <= a.t1
            mid = ((a.p0[0] + a.p1[0]) / 2, (a.p0[1] + a.p1[1]) / 2)
            for p, t in ((a.p0, a.t0), (a.p1, a.t1), (mid, (a.t0 + a.t1) / 2)):
                assert depth(planes, p) == t
                for e in (a.left, a.right):
                    ea, eb, ec = planes[e]
                    assert ec - ea * p[0] - eb * p[1] == t


def test_offsets_match_clipping():
    rng = random.Random(9)
    for poly in [RECT, PENTAGON, TRIANGLE] + [random_convex(rng) for _ in range(40)]:
        arcs, (_, deepest) = medial_axis(poly)
        times = sorted({a.t1 for a in arcs})
        ds = times + [F(rng.randrange(0, 40), 4) for _ in range(6)] + [deepest + F(1, 7)]
        for d in ds:
            assert offset_from_axis(arcs, d) == reference_offset(poly, d)


def test_deepest_node_is_the_inradius():
    rng = random.Random(13)
    for poly in [RECT, PENTAGON] + [random_convex(rng) for _ in range(30)]:
        _, (node, t) = medial_axis(poly)
        assert t == brute_inradius(poly)
        _, planes = half_planes(poly)
        assert depth(planes, node) == t


def test_pocket_loops_and_links():
    rng = random.Random(17)
    for poly in [PENTAGON] + [random_convex(rng) for _ in range(20)]:
        _, planes = half_planes(poly)
        r = F(rng.randrange(1, 5), 2)
        s = r * F(rng.randrange(2, 5), 4)
        loops, links = voronoi_pocket(poly, r, s)
        assert len(links) == max(0, len(loops) - 1)
        for k, (d, loop) in enumerate(loops):
            assert d == r + k * s
            assert convex_hull(loop) == reference_offset(poly, d)
        for k, link in enumerate(links):
            assert link[0] == loops[k][1][0] and link[-1] == loops[k + 1][1][0]
            ts = [depth(planes, p) for p in link]
            assert ts == sorted(ts) and ts[0] >= r


def test_pentagon_example():
    arcs, (node, t) = medial_axis(PENTAGON)
    assert node == (F(37, 4), F(35, 4)) and t == F(35, 4)
    assert sorted({(a.p1, a.t1) for a in arcs[:5]}) == [
        ((F(8), F(8)), F(8)),
        ((F(37, 4), F(35, 4)), F(35, 4)),
        ((F(53, 4), F(27, 4)), F(27, 4)),
    ]
    loops, links = voronoi_pocket(PENTAGON, 2, 2)
    assert [(d, len(q)) for d, q in loops] == [(2, 5), (4, 5), (6, 5), (8, 3)]
    assert loops[3][1] == [(F(43, 4), 8), (F(64, 7), F(71, 7)), (8, 8)]
    assert links[2] == [(14, 6), (F(53, 4), F(27, 4)), (F(43, 4), 8)]


def test_bad_input():
    with pytest.raises(ValueError):
        medial_axis([(0, 0), (1, 0), (0, 1)])
    with pytest.raises(ValueError):
        medial_axis([(0, 0), (0, 4), (3, 0)])
    with pytest.raises(ValueError):
        voronoi_pocket(TRIANGLE, 1, 0)
