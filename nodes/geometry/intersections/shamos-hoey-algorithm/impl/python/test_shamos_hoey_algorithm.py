# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shamos-hoey-algorithm/. The authors are listed in prov/5XWJY8.jsonl.

import random
from fractions import Fraction

from shamos_hoey_algorithm import shamos_hoey

F = Fraction
P = tuple[Fraction, Fraction]


def on_seg(a: P, b: P, p: P) -> bool:
    """Is p = a + t (b - a) with 0 <= t <= 1? No orientation test is used."""
    if a == b:
        return p == a
    t = (p[0] - a[0]) / (b[0] - a[0]) if a[0] != b[0] else (p[1] - a[1]) / (b[1] - a[1])
    return 0 <= t <= 1 and a[0] + t * (b[0] - a[0]) == p[0] and a[1] + t * (b[1] - a[1]) == p[1]


def meet(s: tuple, t: tuple) -> bool:
    """Brute-force test: the common part is convex, so it contains an end point or the meet of the lines."""
    a, b = [(F(x), F(y)) for x, y in s]
    c, d = [(F(x), F(y)) for x, y in t]
    cand = [a, b, c, d]
    a1, b1 = b[1] - a[1], a[0] - b[0]
    a2, b2 = d[1] - c[1], c[0] - d[0]
    det = a1 * b2 - a2 * b1
    if det != 0:
        c1, c2 = a1 * a[0] + b1 * a[1], a2 * c[0] + b2 * c[1]
        cand.append(((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det))
    return any(on_seg(a, b, p) and on_seg(c, d, p) for p in cand)


def brute_any(segs: list) -> bool:
    return any(meet(segs[i], segs[j]) for i in range(len(segs)) for j in range(i + 1, len(segs)))


def check(segs: list) -> None:
    got = shamos_hoey(segs)
    if got is None:
        assert not brute_any(segs), segs
    else:
        i, j = got
        assert 0 <= i < j < len(segs) and meet(segs[i], segs[j]), (segs, got)


def random_segments(rng: random.Random, n: int, r: int) -> list:
    segs = []
    for _ in range(n):
        kind = rng.random()
        a = (rng.randint(0, r), rng.randint(0, r))
        if kind < 0.15:
            b = (a[0], rng.randint(0, r))  # vertical
        elif kind < 0.3:
            b = (rng.randint(0, r), a[1])  # horizontal
        elif kind < 0.35:
            b = a  # a single point
        elif kind < 0.45 and segs:
            b = rng.choice(segs)[rng.randint(0, 1)]  # share an end point
        else:
            b = (rng.randint(0, r), rng.randint(0, r))
        segs.append((a, b))
    return segs


def test_example() -> None:
    segs = [((0, 0), (6, 2)), ((1, 4), (7, 5)), ((2, 3), (5, 0)), ((3, 6), (8, 3))]
    assert shamos_hoey(segs) == (0, 2)
    disjoint = [((0, 0), (6, 2)), ((1, 4), (7, 5)), ((2, 3), (5, 2)), ((8, 0), (8, 6))]
    assert shamos_hoey(disjoint) is None


def test_small_and_degenerate() -> None:
    assert shamos_hoey([]) is None
    assert shamos_hoey([((0, 0), (1, 1))]) is None
    assert shamos_hoey([((0, 0), (0, 0))]) is None
    assert shamos_hoey([((0, 0), (0, 0)), ((0, 0), (0, 0))]) == (0, 1)
    # shared end point, T-junction, collinear overlap, collinear and disjoint
    assert shamos_hoey([((0, 0), (1, 1)), ((1, 1), (2, 0))]) == (0, 1)
    assert shamos_hoey([((0, 0), (4, 0)), ((2, 0), (2, 3))]) == (0, 1)
    assert shamos_hoey([((0, 0), (4, 4)), ((2, 2), (6, 6))]) == (0, 1)
    assert shamos_hoey([((0, 0), (1, 1)), ((2, 2), (3, 3))]) is None
    # vertical segments: a crossing, an overlap, a point on a vertical segment
    assert shamos_hoey([((1, -1), (1, 1)), ((0, 0), (2, 0))]) == (0, 1)
    assert shamos_hoey([((1, 0), (1, 5)), ((1, 3), (1, 9))]) == (0, 1)
    assert shamos_hoey([((1, 0), (1, 5)), ((1, 2), (1, 2))]) == (0, 1)
    assert shamos_hoey([((1, 0), (1, 2)), ((1, 3), (1, 5)), ((0, 9), (5, 9))]) is None
    # a vertical segment that touches a long segment from below at its top end point
    assert shamos_hoey([((0, 0), (4, 4)), ((2, -3), (2, 2))]) == (0, 1)
    # the leftmost crossing is far to the right of many disjoint segments
    segs = [((0, 2 * i), (10, 2 * i)) for i in range(5)] + [((11, 0), (12, 9)), ((11, 9), (12, 0))]
    assert shamos_hoey(segs) == (5, 6)


def test_fractions_and_large_ints() -> None:
    assert shamos_hoey([((F(0), F(0)), (F(1), F(1, 3))), ((F(1, 2), F(0)), (F(1, 2), F(1)))]) == (0, 1)
    big = 10**18
    assert shamos_hoey([((0, 0), (big, big + 1)), ((1, 0), (big + 1, big + 1))]) is None


def test_random_against_brute_force() -> None:
    rng = random.Random(51976)
    for _ in range(1500):
        r = rng.choice([2, 3, 4, 6, 20])
        n = rng.randint(0, 9)
        check(random_segments(rng, n, r))


def test_random_disjoint_families() -> None:
    # disjoint inputs force the full sweep; build them by rejection
    rng = random.Random(7)
    built = 0
    while built < 400:
        r = rng.choice([4, 6, 10])
        segs: list = []
        for _ in range(rng.randint(1, 12)):
            cand = random_segments(rng, 1, r)[0]
            if not any(meet(cand, t) for t in segs):
                segs.append(cand)
        assert shamos_hoey(segs) is None
        if len(segs) >= 2:
            x = rng.choice(segs)
            check(segs + [x])  # a duplicate segment
        built += 1
