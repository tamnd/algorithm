# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incidence-matrix/. The authors are listed in prov/7DQ56G.jsonl.

import random

from incidence_matrix import IncidenceMatrix

EDGES = [(0, 1), (0, 2), (1, 2), (2, 3)]


def test_undirected_example() -> None:
    g = IncidenceMatrix(4)
    for u, v in EDGES:
        g.add_edge(u, v)
    assert g.B == [[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 0, 1]]
    assert g.ends(2) == (1, 2)
    assert g.incident(2) == [1, 2, 3]
    assert g.adjacent(3, 2) and not g.adjacent(0, 3)
    # B B^T = D + A for a simple undirected graph
    assert g.b_bt() == [[2, 1, 1, 0], [1, 2, 1, 0], [1, 1, 3, 1], [0, 0, 1, 1]]
    # B^T B = 2I + A(L(G))
    assert g.bt_b() == [[2, 1, 1, 0], [1, 2, 1, 1], [1, 1, 2, 1], [0, 1, 1, 2]]


def test_directed_example() -> None:
    g = IncidenceMatrix(4, directed=True)
    for u, v in EDGES:
        g.add_edge(u, v)
    assert g.B == [[-1, -1, 0, 0], [1, 0, -1, 0], [0, 1, 1, -1], [0, 0, 0, 1]]
    assert g.ends(3) == (2, 3)
    assert g.adjacent(0, 1) and not g.adjacent(1, 0)
    # B B^T = D - A of the underlying undirected graph: the Laplacian
    assert g.b_bt() == [[2, -1, -1, 0], [-1, 2, -1, 0], [-1, -1, 3, -1], [0, 0, -1, 1]]


def test_loop_and_parallel() -> None:
    g = IncidenceMatrix(2)
    g.add_edge(0, 0)
    g.add_edge(0, 1)
    g.add_edge(1, 0)
    assert g.B == [[2, 1, 1], [0, 1, 1]]
    assert g.ends(0) == (0, 0)
    assert g.adjacent(0, 0) and not g.adjacent(1, 1)
    assert [sum(r) for r in g.B] == [4, 2]


def test_random() -> None:
    rng = random.Random(5)
    for directed in (False, True):
        for _ in range(50):
            n = rng.randrange(1, 7)
            g = IncidenceMatrix(n, directed)
            es = []
            for _ in range(rng.randrange(12)):
                u, v = rng.randrange(n), rng.randrange(n)
                if directed and u == v:
                    continue
                es.append((u, v))
                g.add_edge(u, v)
            for e, (u, v) in enumerate(es):
                a, b = g.ends(e)
                assert (a, b) == (u, v) or (not directed and (b, a) == (u, v))
            for u in range(n):
                for v in range(n):
                    want = any((a, b) == (u, v) or (not directed and (b, a) == (u, v)) for a, b in es)
                    assert g.adjacent(u, v) == want
            for col in range(len(es)):
                s = sum(g.B[v][col] for v in range(n))
                assert s == (0 if directed else 2)
