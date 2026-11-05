# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edge-list/. The authors are listed in prov/SX5BWH.jsonl.

import random

import pytest

from edge_list import EdgeList


def test_example() -> None:
    g = EdgeList(4)
    assert g.edges() == []
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(3, 1)
    assert g.edges() == [(0, 1), (1, 2), (2, 0), (3, 1)]
    assert g.adjacent(0, 2)
    assert not g.adjacent(0, 3)
    assert g.neighbors(1) == [0, 2, 3]
    assert g.degree(1) == 3
    g.remove_edge(1, 0)
    assert g.edges() == [(3, 1), (1, 2), (2, 0)]
    assert g.add_vertex() == 4
    assert g.n == 5
    g.check_invariant()


def test_directed_example() -> None:
    g = EdgeList(5, directed=True)
    es = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 1), (3, 4)]
    for u, v in es:
        g.add_edge(u, v)
    assert [g.degree(v) for v in range(5)] == [2, 1, 1, 2, 0]
    assert g.to_adjacency_lists() == [[1, 2], [2], [3], [1, 4], []]
    assert not g.adjacent(1, 0)


def test_edge_cases() -> None:
    g = EdgeList(0)
    assert g.add_vertex() == 0
    assert g.neighbors(0) == []
    with pytest.raises(ValueError):
        g.add_edge(0, 0)
    with pytest.raises(ValueError):
        EdgeList(-1)
    d = EdgeList(1, directed=True)
    d.add_edge(0, 0)
    assert d.neighbors(0) == [0]
    d.remove_edge(0, 0)
    assert d.edges() == []
    with pytest.raises(IndexError):
        d.adjacent(0, 3)
    u = EdgeList(2)
    assert u.add_edge_if_absent(1, 0)
    assert not u.add_edge_if_absent(0, 1)
    u.remove_edge(0, 1)
    u.remove_edge(0, 1)
    assert u.edges() == []


@pytest.mark.parametrize("directed", [False, True])
def test_random_against_set_model(directed: bool) -> None:
    rng = random.Random(5847)
    for _ in range(300):
        n = rng.randint(1, 7)
        g = EdgeList(n, directed)
        model: set[tuple[int, int]] = set()

        def key(a: int, b: int) -> tuple[int, int]:
            return (a, b) if directed else (min(a, b), max(a, b))

        for _ in range(rng.randint(0, 40)):
            op = rng.random()
            u, v = rng.randrange(n), rng.randrange(n)
            if op < 0.05:
                assert g.add_vertex() == n
                n += 1
            elif op < 0.5:
                if not directed and u == v:
                    continue
                assert g.add_edge_if_absent(u, v) == (key(u, v) not in model)
                model.add(key(u, v))
            elif op < 0.75:
                g.remove_edge(u, v)
                model.discard(key(u, v))
            else:
                assert g.adjacent(u, v) == (key(u, v) in model)
            g.check_invariant()
        assert {key(a, b) for a, b in g.edges()} == model
        adj = g.to_adjacency_lists()
        for u in range(n):
            nb = {b for a, b in model if a == u}
            if not directed:
                nb |= {a for a, b in model if b == u}
            assert sorted(g.neighbors(u)) == sorted(nb) == sorted(adj[u])
