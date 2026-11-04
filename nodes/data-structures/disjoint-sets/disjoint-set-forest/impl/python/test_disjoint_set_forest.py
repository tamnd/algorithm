# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disjoint-set-forest/. The authors are listed in prov/B24A25.jsonl.

import random

import pytest

from disjoint_set_forest import DisjointSetForest


def test_example() -> None:
    d: DisjointSetForest[int] = DisjointSetForest()
    for x in range(8):
        d.make_set(x)
    for a, b in [(0, 1), (2, 3), (0, 2), (4, 5), (6, 7), (4, 6), (0, 4)]:
        assert d.union(a, b)
        d.check_invariant()
    assert d.parent == {0: 3, 1: 3, 2: 3, 3: 7, 4: 7, 5: 7, 6: 7, 7: 7}
    assert d.rank == {0: 0, 1: 1, 2: 0, 3: 2, 4: 0, 5: 1, 6: 0, 7: 3}
    assert d.find(0) == 7
    assert d.parent[0] == 7 and d.parent[1] == 3
    assert d.count == 1
    assert not d.union(2, 6)


def test_edges() -> None:
    d: DisjointSetForest[str] = DisjointSetForest()
    d.make_set("a")
    assert d.find("a") == "a"
    assert not d.union("a", "a")
    assert d.connected("a", "a")
    with pytest.raises(ValueError):
        d.make_set("a")
    with pytest.raises(KeyError):
        d.find("b")


def test_long_chain_has_log_height() -> None:
    d: DisjointSetForest[int] = DisjointSetForest()
    n = 1 << 12
    for x in range(n):
        d.make_set(x)
    for x in range(1, n):
        d.union(0, x)
    d.check_invariant()
    assert max(d.rank.values()) <= 12


def test_random_against_labels() -> None:
    rng = random.Random(19)
    for _ in range(500):
        n = rng.randrange(1, 15)
        d: DisjointSetForest[int] = DisjointSetForest()
        label = list(range(n))
        for x in range(n):
            d.make_set(x)
        for _ in range(rng.randrange(30)):
            a, b = rng.randrange(n), rng.randrange(n)
            if rng.random() < 0.5:
                merged = d.union(a, b)
                assert merged == (label[a] != label[b])
                old = label[b]
                label = [label[a] if v == old else v for v in label]
            else:
                assert d.connected(a, b) == (label[a] == label[b])
            d.check_invariant()
        assert d.count == len(set(label))
