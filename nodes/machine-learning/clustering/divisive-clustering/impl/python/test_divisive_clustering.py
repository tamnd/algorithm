# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divisive-clustering/. The authors are listed in prov/9ERGNS.jsonl.

import random
from fractions import Fraction

from divisive_clustering import diameter, divisive_clustering, splinter, splits_to_merges


def line(xs):
    return [[abs(a - b) for b in xs] for a in xs]


def mean(vals):
    vals = list(vals)
    return Fraction(sum(vals), len(vals))


def check_splinter(D, c, s, r):
    """The splinter rule, checked from its definition with fresh sums."""
    assert sorted(s + r) == sorted(c) and s and r
    if len(r) >= 2:
        for i in r:
            assert mean(D[i][j] for j in r if j != i) - mean(D[i][h] for h in s) <= 0


def test_worked_example():
    D = line([0, 2, 3, 7, 13, 21])
    assert divisive_clustering(D) == [
        ((4, 5), (0, 1, 2, 3), 21),
        ((4,), (5,), 8),
        ((3,), (0, 1, 2), 7),
        ((0,), (1, 2), 3),
        ((1,), (2,), 1),
    ]


def test_edges():
    assert divisive_clustering([]) == []
    assert divisive_clustering([[0]]) == []
    assert divisive_clustering([[0, 4], [4, 0]]) == [((0,), (1,), 4)]
    assert splinter([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [0, 1, 2]) == ([0], [1, 2])
    # duplicate points: a cluster of diameter 0 with two points must still be split
    splits = divisive_clustering(line([0, 5, 5]))
    assert [h for _, _, h in splits] == [5, 0]
    assert splits[1] == ((1,), (2,), 0)


def test_properties_on_random_inputs():
    rng = random.Random(19)
    for _ in range(500):
        n = rng.randrange(1, 9)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randrange(1, 20)
        splits = divisive_clustering(D)
        assert len(splits) == max(n - 1, 0)
        live = [tuple(range(n))] if n else []
        last = None
        for s, r, h in splits:
            c = tuple(sorted(s + r))
            assert c in live
            assert h == diameter(D, c) == max(diameter(D, x) for x in live)
            check_splinter(D, list(c), list(s), list(r))
            assert last is None or h <= last
            last = h
            live.remove(c)
            live += [s, r]
        assert all(len(x) == 1 for x in live)
        merges = splits_to_merges(n, splits)
        hs = [h for _, _, h, _ in merges]
        assert hs == sorted(hs)
        if merges:
            assert merges[-1][3] == n


def test_first_splinter_point():
    rng = random.Random(2)
    for _ in range(300):
        m = rng.randrange(2, 8)
        D = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                D[i][j] = D[j][i] = rng.randrange(1, 30)
        c = list(range(m))
        s, _ = splinter(D, c)
        top = max(mean(D[i][j] for j in c if j != i) for i in c)
        assert any(mean(D[i][j] for j in c if j != i) == top for i in s)
