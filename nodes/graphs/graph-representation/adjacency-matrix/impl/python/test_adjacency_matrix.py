# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjacency-matrix/. The authors are listed in prov/4VK71J.jsonl.

import random

import pytest

from adjacency_matrix import AdjacencyMatrix


def rows(g: AdjacencyMatrix) -> list[str]:
    return ["".join("1" if x else "0" for x in r) for r in g.a]


def test_example() -> None:
    g = AdjacencyMatrix(4)
    assert rows(g) == ["0000"] * 4
    g.add_edge(0, 1)
    assert rows(g) == ["0100", "1000", "0000", "0000"]
    g.add_edge(1, 2)
    assert rows(g) == ["0100", "1010", "0100", "0000"]
    g.add_edge(2, 0)
    assert rows(g) == ["0110", "1010", "1100", "0000"]
    g.add_edge(3, 1)
    assert rows(g) == ["0110", "1011", "1100", "0100"]
    assert [g.degree(v) for v in range(4)] == [2, 3, 2, 1]
    assert g.adjacent(0, 2)
    assert not g.adjacent(0, 3)
    assert g.neighbors(1) == [0, 2, 3]
    assert g.degree(1) == 3
    g.remove_edge(1, 0)
    assert rows(g) == ["0010", "0011", "1100", "0100"]
    assert g.add_vertex() == 4
    assert rows(g) == ["00100", "00110", "11000", "01000", "00000"]
    g.check_invariant()


def test_directed_example() -> None:
    g = AdjacencyMatrix(5, directed=True)
    for u, v in [(0, 1), (0, 2), (1, 2), (2, 3), (3, 1), (3, 4)]:
        g.add_edge(u, v)
    assert rows(g) == ["01100", "00100", "00010", "01001", "00000"]
    assert [g.degree(v) for v in range(5)] == [2, 1, 1, 2, 0]
    assert [sum(g.a[u][v] for u in range(5)) for v in range(5)] == [0, 2, 2, 1, 1]


def test_edge_cases() -> None:
    g = AdjacencyMatrix(0)
    assert g.edges() == []
    assert g.add_vertex() == 0
    assert g.neighbors(0) == []
    with pytest.raises(ValueError):
        g.add_edge(0, 0)
    d = AdjacencyMatrix(1, directed=True)
    d.add_edge(0, 0)
    assert d.adjacent(0, 0) and d.neighbors(0) == [0]
    with pytest.raises(IndexError):
        d.adjacent(0, 1)
    with pytest.raises(ValueError):
        AdjacencyMatrix(-1)
    g2 = AdjacencyMatrix(2)
    g2.add_edge(0, 1)
    g2.add_edge(1, 0)
    assert g2.edges() == [(0, 1)]
    g2.remove_edge(0, 1)
    g2.remove_edge(0, 1)
    assert g2.edges() == []


@pytest.mark.parametrize("directed", [False, True])
def test_random_against_set_model(directed: bool) -> None:
    rng = random.Random(4071)
    for _ in range(300):
        n = rng.randint(1, 7)
        g = AdjacencyMatrix(n, directed)
        model: set[tuple[int, int]] = set()

        def key(u: int, v: int) -> tuple[int, int]:
            return (u, v) if directed else (min(u, v), max(u, v))

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
        for u in range(n):
            nb = sorted({b for a, b in model if a == u} | (set() if directed else {a for a, b in model if b == u}))
            assert g.neighbors(u) == nb
            assert g.degree(u) == len(nb)
