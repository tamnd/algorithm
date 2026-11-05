# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aldous-broder/. The authors are listed in prov/KAFQ9E.jsonl.

import itertools
import math
import random
from collections import Counter

from aldous_broder import aldous_broder

EXAMPLE = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (2, 4, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]


def components(n, edges, chosen):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in chosen:
        u, v, _ = edges[i]
        parent[find(u)] = find(v)
    return len({find(x) for x in range(n)})


def spanning_forests(n, edges):
    """All edge sets that are forests with the components of the graph."""
    c = components(n, edges, range(len(edges)))
    k = n - c
    return [
        s
        for s in itertools.combinations(range(len(edges)), k)
        if components(n, edges, s) == c
    ]


def chi_square(counts, expected):
    return sum((counts.get(t, 0) - e) ** 2 / e for t, e in expected.items())


def check_distribution(n, edges, samples, seed, weighted=False):
    forests = spanning_forests(n, edges)
    weight = {s: (math.prod(edges[i][2] for i in s) if weighted else 1.0) for s in forests}
    total = sum(weight.values())
    expected = {s: samples * weight[s] / total for s in forests}
    rng = random.Random(seed)
    counts = Counter(tuple(aldous_broder(n, edges, rng, weighted)) for _ in range(samples))
    assert set(counts) <= set(forests)
    df = len(forests) - 1
    # A bound far in the upper tail: mean df, standard deviation sqrt(2 df).
    assert chi_square(counts, expected) < df + 6 * math.sqrt(2 * df) + 10


def test_uniform_on_example():
    assert len(spanning_forests(6, EXAMPLE)) == 55
    check_distribution(6, EXAMPLE, 55 * 200, seed=1990)


def test_uniform_on_k4_and_with_parallel_edges_and_loops():
    k4 = [(i, j, 1) for i in range(4) for j in range(i + 1, 4)]
    check_distribution(4, k4, 16 * 300, seed=1)
    multi = [(0, 1, 1), (0, 1, 1), (1, 2, 1), (2, 0, 1), (2, 2, 1)]
    check_distribution(3, multi, 5 * 600, seed=2)


def test_weighted_distribution():
    tri = [(0, 1, 1.0), (1, 2, 2.0), (2, 0, 3.0)]
    check_distribution(3, tri, 6000, seed=3, weighted=True)
    check_distribution(6, EXAMPLE, 30000, seed=4, weighted=True)


def test_disconnected_gives_uniform_forest():
    g = [(0, 1, 1), (1, 2, 1), (2, 0, 1), (3, 4, 1), (4, 5, 1), (5, 3, 1), (3, 4, 1)]
    check_distribution(7, g, 15 * 300, seed=5)


def test_edge_cases():
    rng = random.Random(0)
    assert aldous_broder(0, [], rng) == []
    assert aldous_broder(1, [], rng) == []
    assert aldous_broder(1, [(0, 0, 1)], rng) == []
    assert aldous_broder(2, [], rng) == []
    assert aldous_broder(2, [(0, 1, -3)], rng) == [0]
    try:
        aldous_broder(2, [(0, 1, 0)], rng, weighted=True)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_random_graphs_give_spanning_forests():
    rng = random.Random(1989)
    for _ in range(600):
        n = rng.randrange(1, 8)
        m = rng.randrange(0, 12)
        edges = [(rng.randrange(n), rng.randrange(n), rng.choice([-1, 0, 2, 2])) for _ in range(m)]
        f = aldous_broder(n, edges, rng)
        c = components(n, edges, range(m))
        assert len(f) == n - c
        assert components(n, edges, f) == c
        assert all(edges[i][0] != edges[i][1] for i in f)
