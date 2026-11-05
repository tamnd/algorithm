# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/label-propagation-algorithm/. The authors are listed in prov/GKHM2A.jsonl.

import random
from itertools import combinations

from label_propagation_algorithm import label_propagation_algorithm


def neighbour_lists(n, edges):
    nb = [[] for _ in range(n)]
    for u, v in set((min(a, b), max(a, b)) for a, b in edges if a != b):
        nb[u].append(v)
        nb[v].append(u)
    return nb


def is_stable(n, edges, label):
    """The definition: each vertex with a neighbour holds a most frequent neighbour label."""
    nb = neighbour_lists(n, edges)
    for v in range(n):
        if not nb[v]:
            continue
        counts = [sum(1 for w in nb[v] if label[w] == x) for x in range(n)]
        if counts[label[v]] != max(counts):
            return False
    return True


def components(n, edges):
    comp = list(range(n))
    changed = True
    while changed:
        changed = False
        for u, v in edges:
            low = min(comp[u], comp[v])
            if comp[u] != low or comp[v] != low:
                comp[u] = comp[v] = low
                changed = True
    return comp


def random_graph(rng, n, p):
    return [(u, v) for u, v in combinations(range(n), 2) if rng.random() < p]


def test_single_edge_and_empty():
    labels, comms, rounds = label_propagation_algorithm(2, [(0, 1)], random.Random(1))
    assert comms == [[0, 1]] and rounds == 2
    labels, comms, rounds = label_propagation_algorithm(3, [], random.Random(1))
    assert labels == [0, 1, 2] and comms == [[0], [1], [2]] and rounds == 1
    assert label_propagation_algorithm(0, []) == ([], [], 1)


def test_disjoint_cliques():
    rng = random.Random(36106)
    for _ in range(100):
        sizes = [rng.randint(2, 6) for _ in range(rng.randint(1, 4))]
        edges, start, expect = [], 0, []
        for s in sizes:
            block = list(range(start, start + s))
            edges += list(combinations(block, 2))
            expect.append(block)
            start += s
        _, comms, _ = label_propagation_algorithm(start, edges, rng)
        assert comms == expect


def test_random_graphs():
    rng = random.Random(20070911)
    for _ in range(800):
        n = rng.randint(0, 12)
        edges = random_graph(rng, n, rng.choice([0.1, 0.25, 0.5, 0.8]))
        labels, comms, rounds = label_propagation_algorithm(n, edges, random.Random(rng.random()))
        assert is_stable(n, edges, labels)
        assert rounds <= len(edges) + 1
        comp = components(n, edges)
        for v in range(n):
            assert comp[labels[v]] == comp[v]
        assert sorted(v for c in comms for v in c) == list(range(n))
        for c in comms:
            assert len({labels[v] for v in c}) == 1


def test_reproducible():
    rng = random.Random(5)
    edges = random_graph(rng, 30, 0.15)
    a = label_propagation_algorithm(30, edges, random.Random(99))
    b = label_propagation_algorithm(30, edges, random.Random(99))
    assert a == b


if __name__ == "__main__":
    test_single_edge_and_empty()
    test_disjoint_cliques()
    test_random_graphs()
    test_reproducible()
    print("ok")
