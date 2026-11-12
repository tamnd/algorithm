# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-means/. The authors are listed in prov/MRP5YA.jsonl.

import random
from fractions import Fraction as F

from k_means import assignment_cost, centroid, lloyd, random_init, sq_dist


def pts(*ps):
    return [tuple(F(v) for v in p) for p in ps]


def partitions(n: int, k: int):
    """All labelings of n points with labels in 0..k-1 whose blocks are all non-empty."""
    labels = [0] * n
    while True:
        if len(set(labels)) == k:
            yield list(labels)
        i = n - 1
        while i >= 0 and labels[i] == k - 1:
            labels[i] = 0
            i -= 1
        if i < 0:
            return
        labels[i] += 1


def best_cost(points, k):
    best = None
    for lab in partitions(len(points), k):
        cs = [centroid([p for p, a in zip(points, lab) if a == j]) for j in range(k)]
        c = assignment_cost(points, cs, lab)
        best = c if best is None or c < best else best
    return best


def test_trace_example() -> None:
    x = pts((1, 1), (2, 1), (1, 2), (6, 5), (7, 5), (6, 6), (9, 9))
    centers, labels, history = lloyd(x, [x[0], x[1]])
    assert labels == [0, 0, 0, 1, 1, 1, 1]
    assert centers == [(F(4, 3), F(4, 3)), (F(7), F(25, 4))]
    assert history == [F(593, 10), F(217, 12)]
    assert history[-1] == best_cost(x, 2)


def test_local_optimum_rectangle() -> None:
    for w in (2, 4, 10):
        x = pts((0, 0), (0, 1), (w, 0), (w, 1))
        centers, labels, history = lloyd(x, [x[0], x[1]])
        assert labels == [0, 1, 0, 1]
        assert history[-1] == w * w
        assert best_cost(x, 2) == 1


def test_monotone_and_fixed_point() -> None:
    rng = random.Random(3)
    for _ in range(60):
        n = rng.randrange(2, 9)
        d = rng.randrange(1, 3)
        x = [tuple(F(rng.randrange(-6, 7)) for _ in range(d)) for _ in range(n)]
        k = rng.randrange(1, n + 1)
        init = random_init(x, k, rng)
        centers, labels, history = lloyd(x, init)
        assert all(history[i + 1] < history[i] for i in range(len(history) - 1))
        # fixed point: each point is at a nearest center, each non-empty cluster at its mean
        for p, a in zip(x, labels):
            assert sq_dist(p, centers[a]) == min(sq_dist(p, c) for c in centers)
        for j in range(k):
            m = [p for p, a in zip(x, labels) if a == j]
            if m:
                assert centers[j] == centroid(m)
        if n <= 6 and k <= 3:
            assert history[-1] >= best_cost(x, k) or len(set(labels)) < k


def test_half_steps_do_not_increase() -> None:
    rng = random.Random(11)
    for _ in range(80):
        x = [(F(rng.randrange(-9, 10)), F(rng.randrange(-9, 10))) for _ in range(rng.randrange(3, 12))]
        k = rng.randrange(1, 4)
        centers = random_init(x, min(k, len(x)), rng)
        labels = [min(range(len(centers)), key=lambda j: sq_dist(p, centers[j])) for p in x]
        for _ in range(20):
            before = assignment_cost(x, centers, labels)
            new_centers = list(centers)
            for j in range(len(centers)):
                m = [p for p, a in zip(x, labels) if a == j]
                if m:
                    new_centers[j] = centroid(m)
            mid = assignment_cost(x, new_centers, labels)
            assert mid <= before
            new_labels = [min(range(len(centers)), key=lambda j: sq_dist(p, new_centers[j])) for p in x]
            assert assignment_cost(x, new_centers, new_labels) <= mid
            centers, labels = new_centers, new_labels


def test_float_input_terminates() -> None:
    rng = random.Random(5)
    x = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(300)]
    centers, labels, history = lloyd(x, random_init(x, 5, rng))
    assert len(history) < 300
    assert all(history[i + 1] <= history[i] + 1e-9 for i in range(len(history) - 1))


def test_edges() -> None:
    x = pts((3, 4))
    assert lloyd(x, [x[0]]) == ([x[0]], [0], [0])
    x = pts((0,), (0,), (5,))
    centers, labels, history = lloyd(x, [x[0], x[1]])
    # both centers start at 0; the lowest index takes all points, the second center
    # stays empty for one iteration and keeps its place, then takes the two zeros
    assert history == [F(50, 3), 0]
    assert labels == [1, 1, 0]
