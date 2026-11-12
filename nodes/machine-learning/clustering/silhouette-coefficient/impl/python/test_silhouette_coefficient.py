# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/silhouette-coefficient/. The authors are listed in prov/9J34RM.jsonl.

import random
from fractions import Fraction
from math import isclose

from silhouette_coefficient import cluster_silhouettes, mean_silhouette, silhouette_samples

POINTS = [(0, 0), (2, 0), (1, 3), (8, 0), (10, 0), (9, 3), (4, 8), (6, 8), (5, 11)]
GOOD = [0, 0, 0, 1, 1, 1, 2, 2, 2]
MERGED = [0, 0, 0, 0, 0, 0, 1, 1, 1]


def absd(x, y):
    return abs(Fraction(x) - Fraction(y))


def test_one_dimensional_exact() -> None:
    # Points 0, 1, 2 | 6, 7 on a line. For the point 0: a = (1 + 2)/2 = 3/2,
    # b = (6 + 7)/2 = 13/2, s = (13/2 - 3/2) / (13/2) = 10/13.
    s = silhouette_samples([0, 1, 2, 6, 7], [0, 0, 0, 1, 1], absd)
    assert s[0] == Fraction(10, 13)
    assert s == [Fraction(10, 13), Fraction(9, 11), Fraction(2, 3), Fraction(4, 5), Fraction(5, 6)]


def test_singleton_is_zero_and_bad_point_is_negative() -> None:
    s = silhouette_samples([0, 1, 2, 6, 7, 20], [0, 0, 0, 1, 1, 2], absd)
    assert s[5] == 0
    # The point 2 put in the far cluster gets a negative silhouette.
    s = silhouette_samples([0, 1, 2, 6, 7], [0, 0, 1, 1, 1], absd)
    assert s[2] < 0


def test_two_dimensional_example() -> None:
    assert isclose(mean_silhouette(POINTS, GOOD), 0.65404, abs_tol=5e-6)
    assert isclose(mean_silhouette(POINTS, MERGED), 0.44030, abs_tol=5e-5)
    assert isclose(silhouette_samples(POINTS, GOOD)[0], 0.71826, abs_tol=5e-5)
    per = cluster_silhouettes(POINTS, GOOD)
    assert set(per) == {0, 1, 2}


def test_range_and_scale_invariance() -> None:
    rng = random.Random(8)
    for _ in range(100):
        n = rng.randrange(3, 15)
        pts = [(rng.randrange(20), rng.randrange(20)) for _ in range(n)]
        lab = [rng.randrange(3) for _ in range(n)]
        if len(set(lab)) < 2:
            continue
        s = silhouette_samples(pts, lab)
        assert all(-1 - 1e-12 <= x <= 1 + 1e-12 for x in s)
        scaled = [(3 * x + 5, 3 * y - 2) for x, y in pts]
        s2 = silhouette_samples(scaled, lab)
        assert all(isclose(x, y, abs_tol=1e-12) for x, y in zip(s, s2))


def test_all_singletons() -> None:
    assert silhouette_samples([0, 1, 2], [0, 1, 2], absd) == [0, 0, 0]
