# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/half-plane-intersection-deque/. The authors are listed in prov/EFZJWK.jsonl.

import random
from fractions import Fraction

from half_plane_intersection_deque import cross, half_plane_intersection, meet


def inside(h, x) -> bool:
    (p, d) = h
    return cross(d, (x[0] - p[0], x[1] - p[1])) >= 0


def strict_hull(pts: list) -> list:
    pts = sorted(set(pts))
    if len(pts) < 3:
        return []

    def chain(seq: list) -> list:
        out: list = []
        for p in seq:
            while len(out) >= 2 and cross((out[-1][0] - out[-2][0], out[-1][1] - out[-2][1]), (p[0] - out[-1][0], p[1] - out[-1][1])) <= 0:
                out.pop()
            out.append(p)
        return out

    lower, upper = chain(pts), chain(pts[::-1])
    hull = lower[:-1] + upper[:-1]
    return hull if len(hull) >= 3 else []


def brute(planes: list) -> list:
    cands = []
    for i in range(len(planes)):
        for j in range(i + 1, len(planes)):
            x = meet(planes[i], planes[j])
            if x is not None and all(inside(h, x) for h in planes):
                cands.append(x)
    return strict_hull(cands)


def same_polygon(a: list, b: list) -> bool:
    if len(a) != len(b):
        return False
    if not a:
        return True
    if b[0] not in a:
        return False
    k = a.index(b[0])
    return a[k:] + a[:k] == b


def box(lo: int, hi: int) -> list:
    return [((lo, lo), (1, 0)), ((hi, lo), (0, 1)), ((hi, hi), (-1, 0)), ((lo, hi), (0, -1))]


def test_example() -> None:
    # y >= 0, y >= 1, y >= x - 2, x <= 4, x + y <= 7, y <= 4, x >= 0, x + y >= 5
    planes = [((0, 0), (1, 0)), ((0, 1), (1, 0)), ((2, 0), (1, 1)), ((4, 0), (0, 1)), ((7, 0), (-1, 1)), ((0, 4), (-1, 0)), ((0, 0), (0, -1)), ((5, 0), (1, -1))]
    got = half_plane_intersection(planes)
    want = [(Fraction(4), Fraction(2)), (Fraction(4), Fraction(3)), (Fraction(3), Fraction(4)), (Fraction(1), Fraction(4)), (Fraction(7, 2), Fraction(3, 2))]
    assert got == want
    assert same_polygon(got, brute(planes))
    # the input order does not matter
    assert same_polygon(half_plane_intersection(planes[::-1]), want)


def test_degenerate() -> None:
    assert half_plane_intersection([]) == []
    sq = [(Fraction(0), Fraction(0)), (Fraction(2), Fraction(0)), (Fraction(2), Fraction(2)), (Fraction(0), Fraction(2))]
    assert same_polygon(half_plane_intersection(box(0, 2)), sq)
    # duplicates and parallel copies do not change the result
    assert same_polygon(half_plane_intersection(box(0, 2) * 3 + box(-1, 3)), sq)
    # empty: two opposite half-planes that do not overlap
    assert half_plane_intersection(box(0, 2) + [((0, 1), (-1, 0)), ((0, 3), (1, 0))]) == []
    # zero area: the region is a segment or a point
    assert half_plane_intersection(box(0, 2) + [((0, 1), (-1, 0)), ((0, 1), (1, 0))]) == []
    assert half_plane_intersection(box(0, 2) + [((0, 0), (-1, 1))]) == []
    assert half_plane_intersection(box(0, 2) + [((2, 0), (-1, 1)), ((0, 2), (1, -1)), ((0, 0), (1, 1))]) == []
    # many lines through one point
    star = box(-3, 3) + [((0, 0), (1, k)) for k in range(-2, 3)]
    assert same_polygon(half_plane_intersection(star), brute(star))


def test_random_against_brute_force() -> None:
    rng = random.Random(2003)
    for _ in range(1200):
        r = rng.choice([1, 2, 3, 6])
        b = rng.randint(2, 8)
        planes = box(-b, b)
        for _ in range(rng.randint(0, 9)):
            p = (rng.randint(-r, r), rng.randint(-r, r))
            d = (0, 0)
            while d == (0, 0):
                d = (rng.randint(-2, 2), rng.randint(-2, 2))
            planes.append((p, d))
            if rng.random() < 0.2:
                planes.append(((p[0] + rng.randint(-1, 1), p[1]), (-d[0], -d[1])))
        rng.shuffle(planes)
        assert same_polygon(half_plane_intersection(planes), brute(planes)), planes
