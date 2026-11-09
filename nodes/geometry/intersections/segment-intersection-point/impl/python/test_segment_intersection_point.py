# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segment-intersection-point/. The authors are listed in prov/DG9ZZA.jsonl.

import random
from fractions import Fraction
from typing import Optional

from segment_intersection_point import segment_intersection, segments_intersect

F = Fraction
P = tuple[Fraction, Fraction]


def on_segment_param(a: P, b: P, p: P) -> bool:
    """Is p = a + t (b - a) for some t in [0, 1]? Uses no orientation test."""
    if a == b:
        return p == a
    if a[0] != b[0]:
        t = (p[0] - a[0]) / (b[0] - a[0])
    else:
        t = (p[1] - a[1]) / (b[1] - a[1])
    return 0 <= t <= 1 and a[0] + t * (b[0] - a[0]) == p[0] and a[1] + t * (b[1] - a[1]) == p[1]


def line_meet(a: P, b: P, c: P, d: P) -> Optional[P]:
    """The common point of the lines ab and cd by Cramer's rule, or None if they are parallel."""
    a1, b1 = b[1] - a[1], a[0] - b[0]
    c1 = a1 * a[0] + b1 * a[1]
    a2, b2 = d[1] - c[1], c[0] - d[0]
    c2 = a2 * c[0] + b2 * c[1]
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    return ((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det)


def brute(a: P, b: P, c: P, d: P) -> tuple[P, ...]:
    """The intersection is convex, so its extreme points are among a, b, c, d and the meet of the lines."""
    cand = [a, b, c, d]
    m = line_meet(a, b, c, d) if a != b and c != d else None
    if m is not None:
        cand.append(m)
    good = sorted({p for p in cand if on_segment_param(a, b, p) and on_segment_param(c, d, p)})
    if not good:
        return ()
    if good[0] == good[-1]:
        return (good[0],)
    return (good[0], good[-1])


def fp(p: tuple[int, int]) -> P:
    return (F(p[0]), F(p[1]))


def test_named_cases() -> None:
    si = segment_intersection
    # proper crossing with a non-integer point
    assert si((0, 0), (3, 1), (0, 1), (3, 0)) == ((F(3, 2), F(1, 2)),)
    # T-junction: an end point in the interior of the other segment
    assert si((0, 0), (4, 0), (2, 0), (2, 5)) == ((F(2), F(0)),)
    # shared end point, not collinear
    assert si((0, 0), (1, 1), (1, 1), (2, 0)) == ((F(1), F(1)),)
    # collinear and touching at one end
    assert si((0, 0), (1, 1), (1, 1), (2, 2)) == ((F(1), F(1)),)
    # collinear overlap
    assert si((0, 0), (4, 4), (2, 2), (6, 6)) == ((F(2), F(2)), (F(4), F(4)))
    # collinear and disjoint
    assert si((0, 0), (1, 1), (2, 2), (3, 3)) == ()
    # vertical segments: crossing, overlapping and disjoint
    assert si((1, -1), (1, 1), (0, 0), (2, 0)) == ((F(1), F(0)),)
    assert si((1, 0), (1, 5), (1, 3), (1, 9)) == ((F(1), F(3)), (F(1), F(5)))
    assert si((1, 0), (1, 2), (1, 3), (1, 9)) == ()
    # parallel, not collinear
    assert si((0, 0), (2, 2), (0, 1), (2, 3)) == ()
    # the lines cross outside both segments
    assert si((0, 0), (1, 0), (2, 1), (2, 5)) == ()
    # degenerate segments that are single points
    assert si((1, 1), (1, 1), (0, 0), (2, 2)) == ((F(1), F(1)),)
    assert si((1, 1), (1, 1), (0, 0), (2, 3)) == ()
    assert si((1, 1), (1, 1), (1, 1), (1, 1)) == ((F(1), F(1)),)
    assert si((1, 1), (1, 1), (2, 1), (2, 1)) == ()
    # the order of the end points does not matter
    assert si((4, 4), (0, 0), (6, 6), (2, 2)) == ((F(2), F(2)), (F(4), F(4)))
    assert segments_intersect((0, 0), (2, 0), (1, 0), (1, 0))


def test_fractions_and_large_ints() -> None:
    a, b = (F(1, 3), F(0)), (F(1, 3), F(1))
    c, d = (F(0), F(1, 7)), (F(1), F(1, 7))
    assert segment_intersection(a, b, c, d) == ((F(1, 3), F(1, 7)),)
    big = 10**20
    # nearly parallel segments that floats would get wrong
    assert segment_intersection((0, 0), (big, big + 1), (1, 0), (big + 1, big + 1)) == ()
    assert segment_intersection((0, 0), (2 * big, 2), (big, 0), (big, 5)) == ((F(big), F(1)),)


def test_random_against_brute_force() -> None:
    rng = random.Random(20260507)
    for trial in range(4000):
        r = rng.choice([1, 2, 3, 5, 50])
        pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(4)]
        if trial % 5 == 0:
            # force all four points on one random line through the origin
            dx, dy = rng.choice([(1, 0), (0, 1), (1, 1), (2, -1), (1, 3)])
            pts = [(k * dx, k * dy) for k in (rng.randint(-r, r) for _ in range(4))]
        if trial % 7 == 0:
            pts[2] = pts[rng.randint(0, 1)]  # a shared end point
        if trial % 11 == 0:
            pts[1] = pts[0]  # a degenerate segment
        a, b, c, d = pts
        got = segment_intersection(a, b, c, d)
        want = brute(fp(a), fp(b), fp(c), fp(d))
        assert got == want, (pts, got, want)
        assert segment_intersection(c, d, a, b) == want
        assert segment_intersection(b, a, d, c) == want
        assert segments_intersect(a, b, c, d) == (len(want) > 0)
