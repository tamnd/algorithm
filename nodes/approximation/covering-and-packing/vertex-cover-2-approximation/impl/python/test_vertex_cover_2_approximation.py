# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-cover-2-approximation/. The authors are listed in prov/MQCR0W.jsonl.

import random
from itertools import combinations

import pytest

from vertex_cover_2_approximation import vertex_cover_2_approximation


def brute_opt(n, edges):
    for r in range(n + 1):
        for c in combinations(range(n), r):
            s = set(c)
            if all(u in s or v in s for u, v in edges):
                return r
    return n


def max_matching_size(edges):
    best = 0
    for r in range(1, len(edges) + 1):
        found = False
        for c in combinations(edges, r):
            ends = [x for e in c for x in e]
            if len(set(ends)) == len(ends):
                found = True
                break
        if not found:
            break
        best = r
    return best


def test_example_page():
    edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (4, 6), (5, 7), (6, 7)]
    cover, matching = vertex_cover_2_approximation(edges)
    assert matching == [(1, 2), (3, 5), (4, 6)]
    assert cover == {1, 2, 3, 4, 5, 6}
    assert brute_opt(8, edges) == 4


def test_random_against_brute_force():
    rng = random.Random(1974)
    for trial in range(300):
        n = rng.randint(1, 9)
        edges = [e for e in combinations(range(n), 2) if rng.random() < 0.4]
        rng.shuffle(edges)
        cover, matching = vertex_cover_2_approximation(edges)
        assert all(u in cover or v in cover for u, v in edges)
        ends = [x for e in matching for x in e]
        assert len(ends) == len(set(ends))  # a matching
        assert all(u in cover or v in cover for u, v in edges)  # maximal: each edge meets it
        assert len(cover) == 2 * len(matching)
        opt = brute_opt(n, edges)
        assert len(matching) <= opt  # the lower bound of the analysis
        assert len(cover) <= 2 * opt
        if len(edges) <= 10:
            assert max_matching_size(edges) <= opt


def test_tight_complete_bipartite():
    for k in range(1, 6):
        left = [("a", i) for i in range(k)]
        right = [("b", i) for i in range(k)]
        edges = [(u, v) for u in left for v in right]
        cover, matching = vertex_cover_2_approximation(edges)
        assert len(cover) == 2 * k  # OPT = k, one side


def test_tight_perfect_matching_graph():
    for k in range(1, 8):
        edges = [(2 * i, 2 * i + 1) for i in range(k)]
        cover, _ = vertex_cover_2_approximation(edges)
        assert len(cover) == 2 * k
        assert brute_opt(2 * k, edges) == k


def test_star_order_matters():
    # a star: OPT = 1, and the algorithm always takes 2 vertices
    edges = [(0, i) for i in range(1, 6)]
    cover, _ = vertex_cover_2_approximation(edges)
    assert len(cover) == 2


def test_self_loop():
    with pytest.raises(ValueError):
        vertex_cover_2_approximation([(1, 1)])
