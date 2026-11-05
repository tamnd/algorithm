# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nn-descent/. The authors are listed in prov/264YR6.jsonl.

import math
import random

from nn_descent import nn_descent

P = [(0, 0), (1, 0), (2, 1), (6, 0), (7, 1), (6, 2), (1, 5), (2, 6)]
INIT = [[3, 6], [4, 7], [5, 0], [0, 6], [1, 7], [2, 3], [3, 4], [5, 1]]


def exact(points, k):
    return [sorted((math.dist(points[v], points[u]), u) for u in range(len(points)) if u != v)[:k]
            for v in range(len(points))]


def test_example() -> None:
    stats: dict = {}
    assert nn_descent(P, 2, init=INIT, stats=stats) == exact(P, 2)
    assert stats == {"evaluations": 68, "rounds": 3}


def test_edges() -> None:
    assert nn_descent([], 0) == []
    assert nn_descent([(0, 0)], 0) == [[]]
    pts = [(0, 0), (3, 4), (1, 1)]
    assert nn_descent(pts, 2, seed=5) == exact(pts, 2)
    try:
        nn_descent(pts, 3)
        raise AssertionError("k = n accepted")
    except ValueError:
        pass


def check_lists(points, k, lists):
    for v, lst in enumerate(lists):
        assert len(lst) == k and len({u for _, u in lst}) == k and all(u != v for _, u in lst)
        assert all(dd == math.dist(points[v], points[u]) for dd, u in lst)
        assert lst == sorted(lst)


def test_random_fixpoint_without_sampling() -> None:
    rng = random.Random(2011)
    for _ in range(500):
        n = rng.randint(2, 30)
        k = rng.randint(1, min(5, n - 1))
        pts = [tuple(rng.uniform(0, 10) for _ in range(rng.choice((1, 2, 3)))) for _ in range(1)]
        dim = len(pts[0])
        pts = [tuple(rng.uniform(0, 10) for _ in range(dim)) for _ in range(n)]
        lists = nn_descent(pts, k, seed=rng.randrange(10**6))
        check_lists(pts, k, lists)
        fwd = [{u for _, u in lst} for lst in lists]
        nbar = [set(f) for f in fwd]
        for v in range(n):
            for u in fwd[v]:
                nbar[u].add(v)
        for v in range(n):
            worst = lists[v][-1]
            for u in nbar[v]:
                for w in nbar[u]:
                    if w != v and w not in fwd[v]:
                        assert (math.dist(pts[v], pts[w]), w) >= worst
        if k == n - 1:
            assert lists == exact(pts, k)


def test_random_with_sampling() -> None:
    rng = random.Random(577)
    for _ in range(500):
        n = rng.randint(2, 40)
        k = rng.randint(1, min(6, n - 1))
        pts = [tuple(rng.uniform(0, 10) for _ in range(2)) for _ in range(n)]
        init = [rng.sample([u for u in range(n) if u != v], k) for v in range(n)]
        lists = nn_descent(pts, k, rho=rng.choice((0.3, 0.5, 1.0)), delta=rng.choice((0.0, 0.001, 0.05)),
                           seed=rng.randrange(10**6), init=init)
        check_lists(pts, k, lists)
        truth = exact(pts, k)
        for v in range(n):
            start = sorted(math.dist(pts[v], pts[u]) for u in init[v])
            got = [dd for dd, _ in lists[v]]
            assert all(t[0] <= g <= s for t, g, s in zip(truth[v], got, start))
