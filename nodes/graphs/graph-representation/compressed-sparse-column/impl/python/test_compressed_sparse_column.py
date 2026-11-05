# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-sparse-column/. The authors are listed in prov/RG5BXY.jsonl.

import random

import pytest

from compressed_sparse_column import CompressedSparseColumn


def test_example() -> None:
    g = CompressedSparseColumn(5, [0, 2, 3, 4, 6, 6], [1, 2, 2, 3, 1, 4])
    g.check_invariant()
    assert g.coff == [0, 0, 2, 4, 5, 6]
    assert g.src == [0, 3, 0, 1, 2, 3]
    assert g.in_neighbors(1) == [0, 3]
    assert g.in_degree(0) == 0
    assert g.adjacent(1, 2)
    assert not g.adjacent(2, 1)
    assert g.pull_sum([1, 1, 1, 1, 1]) == [0, 2, 2, 1, 1]


def test_edge_cases() -> None:
    g = CompressedSparseColumn(0, [0], [])
    assert g.coff == [0] and g.edges() == []
    h = CompressedSparseColumn.from_edges(3, [])
    assert h.coff == [0, 0, 0, 0] and not h.adjacent(0, 1)
    loop = CompressedSparseColumn.from_edges(1, [(0, 0)])
    assert loop.in_neighbors(0) == [0] and loop.adjacent(0, 0)
    with pytest.raises(ValueError):
        CompressedSparseColumn(2, [0, 1], [1])
    with pytest.raises(ValueError):
        CompressedSparseColumn.from_edges(2, [(0, 1), (0, 1)])
    with pytest.raises(IndexError):
        CompressedSparseColumn.from_edges(2, [(0, 5)])
    with pytest.raises(IndexError):
        h.in_degree(3)


def test_random_against_set_model() -> None:
    rng = random.Random(5888)
    for _ in range(600):
        n = rng.randint(0, 8)
        pairs = [(u, v) for u in range(n) for v in range(n)]
        model = rng.sample(pairs, rng.randint(0, len(pairs)))
        g = CompressedSparseColumn.from_edges(n, model)
        g.check_invariant()
        assert sorted(g.edges()) == sorted(model)
        s = set(model)
        x = [rng.randint(-5, 5) for _ in range(n)]
        y = g.pull_sum(x)
        for v in range(n):
            ins = sorted(u for u, b in s if b == v)
            assert g.in_neighbors(v) == ins
            assert g.in_degree(v) == len(ins)
            assert y[v] == sum(x[u] for u in ins)
            for u in range(n):
                assert g.adjacent(u, v) == ((u, v) in s)
