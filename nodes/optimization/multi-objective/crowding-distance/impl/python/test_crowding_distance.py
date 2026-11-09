# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crowding-distance/. The authors are listed in prov/KB59FK.jsonl.

import math
import random
from fractions import Fraction as Fr

from crowding_distance import crowding_distance, truncate


def exact(points):
    return [tuple(Fr(v) for v in p) for p in points]


def test_example() -> None:
    d = crowding_distance(exact([(1, 8), (2, 5), (4, 2), (7, 1)]))
    assert d == [math.inf, Fr(19, 14), Fr(59, 42), math.inf]


def test_edges() -> None:
    assert crowding_distance([]) == []
    assert crowding_distance([(1, 2)]) == [math.inf]
    assert crowding_distance([(1, 2), (2, 1)]) == [math.inf, math.inf]
    # all equal in one objective: that objective adds nothing
    assert crowding_distance(exact([(0, 0), (0, 1), (0, 2)])) == [math.inf, 1, math.inf]


def test_copies_are_not_zero() -> None:
    d = crowding_distance(exact([(0, 4), (1, 3), (1, 3), (4, 0)]))
    assert d == [math.inf, 1, 1, math.inf]
    assert crowding_distance(exact([(0, 4), (1, 3), (4, 0)]))[1] == 2


def test_two_objectives_half_perimeter() -> None:
    """For p = 2 on a front with distinct points, d is the normalized half perimeter of the neighbor box."""
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(3, 9)
        xs = sorted(rng.sample(range(50), n))
        ys = sorted(rng.sample(range(50), n), reverse=True)
        front = exact(list(zip(xs, ys)))
        rng.shuffle(front)
        d = crowding_distance(front)
        order = sorted(range(n), key=lambda i: front[i][0])
        r1 = front[order[-1]][0] - front[order[0]][0]
        r2 = front[order[0]][1] - front[order[-1]][1]
        for k in range(1, n - 1):
            a, b = front[order[k - 1]], front[order[k + 1]]
            assert d[order[k]] == (b[0] - a[0]) / r1 + (a[1] - b[1]) / r2
        assert d[order[0]] == d[order[-1]] == math.inf


def test_truncate() -> None:
    front = [(0, 10), (1, 8), (5, 7), (6, 6), (8, 3), (10, 0)]
    assert crowding_distance(exact(front))[1:5] == [Fr(4, 5), Fr(7, 10), Fr(7, 10), 1]
    assert truncate(exact(front), 4) == [0, 1, 4, 5]
    assert truncate(exact(front), 4, recompute=True) == [0, 2, 4, 5]
    rng = random.Random(9)
    for _ in range(100):
        n = rng.randint(3, 10)
        xs = sorted(rng.sample(range(40), n))
        ys = sorted(rng.sample(range(40), n), reverse=True)
        f = exact(list(zip(xs, ys)))
        for keep in range(2, n + 1):
            for rec in (False, True):
                kept = truncate(f, keep, rec)
                assert len(kept) == keep
                # the two extreme points have infinite distance and stay
                assert 0 in kept and n - 1 in kept
