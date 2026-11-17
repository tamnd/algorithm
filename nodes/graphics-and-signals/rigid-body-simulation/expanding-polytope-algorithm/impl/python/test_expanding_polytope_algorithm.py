# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expanding-polytope-algorithm/. The authors are listed in prov/PP6HVM.jsonl.

import math
import random

from expanding_polytope_algorithm import epa, gjk_triangle, polygon_support


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def random_polygon(rng, cx, cy, r):
    while True:
        pts = [(cx + rng.uniform(-r, r), cy + rng.uniform(-r, r)) for _ in range(rng.randint(3, 9))]
        h = hull(pts)
        if len(h) >= 3:
            return h


def brute_depth(A, B):
    """The distance from the origin to the boundary of hull(A - B), or None if the origin is outside."""
    H = hull([(a[0] - b[0], a[1] - b[1]) for a in A for b in B])
    best = None
    for i in range(len(H)):
        p, q = H[i], H[(i + 1) % len(H)]
        e = (q[0] - p[0], q[1] - p[1])
        L = math.hypot(*e)
        s = (e[1] * p[0] - e[0] * p[1]) / L  # signed distance of the origin, outward positive
        if s <= 0:
            return None
        best = s if best is None or s < best else best
    return best


def inside(P, x, tol=1e-9):
    return all(cross(P[i], P[(i + 1) % len(P)], x) >= -tol for i in range(len(P)))


def test_page_example():
    A = [(0.0, 0.0), (4.0, 0.0), (4.0, 3.0), (0.0, 3.0)]
    B = [(3.0, 1.0), (6.0, 2.0), (4.0, 4.0)]
    sa, sb = polygon_support(A), polygon_support(B)
    assert [t[0] for t in gjk_triangle(sa, sb)] == [(1.0, 2.0), (-6.0, 1.0), (1.0, -1.0)]
    depth, n, pa, pb, it = epa(sa, sb)
    assert (depth, n, pa, pb, it) == (1.0, (-1.0, 0.0), (4.0, 1.0), (3.0, 1.0), 2)
    assert brute_depth(A, B) == 1.0


def test_gjk_triangle_contains_the_origin():
    rng = random.Random(7)
    found = 0
    for _ in range(400):
        A = random_polygon(rng, 0, 0, 4)
        B = random_polygon(rng, rng.uniform(-6, 6), rng.uniform(-6, 6), 4)
        tri = gjk_triangle(polygon_support(A), polygon_support(B))
        assert (tri is not None) == (brute_depth(A, B) is not None)
        if tri is not None:
            found += 1
            w = [t[0] for t in tri]
            assert cross(w[0], w[1], w[2]) > 0
            assert inside(w, (0.0, 0.0))
            for wi, a, b in tri:
                assert (a[0] - b[0], a[1] - b[1]) == wi
    assert found >= 100


def test_random_pairs_against_the_hull_of_differences():
    rng = random.Random(2001)
    deep = 0
    for _ in range(500):
        A = random_polygon(rng, 0, 0, 5)
        B = random_polygon(rng, rng.uniform(-7, 7), rng.uniform(-7, 7), 5)
        ref = brute_depth(A, B)
        res = epa(polygon_support(A), polygon_support(B), eps=1e-12)
        assert (res is None) == (ref is None)
        if res is None:
            continue
        deep += 1
        depth, n, pa, pb, _ = res
        assert abs(depth - ref) <= 1e-9 * (1 + ref)
        assert abs(math.hypot(*n) - 1) < 1e-12
        # moving A by depth * n makes the shapes touch: no difference point is beyond depth along -n
        diffs = [(a[0] - b[0], a[1] - b[1]) for a in A for b in B]
        reach = max(-n[0] * w[0] - n[1] * w[1] for w in diffs)
        assert abs(reach - depth) <= 1e-9 * (1 + depth)
        # the witness points lie on the shapes and differ by the deepest point
        assert inside(A, pa) and inside(B, pb)
        assert abs(pa[0] - pb[0] + depth * n[0]) < 1e-9 and abs(pa[1] - pb[1] + depth * n[1]) < 1e-9
    assert deep >= 150


def test_disjoint_and_touching_shapes():
    sq = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]
    for dx, dy in ((3.0, 0.0), (-5.0, 1.0), (2.5, 2.5)):
        other = [(x + dx, y + dy) for x, y in sq]
        assert epa(polygon_support(sq), polygon_support(other)) is None
    for dx, dy in ((2.0, 0.0), (2.0, 2.0), (0.0, -2.0), (-2.0, 1.0)):
        # touching shapes: GJK may stop with the origin on the boundary, or EPA returns depth 0
        other = [(x + dx, y + dy) for x, y in sq]
        res = epa(polygon_support(sq), polygon_support(other))
        assert res is None or res[0] == 0
    inner = [(0.5, 0.5), (1.5, 0.5), (1.0, 1.5)]
    depth, n, _, _, _ = epa(polygon_support(sq), polygon_support(inner))
    assert abs(depth - 1.5) < 1e-12  # push the square down by 1.5 to clear the triangle


def disc(c, r):
    def s(d):
        L = math.hypot(*d)
        return (c[0] + r * d[0] / L, c[1] + r * d[1] / L)

    return s


def test_smooth_shapes_need_the_tolerance():
    # two discs: the true depth is 2 + 1.5 - 1 = 2.5 along the x axis
    counts = []
    for eps in (1e-2, 1e-4, 1e-6, 1e-8):
        depth, n, _, _, it = epa(disc((0.0, 0.0), 2.0), disc((1.0, 0.0), 1.5), eps=eps)
        assert depth <= 2.5 + 1e-12 and 2.5 <= depth + eps + 1e-12
        assert n[0] < 0 and abs(n[1]) <= 10 * math.sqrt(eps)
        counts.append(it)
    assert counts == sorted(counts) and counts[-1] > counts[0]
