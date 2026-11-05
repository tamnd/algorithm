# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/esu-algorithm/. The authors are listed in prov/EG33JY.jsonl.

import random
from itertools import combinations

from esu_algorithm import esu_algorithm


def connected(vertices, adj):
    """Whether the subgraph induced by vertices is connected, by a search inside it."""
    vertices = set(vertices)
    start = next(iter(vertices))
    seen = {start}
    stack = [start]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y in vertices and y not in seen:
                seen.add(y)
                stack.append(y)
    return seen == vertices


def reference(n, edges, k):
    """All k-subsets of the vertices whose induced subgraph is connected."""
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    return sorted(c for c in combinations(range(n), k) if connected(c, adj))


def random_graph(rng, n, p):
    return [(u, v) for u, v in combinations(range(n), 2) if rng.random() < p]


def test_example():
    edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (1, 4)]
    got = esu_algorithm(5, edges, 3)
    assert got == [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 2, 4), (1, 2, 3), (1, 3, 4), (2, 3, 4)]
    assert sorted(got) == reference(5, edges, 3)


def test_edge_cases():
    assert esu_algorithm(0, [], 1) == []
    assert esu_algorithm(3, [], 1) == [(0,), (1,), (2,)]
    assert esu_algorithm(3, [], 2) == []
    assert esu_algorithm(2, [(0, 1)], 3) == []
    assert esu_algorithm(2, [(0, 1), (1, 0), (1, 1)], 2) == [(0, 1)]
    try:
        esu_algorithm(3, [(0, 1)], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("k = 0 must be rejected")


def test_standard_graphs():
    # A path on n vertices has n - k + 1 connected k-sets.
    path = [(i, i + 1) for i in range(7)]
    assert len(esu_algorithm(8, path, 3)) == 6
    # A star with c leaves has C(c, k - 1) connected k-sets for k >= 2.
    star = [(0, i) for i in range(1, 7)]
    assert len(esu_algorithm(7, star, 3)) == 15
    # Every k-subset of a complete graph is connected.
    k6 = list(combinations(range(6), 2))
    assert len(esu_algorithm(6, k6, 4)) == 15


def test_random_against_reference():
    rng = random.Random(2006)
    for _ in range(400):
        n = rng.randint(1, 9)
        edges = random_graph(rng, n, rng.choice([0.2, 0.35, 0.5, 0.8]))
        rng.shuffle(edges)
        k = rng.randint(1, min(n, 5))
        got = esu_algorithm(n, edges, k)
        assert len(got) == len(set(got)), "a subgraph was output twice"
        assert sorted(got) == reference(n, edges, k)


if __name__ == "__main__":
    test_example()
    test_edge_cases()
    test_standard_graphs()
    test_random_against_reference()
    print("ok")
