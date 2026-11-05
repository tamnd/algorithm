# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triangle-listing-by-degree/. The authors are listed in prov/94JZ51.jsonl.

import itertools
import random

from triangle_listing_by_degree import local_counts, triangles_by_degree


def brute(n: int, edges: list[tuple[int, int]]) -> set[frozenset[int]]:
    e = {frozenset(x) for x in edges}
    return {
        frozenset(t)
        for t in itertools.combinations(range(n), 3)
        if all(frozenset(p) in e for p in itertools.combinations(t, 2))
    }


def test_example() -> None:
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 5), (2, 3), (2, 4), (3, 4)]
    tri = triangles_by_degree(6, edges)
    assert len(tri) == 6
    assert {frozenset(t) for t in tri} == brute(6, edges)
    assert local_counts(6, edges) == [5, 2, 4, 3, 3, 1]
    assert (3, 4, 2) in tri and (5, 1, 0) in tri


def test_edges() -> None:
    assert triangles_by_degree(0, []) == []
    assert triangles_by_degree(1, []) == []
    assert triangles_by_degree(3, [(0, 1), (1, 2)]) == []
    assert len(triangles_by_degree(3, [(0, 1), (1, 2), (0, 2)])) == 1
    k = 7
    clique = list(itertools.combinations(range(k), 2))
    assert len(triangles_by_degree(k, clique)) == 35
    star = [(0, i) for i in range(1, 9)]
    assert triangles_by_degree(9, star) == []


def test_random_against_brute_force() -> None:
    rng = random.Random(9071)
    for _ in range(600):
        n = rng.randint(0, 11)
        pairs = list(itertools.combinations(range(n), 2))
        p = rng.random()
        edges = [e if rng.random() < 0.5 else (e[1], e[0]) for e in pairs if rng.random() < p]
        rng.shuffle(edges)
        tri = triangles_by_degree(n, edges)
        sets = [frozenset(t) for t in tri]
        assert len(sets) == len(set(sets))
        assert set(sets) == brute(n, edges)
        assert all(len(s) == 3 for s in sets)
