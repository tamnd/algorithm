# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hartigan-wong-algorithm/. The authors are listed in prov/RNKKMZ.jsonl.

import itertools
import random
from fractions import Fraction as F

from hartigan_wong_algorithm import centroid, hartigan, nearest_labels, partition_cost, sq_dist


def pts(*ps):
    return [tuple(F(v) for v in p) for p in ps]


def optimum(points, k):
    best = None
    for lab in itertools.product(range(k), repeat=len(points)):
        if len(set(lab)) == k:
            c = partition_cost(points, lab, k)
            best = c if best is None or c < best else best
    return best


def replay_check(points, start, k, moves):
    """Each logged move lowers the cost by exactly the logged amount."""
    labels = list(start)
    cost = partition_cost(points, labels, k)
    for i, p, q, delta in moves:
        assert labels[i] == p and p != q
        assert delta < 0
        labels[i] = q
        new = partition_cost(points, labels, k)
        assert new - cost == delta
        cost = new
    return labels


def test_rectangle_escapes_lloyd_fixed_point() -> None:
    x = pts((0, 0), (0, 1), (2, 0), (2, 1))
    start = [0, 1, 0, 1]  # bottom and top: a fixed point of Lloyd's algorithm, cost 4
    assert partition_cost(x, start, 2) == 4
    labels, centers, moves = hartigan(x, start, 2)
    assert moves[0] == (0, 0, 1, F(-2, 3))
    assert partition_cost(x, labels, 2) == 1
    assert replay_check(x, start, 2, moves) == labels


def test_no_escape_when_wide_gap_is_small() -> None:
    # for w^2 < 2 the bottom and top split is optimal and Hartigan stays there
    x = [(F(0), F(0)), (F(0), F(1)), (F(1), F(0)), (F(1), F(1))]
    labels, _, moves = hartigan(x, [0, 1, 0, 1], 2)
    assert moves == [] and labels == [0, 1, 0, 1]


def test_moves_match_recomputed_cost_and_stability() -> None:
    rng = random.Random(4)
    for _ in range(150):
        n = rng.randrange(2, 10)
        d = rng.randrange(1, 3)
        k = rng.randrange(1, min(n, 4) + 1)
        x = [tuple(F(rng.randrange(-8, 9)) for _ in range(d)) for _ in range(n)]
        start = list(range(k)) + [rng.randrange(k) for _ in range(n - k)]
        rng.shuffle(start)
        labels, centers, moves = hartigan(x, start, k)
        assert replay_check(x, start, k, moves) == labels
        size = [labels.count(j) for j in range(k)]
        for j in range(k):
            if size[j]:
                assert centers[j] == centroid([p for p, a in zip(x, labels) if a == j])
        for p, a in zip(x, labels):
            # Hartigan stable: no single move lowers the cost
            if size[a] > 1:
                remove = size[a] * sq_dist(p, centers[a]) / (size[a] - 1)
                for j in range(k):
                    if j != a:
                        add = 0 if size[j] == 0 else size[j] * sq_dist(p, centers[j]) / (size[j] + 1)
                        assert add >= remove
            # hence a fixed point of Lloyd's algorithm: each point is at a nearest center
            assert sq_dist(p, centers[a]) == min(sq_dist(p, c) for c in centers if c is not None)
        if n <= 7 and k <= 3 and len(set(labels)) == k:
            assert partition_cost(x, labels, k) >= optimum(x, k)


def test_from_nearest_centers_and_floats() -> None:
    rng = random.Random(8)
    x = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(200)]
    init = nearest_labels(x, x[:4])
    labels, centers, moves = hartigan(x, init, 4)
    assert partition_cost(x, labels, 4) <= partition_cost(x, init, 4)
    assert all(delta < 0 for *_, delta in moves)


def test_single_point_clusters_never_empty() -> None:
    x = pts((0,), (10,), (11,), (12,))
    labels, _, moves = hartigan(x, [0, 1, 1, 1], 2)
    assert labels == [0, 1, 1, 1] and moves == []
