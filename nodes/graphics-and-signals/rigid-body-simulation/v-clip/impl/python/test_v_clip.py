# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/v-clip/. The authors are listed in prov/D7J6QE.jsonl.

import random
from fractions import Fraction

from v_clip import clip_edge, closest_on_segment, handle_local_min, segments_intersect, v_clip


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
                v = d2(p, closest_on_segment(p, Q[k], Q[(k + 1) % len(Q)]))
                best = v if best is None or v < best else best
    return False, best


def points_of(P, f):
    if f[0] == "v":
        return [P[f[1]]]
    return [P[f[1]], P[(f[1] + 1) % len(P)]]


def on_feature(P, f, x):
    pts = points_of(P, f)
    if len(pts) == 1:
        return x == pts[0]
    return closest_on_segment(x, pts[0], pts[1]) == x


def F(x, y):
    return (Fraction(x), Fraction(y))


def page_example():
    A = [F(0, 0), F(4, 0), F(4, 3), F(0, 3)]
    B = [F(7, 1), F(10, 2), F(8, 5)]
    return A, B


def test_clip_of_the_page_example():
    A, B = page_example()
    # edge e2 of B against VR(a2): clipped to [0, 1/2] by the plane of edge e1 of A
    assert clip_edge(A, 2, B[2], B[0]) == (0, Fraction(1, 2), None, 1, None)
    # edge e1 of A against VR(b0): clipped to [0, 7/12] by the plane of edge e2 of B
    assert clip_edge(B, 0, A[1], A[2]) == (0, Fraction(7, 12), None, 2, None)
    # edge e1 of A against VR(b1): excluded by the plane of edge e0 of B
    assert clip_edge(B, 1, A[1], A[2])[4] == 0


def test_page_example():
    A, B = page_example()
    res = v_clip(A, B, ("v", 2), ("e", 2))
    assert res.status == "disjoint"
    assert res.dist2 == 9
    assert (res.fa, res.fb) == (("e", 1), ("v", 0))
    assert res.pa == F(4, 1) and res.pb == F(7, 1)
    assert res.steps == 3
    assert v_clip(A, B, ("v", 0), ("v", 1)).steps == 5


def test_penetration_is_reported():
    A = [F(0, 0), F(4, 0), F(4, 4), F(0, 4)]
    B = [F(1, 1), F(2, 1), F(2, 2)]
    for fa in [("v", k) for k in range(4)] + [("e", k) for k in range(4)]:
        for fb in [("v", k) for k in range(3)] + [("e", k) for k in range(3)]:
            res = v_clip(A, B, fa, fb)
            assert res.status == "penetration"
    assert handle_local_min(A, F(1, 1)) is None
    assert handle_local_min(A, F(5, 1)) == 1
    crossing = [F(3, -1), F(6, 2), F(3, 2)]
    assert v_clip(A, crossing).status == "penetration"
    touching = [F(4, 4), F(6, 5), F(5, 6)]  # a common vertex
    assert v_clip(A, touching).status == "penetration"


def test_degenerate_but_disjoint_configurations():
    sq = [F(0, 0), F(2, 0), F(2, 2), F(0, 2)]
    for other in (
        [F(4, 0), F(6, 0), F(6, 2), F(4, 2)],  # parallel faces
        [F(4, 2), F(6, 4), F(4, 4)],  # vertex on the boundary of a vertex region
        [F(3, 3), F(5, 3), F(5, 5), F(3, 5)],  # vertex-vertex
        [F(1, 4), F(3, 4), F(2, 6)],  # parallel edges that overlap in part
    ):
        hit, dist = brute(sq, other)
        assert not hit
        for fa in [("v", k) for k in range(4)] + [("e", k) for k in range(4)]:
            for fb in [("v", k) for k in range(len(other))] + [("e", k) for k in range(len(other))]:
                res = v_clip(sq, other, fa, fb)
                assert res.status == "disjoint" and res.dist2 == dist


def test_random_pairs_against_brute_force():
    rng = random.Random(1998)
    disjoint = 0
    for _ in range(700):
        A = random_polygon(rng, 0, 0, 6)
        B = random_polygon(rng, rng.randint(-14, 14), rng.randint(-14, 14), 6)
        hit, dist = brute(A, B)
        fa = (rng.choice("ve"), rng.randrange(len(A)))
        fb = (rng.choice("ve"), rng.randrange(len(B)))
        res = v_clip(A, B, fa, fb)
        assert (res.status == "penetration") == hit
        if not hit:
            disjoint += 1
            assert res.dist2 == dist == d2(res.pa, res.pb)
            assert on_feature(A, res.fa, res.pa) and on_feature(B, res.fb, res.pb)
        else:
            # the witness features really meet the other polygon
            if res.fa is not None and res.fb is not None and res.fa[0] == "e" and res.fb[0] == "e":
                pa, pb = points_of(A, res.fa), points_of(B, res.fb)
                assert segments_intersect(pa[0], pa[1], pb[0], pb[1])
            elif res.fb is None:
                assert inside(B, A[res.fa[1]])
            elif res.fa is None:
                assert inside(A, B[res.fb[1]])
    assert disjoint >= 300


def test_coherent_motion():
    rng = random.Random(3)
    A = random_polygon(rng, 0, 0, 5)
    B0 = random_polygon(rng, 0, 0, 3)
    fa, fb = ("v", 0), ("v", 0)
    for step in range(120):
        ox, oy = Fraction(30 - step, 4), Fraction(step % 7, 3)
        B = [(x + ox, y + oy) for x, y in B0]
        hit, dist = brute(A, B)
        res = v_clip(A, B, fa, fb)
        assert (res.status == "penetration") == hit
        if not hit:
            assert res.dist2 == dist
            fa, fb = res.fa, res.fb
        else:
            fa, fb = ("v", 0), ("v", 0)
