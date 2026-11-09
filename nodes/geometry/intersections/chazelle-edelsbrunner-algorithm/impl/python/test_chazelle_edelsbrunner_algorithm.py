# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-edelsbrunner-algorithm/. The authors are listed in prov/VR6X2D.jsonl.

import math
import random
from fractions import Fraction

from chazelle_edelsbrunner_algorithm import Stats, intersecting_pairs


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def on_segment(p, a, b):
    return (cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def meet(s, t):
    (a, b), (c, d) = s, t
    d1, d2, d3, d4 = cross(c, d, a), cross(c, d, b), cross(a, b, c), cross(a, b, d)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return on_segment(a, c, d) or on_segment(b, c, d) or on_segment(c, a, b) or on_segment(d, a, b)


def brute(segs):
    return [(i, j) for i in range(len(segs)) for j in range(i + 1, len(segs)) if meet(segs[i], segs[j])]


EXAMPLE = [((0, 0), (8, 8)), ((1, 7), (9, 1)), ((2, 4), (10, 4)), ((3, 1), (7, 3))]


def test_example():
    st = Stats()
    assert intersecting_pairs(EXAMPLE, st) == [(0, 1), (0, 2), (1, 2), (1, 3)]
    assert st.reports == 4


def test_empty_and_single():
    assert intersecting_pairs([]) == []
    assert intersecting_pairs([((0, 0), (1, 1))]) == []
    assert intersecting_pairs([((2, 2), (2, 2)), ((2, 2), (2, 2))]) == [(0, 1)]


def test_degenerate_cases():
    segs = [
        ((0, 0), (4, 0)),   # 0 horizontal
        ((2, 0), (6, 0)),   # 1 collinear overlap with 0
        ((4, 0), (4, 3)),   # 2 vertical, touches 0 at its end and crosses 1
        ((4, 3), (7, 3)),   # 3 shares an end point with 2
        ((5, 3), (5, 3)),   # 4 a point on 3
        ((6, 0), (8, 0)),   # 5 touches 1 end to end
        ((4, 1), (4, 2)),   # 6 vertical inside 2
        ((3, -1), (5, 1)),  # 7 crosses 0 and 1 at (4, 0) and meets 2 there
        ((9, 9), (9, 9)),   # 8 an isolated point
    ]
    assert intersecting_pairs(segs) == brute(segs)
    assert (0, 1) in brute(segs) and (2, 6) in brute(segs) and (3, 4) in brute(segs)


def test_all_through_one_point():
    segs = [((-k, -1), (k, 1)) for k in range(1, 8)] + [((0, -3), (0, 3)), ((0, 0), (0, 0))]
    n = len(segs)
    assert intersecting_pairs(segs) == [(i, j) for i in range(n) for j in range(i + 1, n)]


def test_grid_of_crossings():
    n = 12
    segs = [((0, 2 * i), (4 * n, 2 * i)) for i in range(n)] + [((2 * j + 1, -1), (2 * j + 1, 2 * n)) for j in range(n)]
    got = intersecting_pairs(segs)
    assert got == brute(segs) and len(got) == n * n


def random_segment(rng, r):
    a = (rng.randint(0, r), rng.randint(0, r))
    u = rng.random()
    if u < 0.1:
        return (a, a)
    if u < 0.25:
        return (a, (a[0], rng.randint(0, r)))
    if u < 0.35:
        return (a, (rng.randint(0, r), a[1]))
    return (a, (rng.randint(0, r), rng.randint(0, r)))


def test_random_degenerate_against_brute_force():
    rng = random.Random(20261109)
    for _ in range(1500):
        r = rng.choice([1, 2, 3, 6])
        segs = [random_segment(rng, r) for _ in range(rng.randint(0, 12))]
        if segs and rng.random() < 0.2:
            segs.append(rng.choice(segs))
        assert intersecting_pairs(segs) == brute(segs), segs


def test_random_fraction_coordinates():
    rng = random.Random(3)
    for _ in range(300):
        segs = []
        for _ in range(rng.randint(2, 9)):
            a = (Fraction(rng.randint(0, 8), rng.randint(1, 3)), Fraction(rng.randint(0, 8), rng.randint(1, 3)))
            b = (Fraction(rng.randint(0, 8), rng.randint(1, 3)), Fraction(rng.randint(0, 8), rng.randint(1, 3)))
            segs.append((a, b))
        assert intersecting_pairs(segs) == brute(segs)


def test_output_sensitive_work():
    rng = random.Random(11)
    for n in (64, 256):
        segs = []
        for _ in range(n):
            a = (rng.randint(0, 10**6), rng.randint(0, 10**6))
            b = (a[0] + rng.randint(-10**5, 10**5), a[1] + rng.randint(-10**5, 10**5))
            segs.append((a, b))
        st = Stats()
        k = len(intersecting_pairs(segs, st))
        assert st.reports <= 6 * k
        assert st.work <= 4 * (n * math.log2(n) ** 2 + k)
