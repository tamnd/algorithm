# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjacency-list/. The authors are listed in prov/3JK4BH.jsonl.

import random

import pytest

from adjacency_list import AdjacencyList


def test_example() -> None:
    g = AdjacencyList(4)
    assert g.adj == [[], [], [], []]
    g.add_edge(0, 1)
    assert g.adj == [[1], [0], [], []]
    g.add_edge(1, 2)
    assert g.adj == [[1], [0, 2], [1], []]
    g.add_edge(2, 0)
    assert g.adj == [[1, 2], [0, 2], [1, 0], []]
    g.add_edge(3, 1)
    assert g.adj == [[1, 2], [0, 2, 3], [1, 0], [1]]
    assert g.adjacent(0, 2)
    assert not g.adjacent(0, 3)
    assert g.neighbors(1) == [0, 2, 3]
    assert g.degree(1) == 3
    g.remove_edge(1, 0)
    assert g.adj == [[2], [3, 2], [1, 0], [1]]
    assert g.add_vertex() == 4
    assert g.adj == [[2], [3, 2], [1, 0], [1], []]
    g.check_invariant()


def test_directed_example() -> None:
    g = AdjacencyList(5, directed=True)
    for u, v in [(0, 1), (0, 2), (1, 2), (2, 3), (3, 1), (3, 4)]:
        g.add_edge(u, v)
    assert g.adj == [[1, 2], [2], [3], [1, 4], []]
    assert g.transpose().adj == [[], [0, 3], [0, 1], [2], [3]]


def test_edge_cases() -> None:
    g = AdjacencyList(0)
    assert g.edges() == []
    assert g.add_vertex() == 0
    assert g.neighbors(0) == []
    with pytest.raises(ValueError):
        g.add_edge(0, 0)
    with pytest.raises(ValueError):
        AdjacencyList(-1)
    d = AdjacencyList(1, directed=True)
    d.add_edge(0, 0)
    assert d.adjacent(0, 0) and d.degree(0) == 1
    d.remove_edge(0, 0)
    assert d.adj == [[]]
    with pytest.raises(IndexError):
        d.add_edge(0, 1)
    u = AdjacencyList(2)
    assert u.add_edge_if_absent(0, 1)
    assert not u.add_edge_if_absent(1, 0)
    u.remove_edge(0, 1)
    u.remove_edge(0, 1)
    assert u.edges() == []


@pytest.mark.parametrize("directed", [False, True])
def test_random_against_set_model(directed: bool) -> None:
    rng = random.Random(3104)
    for _ in range(300):
        n = rng.randint(1, 7)
        g = AdjacencyList(n, directed)
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
        assert sorted(g.edges()) == sorted(model)
        for u in range(n):
            nb = {b for a, b in model if a == u}
            if not directed:
                nb |= {a for a, b in model if b == u}
            assert sorted(g.neighbors(u)) == sorted(nb)
            assert g.degree(u) == len(nb)
