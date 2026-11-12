# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-means-problem/. The authors are listed in prov/2GYFP1.jsonl.

import random
from fractions import Fraction as F

from k_means_problem import (
    brute_force,
    centroid,
    cost,
    optimal_1d,
    partition_cost,
    set_partitions,
    sq_dist,
)


def stirling2(n: int, k: int) -> int:
    s = [[0] * (k + 1) for _ in range(n + 1)]
    s[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            s[i][j] = j * s[i - 1][j] + s[i - 1][j - 1]
    return s[n][k]


def test_set_partitions_count() -> None:
    for n in range(1, 8):
        for k in range(1, n + 1):
            seen = {tuple(p) for p in set_partitions(n, k)}
            assert len(seen) == stirling2(n, k)
            assert all(max(p) == k - 1 for p in seen)


def test_centroid_identity() -> None:
    rng = random.Random(1)
    for _ in range(200):
        d = rng.randrange(1, 4)
        pts = [tuple(F(rng.randrange(-9, 10)) for _ in range(d)) for _ in range(rng.randrange(1, 7))]
        c = tuple(F(rng.randrange(-9, 10), rng.randrange(1, 4)) for _ in range(d))
        m = centroid(pts)
        lhs = sum(sq_dist(x, c) for x in pts)
        rhs = sum(sq_dist(x, m) for x in pts) + len(pts) * sq_dist(m, c)
        assert lhs == rhs
        assert lhs >= sum(sq_dist(x, m) for x in pts)


def test_partition_cost_is_min_over_centers() -> None:
    pts = [(F(0), F(0)), (F(2), F(0)), (F(9), F(1)), (F(10), F(3))]
    clusters = [pts[:2], pts[2:]]
    centers = [centroid(c) for c in clusters]
    assert partition_cost(clusters) == cost(pts, centers) == F(1 * 2) + F(5, 2)


def test_example_1d() -> None:
    xs = [F(v) for v in (1, 2, 4, 7, 8, 13)]
    c2, cl2 = optimal_1d(xs, 2)
    c3, cl3 = optimal_1d(xs, 3)
    assert (c2, cl2) == (F(76, 3), [[1, 2, 4], [7, 8, 13]])
    assert (c3, cl3) == (F(31, 6), [[1, 2, 4], [7, 8], [13]])
    assert optimal_1d(xs, 4)[0] == 1
    assert optimal_1d(xs, 6)[0] == 0
    assert optimal_1d(xs, 1)[0] == partition_cost([[(x,) for x in xs]])


def test_dp_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randrange(1, 8)
        xs = [F(rng.randrange(-20, 21)) for _ in range(n)]
        k = rng.randrange(1, n + 1)
        best, _ = brute_force([(x,) for x in xs], k)
        got, clusters = optimal_1d(xs, k)
        assert got == best
        assert len(clusters) == k and all(clusters)
        assert sorted(v for c in clusters for v in c) == sorted(xs)
        assert partition_cost([[(v,) for v in c] for c in clusters]) == got


def test_brute_force_2d_small() -> None:
    pts = [(F(0), F(0)), (F(0), F(1)), (F(4), F(0)), (F(4), F(1))]
    best, labels = brute_force(pts, 2)
    assert best == 1
    assert labels == [0, 0, 1, 1]
