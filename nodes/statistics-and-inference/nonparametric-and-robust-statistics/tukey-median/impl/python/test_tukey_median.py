# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tukey-median/. The authors are listed in prov/ES2QKG.jsonl.

import random
from fractions import Fraction
from math import ceil

from tukey_median import centroid, depth, depth_region, tukey_median


def brute_depth(x, points):
    """Oracle: the least count over closed halfplanes {y : u.(y - x) >= 0}.

    The count changes only at the normals of the vectors p - x. Every arc
    between two such normals contains a sum of two of them, or one of the
    vectors p - x itself, so this finite list of u meets every arc.
    """
    d = [(p[0] - x[0], p[1] - x[1]) for p in points]
    crit = []
    for v in d:
        if v != (0, 0):
            crit += [(-v[1], v[0]), (v[1], -v[0]), v, (-v[0], -v[1])]
    cands = list(crit)
    for a in crit:
        for b in crit:
            s = (a[0] + b[0], a[1] + b[1])
            if s != (0, 0):
                cands.append(s)
    if not cands:
        return len(points)
    return min(sum(1 for v in d if u[0] * v[0] + u[1] * v[1] >= 0) for u in cands)


def line_vertices(points):
    """All points where two lines through pairs of sample points cross."""
    lines = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            a, b = points[i], points[j]
            if a != b:
                lines.append((a, b))
    out = set(points)
    for i in range(len(lines)):
        (a, b) = lines[i]
        for j in range(i + 1, len(lines)):
            (c, e) = lines[j]
            r = (b[0] - a[0], b[1] - a[1])
            s = (e[0] - c[0], e[1] - c[1])
            den = r[0] * s[1] - r[1] * s[0]
            if den == 0:
                continue
            t = Fraction((c[0] - a[0]) * s[1] - (c[1] - a[1]) * s[0], den)
            out.add((a[0] + t * r[0], a[1] + t * r[1]))
    return out


def hull(pts):
    """Convex hull by the monotone chain, exact. Returns the vertices CCW."""
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    low, up = [], []
    for p in pts:
        while len(low) >= 2 and turn(low[-2], low[-1], p) <= 0:
            low.pop()
        low.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and turn(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return low[:-1] + up[:-1]


def random_points(rng, n, span):
    return [(rng.randint(-span, span), rng.randint(-span, span)) for _ in range(n)]


def test_depth_small_cases() -> None:
    sq = [(0, 0), (4, 0), (0, 4), (4, 4), (1, 2)]
    assert depth((1, 2), sq) == 2
    assert depth((2, 2), sq) == 2
    assert depth((0, 0), sq) == 1
    assert depth((9, 9), sq) == 0
    # On a line the depth is the one-dimensional depth min(#<=, #>=).
    line = [(i, 2 * i) for i in range(5)]
    assert [depth(p, line) for p in line] == [1, 2, 3, 2, 1]
    # Repeated points all count.
    assert depth((0, 0), [(0, 0)] * 4) == 4


def test_depth_against_brute_force() -> None:
    rng = random.Random(1)
    for trial in range(300):
        n = rng.randint(1, 9)
        pts = random_points(rng, n, 3)
        x = (Fraction(rng.randint(-8, 8), 2), Fraction(rng.randint(-8, 8), 2))
        if trial % 3 == 0:
            x = pts[rng.randrange(n)]
        assert depth(x, pts) == brute_depth(x, pts)


def test_median_against_vertex_search() -> None:
    rng = random.Random(2)
    for _ in range(25):
        n = rng.randint(3, 7)
        pts = random_points(rng, n, 4)
        med, kstar = tukey_median(pts)
        cands = line_vertices([(Fraction(a), Fraction(b)) for a, b in pts])
        best = max(depth(c, pts) for c in cands)
        assert kstar == best
        assert depth(med, pts) == kstar
        deepest = [c for c in cands if depth(c, pts) == kstar]
        assert centroid(hull(deepest)) == med or len(set(deepest)) == 1 and med == deepest[0]


def test_grid_never_deeper() -> None:
    rng = random.Random(3)
    for _ in range(8):
        pts = random_points(rng, 9, 5)
        med, kstar = tukey_median(pts)
        for gx in range(-10, 11):
            for gy in range(-10, 11):
                assert depth((Fraction(gx, 2), Fraction(gy, 2)), pts) <= kstar


def test_centerpoint_bound() -> None:
    rng = random.Random(4)
    for _ in range(40):
        n = rng.randint(1, 14)
        pts = random_points(rng, n, 6)
        med, kstar = tukey_median(pts)
        assert kstar >= ceil(n / 3)
        assert depth(med, pts) == kstar


def test_three_clusters_reach_the_bound() -> None:
    # Three tight groups at the corners of a triangle: max depth is n/3.
    pts = []
    for cx, cy in ((0, 0), (30, 0), (0, 30)):
        pts += [(cx, cy), (cx + 1, cy), (cx, cy + 1)]
    med, kstar = tukey_median(pts)
    assert kstar == 3


def test_regions_are_nested() -> None:
    rng = random.Random(5)
    pts = random_points(rng, 10, 6)
    med, kstar = tukey_median(pts)
    for k in range(1, kstar + 1):
        region = depth_region(pts, k)
        assert region
        for v in region:
            assert depth(v, pts) >= k
    assert depth_region(pts, kstar + 1) == []


def test_collinear_and_tiny() -> None:
    assert tukey_median([(3, 1)]) == ((3, 1), 1)
    med, k = tukey_median([(0, 0), (2, 2), (10, 10), (4, 4)])
    assert med == (3, 3) and k == 2
    med, k = tukey_median([(0, 0), (1, 0), (5, 0)])
    assert med == (1, 0) and k == 2


def test_page_example() -> None:
    pts = [(0, 0), (6, 0), (0, 6), (6, 6), (2, 3), (3, 1), (9, 9)]
    med, k = tukey_median(pts)
    assert k == 3
    assert med == (Fraction(39, 14), Fraction(39, 14))
    assert sorted(depth_region(pts, 3)) == [(Fraction(18, 7), Fraction(18, 7)), (3, 3)]
    assert depth_region(pts, 4) == []
    assert [depth(p, pts) for p in pts] == [1, 1, 1, 2, 2, 2, 1]
