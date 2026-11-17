# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lin-canny-closest-features/. The authors are listed in prov/PQTB3Y.jsonl.

import random
from fractions import Fraction

from lin_canny_closest_features import closest_on_segment, lin_canny, segments_intersect


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
        pts = [(cx + rng.randint(-r, r), cy + rng.randint(-r, r)) for _ in range(rng.randint(3, 9))]
        h = hull(pts)
        if len(h) >= 3:
            return [(Fraction(x), Fraction(y)) for x, y in h]


def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def inside(P, x):
    return all(cross(P[i], P[(i + 1) % len(P)], x) >= 0 for i in range(len(P)))


def brute(A, B):
    """(intersecting, squared distance) over all vertex-edge feature pairs."""
    for i in range(len(A)):
        for j in range(len(B)):
            if segments_intersect(A[i], A[(i + 1) % len(A)], B[j], B[(j + 1) % len(B)]):
                return True, 0
    if inside(B, A[0]) or inside(A, B[0]):
        return True, 0
    best = None
    for P, Q in ((A, B), (B, A)):
        for p in P:
            for k in range(len(Q)):
                c = closest_on_segment(p, Q[k], Q[(k + 1) % len(Q)])
                v = d2(p, c)
                best = v if best is None or v < best else best
    return False, best


def feature_dist2(P, f, Q, g):
    def pts(R, h):
        if h[0] == "v":
            return [R[h[1]]]
        return [R[h[1]], R[(h[1] + 1) % len(R)]]

    a, b = pts(P, f), pts(Q, g)
    best = None
    for p in a:
        for k in range(len(b)):
            seg = (b[k], b[(k + 1) % len(b)]) if len(b) == 2 else (b[0], b[0])
            c = closest_on_segment(p, *seg) if seg[0] != seg[1] else seg[0]
            best = d2(p, c) if best is None or d2(p, c) < best else best
    for p in b:
        for k in range(len(a)):
            seg = (a[k], a[(k + 1) % len(a)]) if len(a) == 2 else (a[0], a[0])
            c = closest_on_segment(p, *seg) if seg[0] != seg[1] else seg[0]
            best = d2(p, c) if best is None or d2(p, c) < best else best
    return best


def F(x, y):
    return (Fraction(x), Fraction(y))


def test_page_example():
    A = [F(0, 0), F(4, 0), F(4, 3), F(0, 3)]
    B = [F(7, 1), F(10, 2), F(8, 5)]
    res = lin_canny(A, B, ("v", 0), ("v", 1))
    assert res.separated
    assert res.dist2 == 9
    assert (res.fa, res.fb) == (("e", 1), ("v", 0))
    assert res.pa == F(4, 1) and res.pb == F(7, 1)
    assert res.steps == 5


def test_vertex_vertex_and_edge_edge_answers():
    A = [F(0, 0), F(2, 0), F(1, 2)]
    B = [F(5, 3), F(6, 5), F(4, 4)]
    res = lin_canny(A, B, ("e", 0), ("e", 2))
    assert res.separated and res.dist2 == brute(A, B)[1]
    C = [F(0, 0), F(2, 0), F(2, 2), F(0, 2)]
    D = [F(5, 0), F(7, 0), F(7, 2), F(5, 2)]  # parallel edges: an edge-edge pair is closest
    res = lin_canny(C, D, ("v", 3), ("v", 1))
    assert res.separated and res.dist2 == 9


def test_intersecting_inputs_are_reported():
    A = [F(0, 0), F(4, 0), F(4, 4), F(0, 4)]
    B = [F(1, 1), F(2, 1), F(2, 2)]  # B inside A
    for fa in [("v", k) for k in range(4)] + [("e", k) for k in range(4)]:
        for fb in [("v", k) for k in range(3)] + [("e", k) for k in range(3)]:
            res = lin_canny(A, B, fa, fb)
            assert not res.separated and res.dist2 == 0
    touching = [F(4, 1), F(6, 1), F(6, 3)]  # the vertex (4, 1) lies on edge 1 of A
    res = lin_canny(A, touching)
    assert not res.separated


def test_random_pairs_against_brute_force():
    rng = random.Random(2024)
    count = 0
    for _ in range(700):
        A = random_polygon(rng, 0, 0, 6)
        B = random_polygon(rng, rng.randint(-14, 14), rng.randint(-14, 14), 6)
        hit, dist = brute(A, B)
        fa = (rng.choice("ve"), rng.randrange(len(A)))
        fb = (rng.choice("ve"), rng.randrange(len(B)))
        res = lin_canny(A, B, fa, fb)
        assert res.separated == (not hit)
        if not hit:
            count += 1
            assert res.dist2 == dist
            assert d2(res.pa, res.pb) == dist
            assert feature_dist2(A, res.fa, B, res.fb) == dist
            assert res.steps <= 4 * len(A) * len(B) + 1
    assert count >= 300


def test_coherent_motion_with_warm_start():
    rng = random.Random(5)
    A = random_polygon(rng, 0, 0, 5)
    B0 = random_polygon(rng, 0, 0, 3)
    fa, fb = ("v", 0), ("v", 0)
    for step in range(200):
        # B goes around A on a square path of radius 12, in steps of 1/2
        t = Fraction(step, 2)
        side, s = divmod(t, 12)
        path = [(12 - 2 * s, 12), (-12, 12 - 2 * s), (-12 + 2 * s, -12), (12, -12 + 2 * s)]
        ox, oy = path[int(side) % 4]
        B = [(x + ox, y + oy) for x, y in B0]
        hit, dist = brute(A, B)
        res = lin_canny(A, B, fa, fb)
        assert res.separated == (not hit)
        if res.separated:
            assert res.dist2 == dist
            fa, fb = res.fa, res.fb
