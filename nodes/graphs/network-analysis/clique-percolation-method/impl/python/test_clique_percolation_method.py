# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clique-percolation-method/. The authors are listed in prov/8MV6VW.jsonl.

import itertools
import random

from clique_percolation_method import clique_percolation_method, k_cliques


def undirected(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def oracle(n: int, edges: list[tuple[int, int]], k: int) -> list[frozenset[int]]:
    """Communities from the definition: all k-subsets, pairwise tests, closure."""
    es = {frozenset(e) for e in edges}
    cl = [frozenset(s) for s in itertools.combinations(range(n), k)
          if all(frozenset(p) in es for p in itertools.combinations(s, 2))]
    label = list(range(len(cl)))
    changed = True
    while changed:
        changed = False
        for i in range(len(cl)):
            for j in range(len(cl)):
                if len(cl[i] & cl[j]) == k - 1 and label[j] < label[i]:
                    label[i] = label[j]
                    changed = True
    groups: dict[int, frozenset[int]] = {}
    for i, c in enumerate(cl):
        groups[label[i]] = groups.get(label[i], frozenset()) | c
    return sorted(groups.values(), key=lambda g: sorted(g))


EXAMPLE = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (6, 7)]


def test_example() -> None:
    adj = undirected(8, EXAMPLE)
    assert clique_percolation_method(adj, 3) == [frozenset({0, 1, 2, 3}), frozenset({3, 4, 5, 6})]
    assert clique_percolation_method(adj, 4) == [frozenset({0, 1, 2, 3})]
    assert clique_percolation_method(adj, 2) == [frozenset(range(8))]
    assert clique_percolation_method(adj, 5) == []


def test_edges() -> None:
    assert clique_percolation_method([], 3) == []
    assert clique_percolation_method([[]], 2) == []
    two = undirected(4, [(0, 1), (2, 3)])
    assert clique_percolation_method(two, 2) == [frozenset({0, 1}), frozenset({2, 3})]
    # two triangles sharing one vertex stay apart for k = 3
    bowtie = undirected(5, [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)])
    assert clique_percolation_method(bowtie, 3) == [frozenset({0, 1, 2}), frozenset({2, 3, 4})]
    k6 = undirected(6, [(u, v) for u in range(6) for v in range(u + 1, 6)])
    assert len(k_cliques(k6, 4)) == 15
    assert clique_percolation_method(k6, 4) == [frozenset(range(6))]


def test_random_against_oracle() -> None:
    rng = random.Random(2005)
    for _ in range(600):
        n = rng.randint(1, 9)
        p = rng.random()
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
        adj = undirected(n, edges)
        for lst in adj:
            rng.shuffle(lst)
        k = rng.randint(2, 5)
        got = clique_percolation_method(adj, k)
        assert sorted(got, key=lambda g: sorted(g)) == oracle(n, edges, k)
