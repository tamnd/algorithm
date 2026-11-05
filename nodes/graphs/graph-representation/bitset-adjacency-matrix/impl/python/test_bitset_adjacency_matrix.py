# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitset-adjacency-matrix/. The authors are listed in prov/WJ5KV3.jsonl.

import random

import pytest

from bitset_adjacency_matrix import BitsetAdjacencyMatrix

EDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5)]


def test_example() -> None:
    g = BitsetAdjacencyMatrix(6, w=4)
    for u, v in EDGES:
        g.add_edge(u, v)
    assert g.rows == [[0b0110, 0], [0b1101, 0], [0b1011, 0], [0b0110, 1], [0b1000, 2], [0, 1]]
    assert sum(g.common(u, v) for u, v in EDGES) == 6
    assert g.adjacent(1, 3)
    assert g.neighbors(3) == [1, 2, 4]
    assert g.degree(1) == 3
    assert g.common(1, 2) == 2
    g.remove_edge(2, 3)
    assert g.rows[2][0] == 0b0011 and g.rows[3][0] == 0b0010
    assert g.add_vertex() == 6
    assert all(len(r) == 2 for r in g.rows)
    g.check_invariant()


def test_complement_and_growth() -> None:
    g = BitsetAdjacencyMatrix(6, w=4)
    for u, v in EDGES:
        g.add_edge(u, v)
    c = g.complement()
    c.check_invariant()
    assert c.edges() == [(0, 3), (0, 4), (0, 5), (1, 4), (1, 5), (2, 4), (2, 5), (3, 5)]
    h = BitsetAdjacencyMatrix(4, w=4)
    assert h.add_vertex() == 4
    assert all(len(r) == 2 for r in h.rows)
    h.add_edge(4, 0)
    assert h.neighbors(0) == [4]
    h.check_invariant()


def test_edge_cases() -> None:
    g = BitsetAdjacencyMatrix(0)
    assert g.edges() == [] and g.complement().edges() == []
    assert g.add_vertex() == 0
    assert g.neighbors(0) == [] and g.degree(0) == 0
    with pytest.raises(ValueError):
        g.add_edge(0, 0)
    with pytest.raises(ValueError):
        BitsetAdjacencyMatrix(3, w=0)
    d = BitsetAdjacencyMatrix(1, directed=True, w=1)
    d.add_edge(0, 0)
    assert d.adjacent(0, 0) and d.neighbors(0) == [0]
    with pytest.raises(IndexError):
        d.adjacent(0, 1)


@pytest.mark.parametrize("w", [1, 3, 4, 64])
@pytest.mark.parametrize("directed", [False, True])
def test_random_against_set_model(directed: bool, w: int) -> None:
    rng = random.Random(5300 + w)
    for _ in range(150):
        n = rng.randint(1, 9)
        g = BitsetAdjacencyMatrix(n, directed, w)
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
                g.add_edge(u, v)
                model.add(key(u, v))
            elif op < 0.75:
                g.remove_edge(u, v)
                model.discard(key(u, v))
            else:
                assert g.adjacent(u, v) == (key(u, v) in model)
            g.check_invariant()
        assert set(g.edges()) == model

        def nb(x: int) -> set[int]:
            s = {b for a, b in model if a == x}
            if not directed:
                s |= {a for a, b in model if b == x}
            return s

        for u in range(n):
            assert g.neighbors(u) == sorted(nb(u))
            assert g.degree(u) == len(nb(u))
            v = rng.randrange(n)
            assert g.common(u, v) == len(nb(u) & nb(v))
        c = g.complement()
        c.check_invariant()
        for u in range(n):
            for v in range(n):
                if not directed and u == v:
                    assert not c.adjacent(u, v)
                else:
                    assert c.adjacent(u, v) != g.adjacent(u, v)
