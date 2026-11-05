# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-sparse-row/. The authors are listed in prov/J0260T.jsonl.

import random

import pytest

from compressed_sparse_row import CompressedSparseRow, _counting_pass


def test_example() -> None:
    e = [(3, 4), (0, 2), (2, 3), (3, 1), (0, 1), (1, 2)]
    off, by_u = _counting_pass(5, e, 0)
    assert off == [0, 2, 3, 4, 6, 6]
    assert [v for _, v in by_u] == [2, 1, 2, 3, 4, 1]
    g = CompressedSparseRow(5, e, directed=True)
    g.check_invariant()
    assert g.off == [0, 2, 3, 4, 6, 6]
    assert g.adj == [1, 2, 2, 3, 1, 4]
    assert g.neighbors(3) == [1, 4]
    assert g.degree(3) == 2 and g.degree(4) == 0
    assert g.adjacent(3, 4)
    assert not g.adjacent(1, 0)


def test_undirected_example() -> None:
    e = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5)]
    g = CompressedSparseRow(6, e)
    g.check_invariant()
    assert g.off == [0, 2, 5, 8, 11, 13, 14]
    assert g.adj == [1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3, 5, 4]
    assert g.edges() == e


def test_edge_cases() -> None:
    g = CompressedSparseRow(0, [])
    assert g.off == [0] and g.adj == [] and g.edges() == []
    h = CompressedSparseRow(3, [])
    assert h.off == [0, 0, 0, 0] and not h.adjacent(0, 2)
    d = CompressedSparseRow(1, [(0, 0)], directed=True)
    assert d.adjacent(0, 0) and d.neighbors(0) == [0]
    with pytest.raises(ValueError):
        CompressedSparseRow(2, [(1, 1)])
    with pytest.raises(ValueError):
        CompressedSparseRow(2, [(0, 1), (1, 0)])
    with pytest.raises(IndexError):
        CompressedSparseRow(2, [(0, 2)])
    with pytest.raises(IndexError):
        h.degree(3)


@pytest.mark.parametrize("directed", [False, True])
def test_random_against_set_model(directed: bool) -> None:
    rng = random.Random(260)
    for _ in range(300):
        n = rng.randint(0, 8)
        pairs = [(u, v) for u in range(n) for v in range(n) if directed or u < v]
        model = set(rng.sample(pairs, rng.randint(0, len(pairs))))
        given = [(v, u) if not directed and rng.random() < 0.5 else (u, v) for u, v in model]
        rng.shuffle(given)
        g = CompressedSparseRow(n, given, directed)
        g.check_invariant()
        assert set(g.edges()) == model
        for u in range(n):
            nb = {b for a, b in model if a == u}
            if not directed:
                nb |= {a for a, b in model if b == u}
            assert g.neighbors(u) == sorted(nb)
            assert g.degree(u) == len(nb)
            for v in range(n):
                assert g.adjacent(u, v) == (v in nb)
