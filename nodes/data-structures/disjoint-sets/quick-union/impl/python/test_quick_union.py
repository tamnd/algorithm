# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quick-union/. The authors are listed in prov/TPV99M.jsonl.

import random

import pytest

from quick_union import QuickUnion

TINY = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1), (8, 9), (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]


def test_example() -> None:
    uf = QuickUnion(10)
    merged = []
    for p, q in TINY:
        merged.append(uf.union(p, q))
        uf.check_invariant()
    assert merged == [True] * 5 + [False] + [True] * 3 + [False, False]
    assert uf.parent == [1, 1, 1, 8, 3, 0, 5, 1, 8, 8]
    assert [uf.depth(x) for x in range(10)] == [1, 0, 1, 1, 2, 2, 3, 1, 0, 1]
    assert uf.count == 2
    assert uf.find(6) == 1 and uf.find(9) == 8


def test_edges() -> None:
    uf = QuickUnion(0)
    assert uf.count == 0 and len(uf) == 0
    uf = QuickUnion(1)
    assert uf.find(0) == 0
    assert not uf.union(0, 0)
    assert uf.count == 1
    with pytest.raises(IndexError):
        uf.find(1)
    with pytest.raises(ValueError):
        QuickUnion(-1)


def test_chain_worst_case() -> None:
    n = 2000
    uf = QuickUnion(n)
    for k in range(1, n):
        assert uf.depth(0) == k - 1
        uf.union(0, k)
    assert uf.depth(0) == n - 1
    assert uf.find(0) == n - 1
    uf.check_invariant()


def test_random_against_labels() -> None:
    rng = random.Random(29)
    for _ in range(600):
        n = rng.randrange(1, 14)
        uf = QuickUnion(n)
        label = list(range(n))
        for _ in range(rng.randrange(30)):
            p, q = rng.randrange(n), rng.randrange(n)
            if rng.random() < 0.5:
                assert uf.union(p, q) == (label[p] != label[q])
                old, new = label[p], label[q]
                label = [new if v == old else v for v in label]
                uf.check_invariant()
            else:
                assert uf.connected(p, q) == (label[p] == label[q])
        assert uf.count == len(set(label))
