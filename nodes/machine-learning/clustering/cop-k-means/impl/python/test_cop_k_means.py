# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cop-k-means/. The authors are listed in prov/CH7828.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from cop_k_means import cop_kmeans, satisfies, sqdist, mean


def random_points(rng, n):
    return [[Fraction(rng.randint(0, 20)), Fraction(rng.randint(0, 20))] for _ in range(n)]


def lloyd(points, centers, max_iter=100):
    centers = [list(c) for c in centers]
    k = len(centers)
    previous = None
    for _ in range(max_iter):
        labels = [min(range(k), key=lambda c: (sqdist(p, centers[c]), c)) for p in points]
        for c in range(k):
            members = [p for p, l in zip(points, labels) if l == c]
            if members:
                centers[c] = mean(members)
        if labels == previous:
            break
        previous = labels
    return labels, centers


def test_output_satisfies_constraints_or_reports_failure():
    rng = random.Random(1)
    failures = successes = 0
    for _ in range(300):
        n = rng.randint(2, 12)
        k = rng.randint(1, min(4, n))
        pts = random_points(rng, n)
        pairs = list(combinations(range(n), 2))
        rng.shuffle(pairs)
        ml = pairs[:rng.randint(0, 3)]
        cl = pairs[3:3 + rng.randint(0, 4)]
        labels, _ = cop_kmeans(pts, k, ml, cl, rng=random.Random(rng.random()))
        if labels is None:
            failures += 1
        else:
            successes += 1
            assert satisfies(labels, ml, cl)
            assert all(0 <= l < k for l in labels)
    assert failures > 0 and successes > 0


def test_failure_on_a_feasible_instance():
    # a and b take the two clusters, then c can join neither
    a, b, c = [Fraction(0)], [Fraction(10)], [Fraction(5)]
    pts = [a, b, c]
    cl = [(0, 2), (1, 2)]
    labels, _ = cop_kmeans(pts, 2, [], cl, centers=[a, b])
    assert labels is None
    # yet the clustering {a, b}, {c} is feasible
    assert satisfies([0, 0, 1], [], cl)
    # with another order COP-k-means succeeds
    labels, _ = cop_kmeans(pts, 2, [], cl, centers=[a, b], order=[2, 0, 1])
    assert labels is not None and satisfies(labels, [], cl)


def test_no_constraints_is_lloyd():
    rng = random.Random(2)
    for _ in range(50):
        pts = random_points(rng, rng.randint(3, 15))
        k = rng.randint(1, 3)
        init = [pts[i] for i in rng.sample(range(len(pts)), k)]
        assert cop_kmeans(pts, k, [], [], centers=init) == lloyd(pts, init)


def test_must_link_alone_never_fails():
    # with the closure, a chain a - c - b cannot end in two clusters
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(2, 12)
        pts = random_points(rng, n)
        ml = [p for p in combinations(range(n), 2) if rng.random() < 0.15]
        order = list(range(n))
        rng.shuffle(order)
        labels, _ = cop_kmeans(pts, rng.randint(1, min(3, n)), ml, [], rng=rng, order=order)
        assert labels is not None and satisfies(labels, ml, [])


def test_example_order_matters():
    pts = [[Fraction(x)] for x in [0, 1, 2, 10, 11, 12]]
    init = [[Fraction(0)], [Fraction(12)]]
    labels, centers = cop_kmeans(pts, 2, [(2, 3)], [], centers=init)
    assert labels == [0, 0, 0, 0, 1, 1]
    assert centers == [[Fraction(13, 4)], [Fraction(23, 2)]]
    labels, centers = cop_kmeans(pts, 2, [(2, 3)], [], centers=init, order=[5, 4, 3, 2, 1, 0])
    assert labels == [0, 0, 1, 1, 1, 1]
    assert centers == [[Fraction(1, 2)], [Fraction(35, 4)]]


def test_must_link_moves_points_together():
    pts = [[Fraction(x)] for x in [0, 1, 2, 10, 11, 12]]
    labels, centers = cop_kmeans(pts, 2, [(2, 3)], [], centers=[[Fraction(0)], [Fraction(12)]])
    assert labels[2] == labels[3]
    assert satisfies(labels, [(2, 3)], [])
