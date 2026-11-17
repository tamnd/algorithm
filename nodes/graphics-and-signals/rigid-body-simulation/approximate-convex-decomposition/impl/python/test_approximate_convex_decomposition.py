# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-convex-decomposition/. The authors are listed in prov/1SYCDG.jsonl.

import math
import random
from fractions import Fraction

import pytest

from approximate_convex_decomposition import (
    approximate_convex_decomposition,
    area2,
    concavity,
    cross,
    normalize,
    reflex_count,
    seg_dist2,
    vertex_concavities,
)

EXAMPLE = [(0, 0), (3, 0), (4, 1), (5, 0), (8, 0), (8, 6), (6, 6), (5, 2), (3, 6), (0, 6)]


def F(*xs):
    return tuple(Fraction(x) for x in xs)


def _orient(a, b, c):
    v = cross(a, b, c)
    return (v > 0) - (v < 0)


def _on_segment(p, a, b):
    return _orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def _segments_meet(a, b, c, d):
    o1, o2, o3, o4 = _orient(a, b, c), _orient(a, b, d), _orient(c, d, a), _orient(c, d, b)
    if o1 != o2 and o3 != o4 and 0 not in (o1, o2, o3, o4):
        return True
    return _on_segment(c, a, b) or _on_segment(d, a, b) or _on_segment(a, c, d) or _on_segment(b, c, d)


def is_simple(P):
    n = len(P)
    if len(set(P)) != n or n < 3:
        return False
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        for j in range(i + 1, n):
            c, d = P[j], P[(j + 1) % n]
            if j == i + 1 or (i == 0 and j == n - 1):
                far_end = d if j == i + 1 else c  # the end of the edge cd that is not shared with ab
                near_end = a if j == i + 1 else b
                if _on_segment(far_end, a, b) or _on_segment(near_end, c, d):
                    return False  # adjacent edges that overlap
                continue
            if _segments_meet(a, b, c, d):
                return False
    return True


def on_boundary(p, P):
    return any(_on_segment(p, P[i], P[(i + 1) % len(P)]) for i in range(len(P)))


def strictly_inside(p, P):
    if on_boundary(p, P):
        return False
    inside = False
    n = len(P)
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > p[0]:
                inside = not inside
    return inside


def random_polygon(rng, n):
    """A random simple star-shaped polygon with integer vertices, counterclockwise."""
    while True:
        angles = sorted(rng.uniform(0, 2 * math.pi) for _ in range(n))
        P = []
        for a in angles:
            R = rng.uniform(4, 30)
            P.append(F(round(R * math.cos(a)), round(R * math.sin(a))))
        if is_simple(P) and area2(P) > 0:
            return P


def brute_concavities(P):
    """The squared concavities with the hull by brute force: ab is a hull edge if no point is right of it."""
    n = len(P)
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j and all(cross(P[i], P[j], P[k]) >= 0 for k in range(n))]
    on_hull = {i for pair in pairs for i in pair}
    # keep the corners only: drop a point in the middle of a hull edge, as the monotone chain does
    hull = {i for i in on_hull if not any(i not in (a, b) and _on_segment(P[i], P[a], P[b]) for a, b in pairs)}
    out = []
    for v in range(n):
        if v in hull:
            out.append(Fraction(0))
            continue
        a = v
        while a not in hull:
            a = (a - 1) % n
        b = v
        while b not in hull:
            b = (b + 1) % n
        out.append(seg_dist2(P[v], P[a], P[b]))
    return out


def test_page_example():
    P = normalize(EXAMPLE)
    assert area2(P) == 82
    conc = vertex_concavities(P)
    assert conc[P.index(F(5, 2))] == 16 and conc[P.index(F(4, 1))] == 1
    assert sum(1 for x in conc if x) == 2
    assert len(approximate_convex_decomposition(EXAMPLE, 4)) == 1
    two = approximate_convex_decomposition(EXAMPLE, 1)
    assert len(two) == 2
    assert sorted(area2(X) / 2 for X in two) == [Fraction(82, 5), Fraction(123, 5)]
    left = next(X for X in two if F(0, 0) in X)
    assert F(Fraction(23, 5), Fraction(2, 5)) in left
    assert max(vertex_concavities(left)) == Fraction(9, 17)  # 3 / sqrt(17) for the vertex (4, 1)
    three = approximate_convex_decomposition(EXAMPLE, Fraction(1, 2))
    assert len(three) == 3 and all(reflex_count(X) == 0 for X in three)
    assert sorted(area2(X) / 2 for X in three) == [Fraction(3, 5), Fraction(82, 5), 24]


def test_convex_input_is_one_piece():
    sq = [(0, 0), (2, 0), (2, 2), (1, 2), (0, 2)]
    D = approximate_convex_decomposition(sq, 0)
    assert len(D) == 1 and area2(D[0]) == 8 and len(D[0]) == 4
    assert concavity(sq) == 0
    assert len(approximate_convex_decomposition(list(reversed(sq)), 0)) == 1


def test_concavity_against_brute_force():
    rng = random.Random(5)
    for _ in range(60):
        P = random_polygon(rng, rng.randint(5, 12))
        P = normalize(P)
        assert vertex_concavities(P) == brute_concavities(P)


def test_a_reflex_vertex_has_positive_concavity():
    rng = random.Random(6)
    for _ in range(60):
        P = normalize(random_polygon(rng, rng.randint(5, 12)))
        conc = vertex_concavities(P)
        for i in range(len(P)):
            if cross(P[i - 1], P[i], P[(i + 1) % len(P)]) < 0:
                assert conc[i] > 0


@pytest.mark.parametrize("tau", [0, 1, 3])
def test_random_polygons_are_partitioned(tau):
    rng = random.Random(100 + tau)
    for _ in range(25):
        P = normalize(random_polygon(rng, rng.randint(6, 12)))
        r = reflex_count(P)
        D = approximate_convex_decomposition(P, tau)
        assert 1 <= len(D) <= r + 1
        assert sum(area2(X) for X in D) == area2(P)
        for X in D:
            assert area2(X) > 0 and is_simple(X)
            assert max(vertex_concavities(X)) <= Fraction(tau) ** 2
            assert all(strictly_inside(v, P) or on_boundary(v, P) for v in X)
            if tau == 0:
                assert reflex_count(X) == 0
        xs = [p[0] for p in P]
        ys = [p[1] for p in P]
        for _ in range(40):
            p = (Fraction(rng.randint(int(min(xs)) * 16, int(max(xs)) * 16), 16) + Fraction(1, 97),
                 Fraction(rng.randint(int(min(ys)) * 16, int(max(ys)) * 16), 16) + Fraction(1, 89))
            if any(on_boundary(p, X) for X in D):
                continue
            count = sum(strictly_inside(p, X) for X in D)
            assert count == (1 if strictly_inside(p, P) else 0)


def test_a_smaller_tolerance_never_leaves_a_concave_piece():
    rng = random.Random(9)
    for _ in range(20):
        P = random_polygon(rng, 10)
        for tau in (Fraction(1, 2), 2, 5):
            for X in approximate_convex_decomposition(P, tau):
                assert concavity(X) <= tau + 1e-12
