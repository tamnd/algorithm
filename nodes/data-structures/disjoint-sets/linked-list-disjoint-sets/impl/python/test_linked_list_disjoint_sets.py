# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linked-list-disjoint-sets/. The authors are listed in prov/JEF2AM.jsonl.

import random

import pytest

from linked_list_disjoint_sets import LinkedListDisjointSets


def test_example() -> None:
    d: LinkedListDisjointSets[int] = LinkedListDisjointSets()
    for x in range(7):
        d.make_set(x)
    moves = {x: 0 for x in range(7)}
    lists = []
    for a, b in [(0, 1), (2, 3), (1, 3), (4, 0), (5, 4), (3, 6)]:
        before = dict(d.head)
        assert d.union(a, b)
        d.check_invariant()
        for x in range(7):
            moves[x] += before[x] != d.head[x]
        lists.append(list(d.members(a)))
    assert lists[0] == [1, 0]
    assert lists[2] == [3, 2, 1, 0]
    assert lists[-1] == [3, 2, 1, 0, 4, 5, 6]
    assert sum(moves.values()) == 7
    assert max(moves.values()) == 2
    assert d.find(6) == 3 and d.size(0) == 7 and d.count == 1


def test_edges() -> None:
    d: LinkedListDisjointSets[str] = LinkedListDisjointSets()
    assert d.count == 0
    d.make_set("a")
    assert d.find("a") == "a" and d.size("a") == 1
    assert list(d.members("a")) == ["a"]
    assert not d.union("a", "a")
    d.check_invariant()
    with pytest.raises(ValueError):
        d.make_set("a")
    with pytest.raises(KeyError):
        d.find("b")


def test_moves_are_logarithmic() -> None:
    n = 1 << 10
    d: LinkedListDisjointSets[int] = LinkedListDisjointSets()
    for x in range(n):
        d.make_set(x)
    moves = [0] * n
    rng = random.Random(5)
    while d.count > 1:
        heads = list(d.length)
        a, b = rng.sample(heads, 2)
        before = [d.head[x] for x in range(n)]
        d.union(a, b)
        for x in range(n):
            moves[x] += before[x] != d.head[x]
    assert max(moves) <= 10


def test_random_against_model() -> None:
    rng = random.Random(31)
    for _ in range(500):
        n = rng.randrange(1, 14)
        d: LinkedListDisjointSets[int] = LinkedListDisjointSets()
        label = list(range(n))
        for x in range(n):
            d.make_set(x)
        for _ in range(rng.randrange(30)):
            a, b = rng.randrange(n), rng.randrange(n)
            r = rng.random()
            if r < 0.4:
                assert d.union(a, b) == (label[a] != label[b])
                old, new = label[a], label[b]
                label = [new if v == old else v for v in label]
                d.check_invariant()
            elif r < 0.7:
                assert d.connected(a, b) == (label[a] == label[b])
            else:
                expect = sorted(x for x in range(n) if label[x] == label[a])
                assert sorted(d.members(a)) == expect
                assert d.size(a) == len(expect)
        assert d.count == len(set(label))
