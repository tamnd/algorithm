# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bisecting-k-means/. The authors are listed in prov/4FMVJH.jsonl.

import random
from fractions import Fraction as F

from bisecting_k_means import bisecting_k_means, centroid, sq_dist, sse, two_means


def pts(*xs):
    return [tuple(F(v) for v in (x if isinstance(x, tuple) else (x,))) for x in xs]


def test_example_rules_differ() -> None:
    # a big tight group, and two small groups far apart
    x = pts(0, 1, 2, 3, 4, 5, 100, 101, 200, 201)
    for seed in range(5):
        clusters, log = bisecting_k_means(x, 3, random.Random(seed), rule="sse")
        assert sorted(sorted(c) for c in clusters) == [[0, 1, 2, 3, 4, 5], [6, 7], [8, 9]]
    # rule "largest": after the first split the six close points form the largest
    # cluster and get split, although the far pair {100, 101, 200, 201} has a larger SSE
    clusters, log = bisecting_k_means(x, 3, random.Random(0), rule="largest")
    assert sorted(sorted(c) for c in clusters) == [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]


def test_partition_and_monotone_sse() -> None:
    rng = random.Random(21)
    for _ in range(60):
        n = rng.randrange(1, 25)
        x = [(F(rng.randrange(-10, 11)), F(rng.randrange(-10, 11))) for _ in range(n)]
        k = rng.randrange(1, n + 1)
        rule = rng.choice(["sse", "largest"])
        clusters, log = bisecting_k_means(x, k, rng, rule=rule, trials=3)
        assert sorted(i for c in clusters for i in c) == list(range(n))
        assert all(clusters)
        distinct = len(set(x))
        assert len(clusters) == min(k, distinct) or len(clusters) == k
        prev = sse(x, list(range(n)))
        for j, parent, total in log:
            assert total <= prev  # a split never raises the total SSE
            prev = total


def test_sse_rule_picks_largest_sse() -> None:
    rng = random.Random(2)
    for _ in range(20):
        x = [(F(rng.randrange(0, 30)), F(rng.randrange(0, 30))) for _ in range(12)]
        seed = rng.randrange(10**6)
        for rule, key in (("sse", lambda c: sse(x, c)), ("largest", len)):
            # a run with k = m stops exactly where the run with k = m + 1 makes its m-th split
            _, log = bisecting_k_means(x, 5, random.Random(seed), rule=rule)
            for m in range(1, len(log) + 1):
                state, _ = bisecting_k_means(x, m, random.Random(seed), rule=rule)
                j = log[m - 1][0]
                assert key(state[j]) == max(key(c) for c in state)
                assert log[m - 1][1] == sse(x, state[j])


def test_two_means_is_lloyd_fixed_point() -> None:
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randrange(2, 15)
        x = [(F(rng.randrange(-6, 7)), F(rng.randrange(-6, 7))) for _ in range(n)]
        idx = list(range(n))
        res = two_means(x, idx, rng)
        if len(set(x)) < 2:
            assert res is None
            continue
        left, right = res
        cl, cr = centroid([x[i] for i in left]), centroid([x[i] for i in right])
        for i in left:
            assert sq_dist(x[i], cl) <= sq_dist(x[i], cr)
        for i in right:
            assert sq_dist(x[i], cr) <= sq_dist(x[i], cl)


def test_identical_points_cannot_split() -> None:
    x = pts(7, 7, 7, 9)
    clusters, log = bisecting_k_means(x, 4, random.Random(1))
    assert sorted(sorted(c) for c in clusters) == [[0, 1, 2], [3]]
