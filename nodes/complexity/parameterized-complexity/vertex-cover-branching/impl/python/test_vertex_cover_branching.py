# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-cover-branching/. The authors are listed in prov/XFZWRM.jsonl.

import random

import pytest

from graphs import (
    graphs_up_to_isomorphism,
    is_vertex_cover,
    labeled_graphs,
    min_vertex_cover_size,
    random_graph,
)
from vertex_cover_branching import (
    _cover_of_max_degree_two,
    search_tree_nodes,
    vertex_cover_branching,
    vertex_cover_degree3,
)

# The page example: the path a-b-c-d with the extra edge b-d, so a triangle b, c, d with a tail a.
EXAMPLE = [("a", "b"), ("b", "c"), ("c", "d"), ("b", "d")]


def leaf_bound(k: int) -> int:
    """Return T(k) with T(b) = max(1, T(b-1) + T(b-3)) and T(b) = 0 for b < 0."""
    t = [0, 0, 0]  # T(-3), T(-2), T(-1)
    for _ in range(k + 1):
        t.append(max(1, t[-1] + t[-3]))
    return t[-1]


def check(edges: list, k: int, tau: int) -> None:
    """Check both algorithms on (edges, k) against the least cover size tau."""
    s = vertex_cover_branching(edges, k)
    assert (s is not None) == (tau <= k)
    if s is not None:
        assert is_vertex_cover(edges, s) and len(s) <= k
    assert search_tree_nodes(edges, k) <= 2 ** (k + 1) - 1
    t, leaves = vertex_cover_degree3(edges, k)
    assert (t is not None) == (tau <= k)
    if t is not None:
        assert is_vertex_cover(edges, t) and len(t) <= k
    assert leaves <= leaf_bound(k)


def test_page_example() -> None:
    assert vertex_cover_branching(EXAMPLE, 1) is None
    assert search_tree_nodes(EXAMPLE, 1) == 3
    assert vertex_cover_branching(EXAMPLE, 2) == {"b", "c"}
    # Nodes: the root, a, a+b, a+c, b, b+c. The last one covers every edge.
    assert search_tree_nodes(EXAMPLE, 2) == 6
    assert min_vertex_cover_size(EXAMPLE) == 2


def test_edge_cases() -> None:
    assert vertex_cover_branching([], 0) == set()
    assert vertex_cover_branching([(1, 2)], 0) is None
    assert vertex_cover_branching([(1, 2)], 1) in ({1}, {2})
    assert vertex_cover_degree3([], 0) == (set(), 1)
    assert vertex_cover_degree3([(1, 2)], 0)[0] is None
    with pytest.raises(ValueError):
        vertex_cover_branching([(1, 1)], 2)
    with pytest.raises(ValueError):
        vertex_cover_degree3([(1, 2)], -1)


def test_worst_case_tree_is_full() -> None:
    # k + 1 disjoint edges: every branch fails at depth k, so the tree is full.
    for k in range(9):
        edges = [(2 * i, 2 * i + 1) for i in range(k + 1)]
        assert vertex_cover_branching(edges, k) is None
        assert search_tree_nodes(edges, k) == 2 ** (k + 1) - 1


def test_degree_two_solver() -> None:
    for p in range(2, 12):
        path = [(i, i + 1) for i in range(p - 1)]
        cycle = path + [(p - 1, 0)] if p >= 3 else path
        for g in (path, cycle):
            adj: dict = {}
            for u, v in g:
                adj.setdefault(u, set()).add(v)
                adj.setdefault(v, set()).add(u)
            c = _cover_of_max_degree_two(adj)
            assert is_vertex_cover(g, c) and len(c) == min_vertex_cover_size(g)


def test_all_labeled_graphs_up_to_5_vertices() -> None:
    for n in range(2, 6):
        for edges in labeled_graphs(n):
            tau = min_vertex_cover_size(edges)
            for k in range(n + 1):
                check(edges, k, tau)


def test_all_graphs_on_6_and_7_vertices() -> None:
    six = graphs_up_to_isomorphism(6)
    for edges in six:
        tau = min_vertex_cover_size(edges)
        for k in range(7):
            check(edges, k, tau)
    for edges in six:
        for nbrs in range(64):
            g = edges + [(v, 6) for v in range(6) if nbrs >> v & 1]
            tau = min_vertex_cover_size(g)
            for k in {max(0, tau - 1), tau}:
                check(g, k, tau)


def test_random_graphs_against_brute_force() -> None:
    rng = random.Random(20260425)
    for _ in range(600):
        n = rng.randint(2, 14)
        edges = random_graph(n, rng.choice([0.1, 0.2, 0.35, 0.5]), rng)
        rng.shuffle(edges)
        tau = min_vertex_cover_size(edges)
        check(edges, rng.choice([max(0, tau - 1), tau, min(tau + 1, 9)]), tau)


def test_deep_budget_uses_no_recursion() -> None:
    # A long path has a cover of size n // 2; the first branch always succeeds.
    n = 5000
    path = [(i, i + 1) for i in range(n - 1)]
    s = vertex_cover_branching(path, n)
    assert s is not None and is_vertex_cover(path, s)
    t, _ = vertex_cover_degree3(path, n // 2)
    assert t is not None and len(t) == n // 2
