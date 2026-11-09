# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bentley-ottmann-algorithm/. The authors are listed in prov/G9R6WH.jsonl.

import random
from fractions import Fraction

from bentley_ottmann_algorithm import bentley_ottmann

F = Fraction
P = tuple[Fraction, Fraction]


def fp(p: tuple) -> P:
    return (F(p[0]), F(p[1]))


def on_seg(a: P, b: P, p: P) -> bool:
    """Is p = a + t (b - a) with 0 <= t <= 1? No orientation test is used."""
    if a == b:
        return p == a
    t = (p[0] - a[0]) / (b[0] - a[0]) if a[0] != b[0] else (p[1] - a[1]) / (b[1] - a[1])
    return 0 <= t <= 1 and a[0] + t * (b[0] - a[0]) == p[0] and a[1] + t * (b[1] - a[1]) == p[1]


def pair_common(a: P, b: P, c: P, d: P) -> list[P]:
    """The extreme points of the common part of two segments, by checking all candidates."""
    cand = [a, b, c, d]
    a1, b1 = b[1] - a[1], a[0] - b[0]
    a2, b2 = d[1] - c[1], c[0] - d[0]
    det = a1 * b2 - a2 * b1
    if det != 0:
        c1, c2 = a1 * a[0] + b1 * a[1], a2 * c[0] + b2 * c[1]
        cand.append(((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det))
    good = sorted({p for p in cand if on_seg(a, b, p) and on_seg(c, d, p)})
    return [good[0], good[-1]] if good else []


def brute(segs: list) -> dict:
    """Every end point on two or more segments, and every single common point of a pair."""
    s = [(fp(a), fp(b)) for a, b in segs]
    pts = set()
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            c = pair_common(*s[i], *s[j])
            if c and c[0] == c[1]:
                pts.add(c[0])
    for a, b in s:
        for e in (a, b):
            if sum(on_seg(u, v, e) for u, v in s) >= 2:
                pts.add(e)
    return {p: {i for i, (u, v) in enumerate(s) if on_seg(u, v, p)} for p in pts}


def random_segments(rng: random.Random, n: int, r: int) -> list:
    segs = []
    for _ in range(n):
        kind = rng.random()
        a = (rng.randint(0, r), rng.randint(0, r))
        if kind < 0.15:
            b = (a[0], rng.randint(0, r))
        elif kind < 0.3:
            b = (rng.randint(0, r), a[1])
        elif kind < 0.35:
            b = a
        elif kind < 0.45 and segs:
            b = rng.choice(segs)[rng.randint(0, 1)]
        elif kind < 0.55:
            d = rng.choice([(1, 1), (1, -1), (2, 1)])
            k = rng.randint(-2, 2)
            b = (a[0] + k * d[0], a[1] + k * d[1])  # many collinear segments on few lines
        else:
            b = (rng.randint(0, r), rng.randint(0, r))
        segs.append((a, b))
    return segs


def test_example() -> None:
    segs = [((0, 0), (6, 6)), ((0, 6), (6, 0)), ((0, 3), (6, 3)), ((1, 0), (5, 4)), ((4, 0), (4, 6))]
    got = bentley_ottmann(segs)
    assert got == brute(segs)
    assert got[(F(3), F(3))] == {0, 1, 2}
    assert got[(F(4), F(3))] == {2, 3, 4}
    assert got[(F(4), F(4))] == {0, 4}
    assert got[(F(4), F(2))] == {1, 4}
    assert got[(F(7, 2), F(5, 2))] == {1, 3}
    assert len(got) == 5


def test_small_and_degenerate() -> None:
    assert bentley_ottmann([]) == {}
    assert bentley_ottmann([((0, 0), (1, 1))]) == {}
    assert bentley_ottmann([((2, 2), (2, 2)), ((2, 2), (2, 2))]) == {(F(2), F(2)): {0, 1}}
    # a proper crossing at a non-integer point
    assert bentley_ottmann([((0, 0), (3, 1)), ((0, 1), (3, 0))]) == {(F(3, 2), F(1, 2)): {0, 1}}
    # a collinear overlap is reported at the end points of the overlap
    assert bentley_ottmann([((0, 0), (4, 4)), ((2, 2), (6, 6))]) == {(F(2), F(2)): {0, 1}, (F(4), F(4)): {0, 1}}
    # vertical segments: overlap, and a crossing with a horizontal one
    assert bentley_ottmann([((1, 0), (1, 5)), ((1, 3), (1, 9)), ((0, 4), (2, 4))]) == {
        (F(1), F(3)): {0, 1},
        (F(1), F(4)): {0, 1, 2},
        (F(1), F(5)): {0, 1},
    }
    # many segments through one point
    star = [((-k, -1), (k, 1)) for k in range(1, 5)] + [((0, -3), (0, 3))]
    assert bentley_ottmann(star) == {(F(0), F(0)): {0, 1, 2, 3, 4}}


def test_grid_of_lines() -> None:
    # m horizontal and m vertical segments: m^2 crossings, plus some shared end points
    m = 6
    segs = [((0, i), (m - 1, i)) for i in range(m)] + [((i, 0), (i, m - 1)) for i in range(m)]
    got = bentley_ottmann(segs)
    assert len(got) == m * m
    assert got == brute(segs)


def test_random_against_brute_force() -> None:
    rng = random.Random(1979)
    for _ in range(900):
        r = rng.choice([2, 3, 4, 6, 15])
        segs = random_segments(rng, rng.randint(0, 9), r)
        assert bentley_ottmann(segs) == brute(segs), segs


def test_random_general_lines() -> None:
    rng = random.Random(643)
    for _ in range(60):
        segs = [((rng.randint(-50, 50), rng.randint(-50, 50)), (rng.randint(-50, 50), rng.randint(-50, 50))) for _ in range(12)]
        assert bentley_ottmann(segs) == brute(segs)
