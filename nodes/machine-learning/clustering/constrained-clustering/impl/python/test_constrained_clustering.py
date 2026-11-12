# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constrained-clustering/. The authors are listed in prov/PBR52S.jsonl.

import random
from itertools import combinations, product

from constrained_clustering import feasible, ml_components, satisfies


def brute(n, ml, cl, k):
    for labels in product(range(k), repeat=n):
        if len(set(labels)) == k and satisfies(labels, ml, cl):
            return True
    return False


def random_pairs(rng, n, p):
    return [(a, b) for a, b in combinations(range(n), 2) if rng.random() < p]


def test_against_brute_force():
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randint(1, 7)
        k = rng.randint(1, min(n, 4))
        ml = random_pairs(rng, n, rng.choice([0, 0.1, 0.2]))
        cl = random_pairs(rng, n, rng.choice([0, 0.2, 0.4, 0.6]))
        labels = feasible(n, ml, cl, k)
        assert (labels is not None) == brute(n, ml, cl, k)
        if labels is not None:
            assert satisfies(labels, ml, cl)
            assert set(labels) == set(range(k))


def test_must_link_alone_is_feasible_iff_enough_components():
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 9)
        ml = random_pairs(rng, n, 0.2)
        _, m = ml_components(n, ml)
        for k in range(1, n + 1):
            assert (feasible(n, ml, [], k) is not None) == (m >= k)


def test_cannot_link_is_graph_coloring():
    # the 5-cycle needs 3 colors; K4 needs 4; the Petersen graph needs 3
    c5 = [(i, (i + 1) % 5) for i in range(5)]
    assert feasible(5, [], c5, 2) is None
    assert feasible(5, [], c5, 3) is not None
    k4 = list(combinations(range(4), 2))
    assert feasible(4, [], k4, 3) is None
    assert feasible(4, [], k4, 4) is not None
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    petersen = outer + spokes + inner
    assert feasible(10, [], petersen, 2) is None
    labels = feasible(10, [], petersen, 3)
    assert labels is not None and satisfies(labels, [], petersen)


def test_example():
    # ML: 0-1, 1-2, 3-4; CL: 2-3, 0-5, 4-5
    ml = [(0, 1), (1, 2), (3, 4)]
    cl = [(2, 3), (0, 5), (4, 5)]
    assert feasible(6, ml, cl, 2) is None          # a triangle of components
    labels = feasible(6, ml, cl, 3)
    assert labels is not None and satisfies(labels, ml, cl)
    assert feasible(6, ml + [(0, 3)], cl, 3) is None  # CL 2-3 inside a component
