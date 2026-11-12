# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dunn-index/. The authors are listed in prov/PBD47N.jsonl.

import itertools
import random
from fractions import Fraction
from math import inf, isclose, sqrt

from dunn_index import dunn, gap_and_diameter

POINTS = [(0, 0), (2, 0), (1, 3), (8, 0), (10, 0), (9, 3), (4, 8), (6, 8), (5, 11)]
GOOD = [0, 0, 0, 1, 1, 1, 2, 2, 2]
MERGED = [0, 0, 0, 0, 0, 0, 1, 1, 1]


def absd(x, y):
    return abs(Fraction(x) - Fraction(y))


def test_example() -> None:
    # Diameter of each cluster: sqrt(10). Least gap: from (1,3) to (4,8), sqrt(34),
    # which is less than the gap 6 from (2,0) to (8,0).
    assert gap_and_diameter(POINTS, GOOD) == (sqrt(34), sqrt(10))
    assert isclose(dunn(POINTS, GOOD), sqrt(3.4))
    # Merged: the gap is from (1,3) to (4,8), sqrt 34; the diameter is from (0,0) to (10,0), 10.
    assert isclose(dunn(POINTS, MERGED), sqrt(34) / 10)


def test_one_outlier_changes_the_index() -> None:
    xs = [0, 1, 2, 10, 11, 12]
    lab = [0, 0, 0, 1, 1, 1]
    assert dunn(xs, lab, absd) == 4
    # Move one point of the second cluster far away: the diameter grows from 2 to 30.
    assert dunn([0, 1, 2, 10, 11, 40], lab, absd) == Fraction(8, 30)
    # One point between the clusters, in the first cluster: the gap drops from 8 to 4.
    assert dunn([0, 1, 6, 10, 11, 12], lab, absd) == Fraction(4, 6)


def test_greater_than_one_means_compact_and_separated() -> None:
    # D > 1 exactly when every distance inside a cluster is smaller than every distance between clusters.
    rng = random.Random(12)
    for _ in range(300):
        n = rng.randrange(3, 9)
        xs = [rng.randrange(30) for _ in range(n)]
        lab = [rng.randrange(2) for _ in range(n)]
        if len(set(lab)) < 2:
            continue
        inside = [abs(xs[i] - xs[j]) for i, j in itertools.combinations(range(n), 2) if lab[i] == lab[j]]
        between = [abs(xs[i] - xs[j]) for i, j in itertools.combinations(range(n), 2) if lab[i] != lab[j]]
        cws = all(a < b for a in inside for b in between)
        assert (dunn(xs, lab, absd) > 1) == cws


def test_degenerate() -> None:
    assert dunn([0, 0, 5, 5], [0, 0, 1, 1], absd) == inf
