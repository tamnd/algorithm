# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/buss-kernel/. The authors are listed in prov/0V3DF3.jsonl.

import random

import pytest

from buss_kernel import Kernel, buss_kernel
from graphs import (
    graphs_up_to_isomorphism,
    is_vertex_cover,
    labeled_graphs,
    min_vertex_cover,
    min_vertex_cover_size,
    random_graph,
)

# The page example: a star on 0, ..., 6 with the edges 1-2 and 3-4, and a path 7-8-9.
EXAMPLE = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (3, 4), (7, 8), (8, 9)]


def check(edges: list, k: int, tau: int | None = None) -> Kernel:
    """Check every property of the kernel of (edges, k) against brute force.

    tau is the least cover size of the input graph, if the caller knows it.
    """
    ker = buss_kernel(edges, k)
    if tau is None:
        tau = min_vertex_cover_size(edges)
    # Equivalence: (G, k) is a yes-instance exactly when (G', k') is one.
    assert (min_vertex_cover_size(ker.edges) <= ker.k) == (tau <= k)
    # Size bounds in terms of k' and of k.
    assert 0 <= ker.k <= k
    assert len(ker.edges) <= ker.k * ker.k or ker.is_trivial_no
    assert len(ker.vertices) <= ker.k * ker.k + ker.k or ker.is_trivial_no
    assert len(ker.edges) <= max(1, k * k) and len(ker.vertices) <= max(2, k * k + k)
    if not ker.is_trivial_no:
        # The kernel is a subgraph of G, and F has exactly k - k' vertices.
        given = {frozenset(e) for e in edges}
        assert all(frozenset(e) in given for e in ker.edges)
        assert len(ker.forced) == k - ker.k
        assert not ker.forced & ker.vertices
        # Lifting: a least cover of the kernel plus F covers G.
        if min_vertex_cover_size(ker.edges) <= ker.k:
            cover = min_vertex_cover(ker.edges) | ker.forced
            assert is_vertex_cover(edges, cover) and len(cover) <= k
    return ker


def test_page_example_no() -> None:
    ker = check(EXAMPLE, 3)
    assert ker.is_trivial_no


def test_page_example_yes() -> None:
    ker = check(EXAMPLE, 4)
    assert ker.k == 3 and ker.forced == {0}
    assert {frozenset(e) for e in ker.edges} == {frozenset(e) for e in [(1, 2), (3, 4), (7, 8), (8, 9)]}
    assert min_vertex_cover_size(ker.edges) == 3


def test_edge_cases() -> None:
    assert buss_kernel([], 0) == Kernel([], 0, set())
    assert check([(1, 2)], 0).is_trivial_no
    ker = check([(0, i) for i in range(1, 6)], 1)  # a star needs only its center
    assert ker.edges == [] and ker.k == 0 and ker.forced == {0}
    assert check([(2 * i, 2 * i + 1) for i in range(3)], 2).k == 2  # 3 edges, 6 vertices: kept
    assert check([(2 * i, 2 * i + 1) for i in range(5)], 2).is_trivial_no  # 5 edges > 4
    assert check([(1, 2), (1, 2), (2, 1)], 1).edges in ([(1, 2)], [(2, 1)])
    with pytest.raises(ValueError):
        buss_kernel([(1, 1)], 2)
    with pytest.raises(ValueError):
        buss_kernel([(1, 2)], -1)


def test_all_labeled_graphs_up_to_5_vertices() -> None:
    for n in range(2, 6):
        for edges in labeled_graphs(n):
            for k in range(n + 1):
                check(edges, k)


def test_all_graphs_on_6_and_7_vertices() -> None:
    six = graphs_up_to_isomorphism(6)
    assert len(six) == 156
    for edges in six:
        tau = min_vertex_cover_size(edges)
        for k in range(7):
            check(edges, k, tau)
    # Every graph on 7 vertices is a graph on 6 vertices plus a vertex 6.
    # Test the budgets next to the answer, where a wrong kernel shows first.
    for edges in six:
        for nbrs in range(64):
            g = edges + [(v, 6) for v in range(6) if nbrs >> v & 1]
            tau = min_vertex_cover_size(g)
            for k in {max(0, tau - 1), tau}:
                check(g, k, tau)


def test_random_graphs_against_brute_force() -> None:
    rng = random.Random(20260424)
    for _ in range(600):
        n = rng.randint(2, 13)
        edges = random_graph(n, rng.choice([0.1, 0.2, 0.35, 0.5, 0.8]), rng)
        tau = min_vertex_cover_size(edges)
        check(edges, rng.choice([max(0, tau - 1), tau, rng.randint(0, n)]), tau)


def test_stars_and_hubs_hit_the_bound() -> None:
    # k disjoint stars with k leaves each: no forced vertex, k^2 edges, k^2 + k vertices.
    for k in range(1, 4):
        edges = [((s, "c"), (s, i)) for s in range(k) for i in range(k)]
        ker = check(edges, k)
        assert len(ker.edges) == k * k and len(ker.vertices) == k * k + k
    # A hub joined to many leaves, plus a matching of size k: the hub is forced.
    edges = [("h", i) for i in range(50)] + [(("a", i), ("b", i)) for i in range(3)]
    ker = buss_kernel(edges, 4)
    assert ker.forced == {"h"} and ker.k == 3 and len(ker.edges) == 3


def test_large_input_is_fast() -> None:
    rng = random.Random(7)
    n = 20000
    edges = [(0, i) for i in range(1, n)] + [(rng.randrange(1, n), rng.randrange(1, n)) for _ in range(3 * n)]
    edges = [(u, v) for u, v in edges if u != v]
    ker = buss_kernel(edges, 10)
    assert ker.is_trivial_no
