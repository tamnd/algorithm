# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-union-find/. The authors are listed in prov/N5NH9D.jsonl.

import operator
import random

import pytest

from weighted_union_find import WeightedUnionFind


def test_example() -> None:
    u: WeightedUnionFind[int, int] = WeightedUnionFind()
    for x in range(6):
        u.make_set(x)
    results = []
    for x, y, d in [(0, 1, 3), (2, 3, -2), (1, 2, 4), (0, 3, 5), (0, 3, 6), (4, 5, 1)]:
        results.append(u.union(x, y, d))
        u.check_invariant()
    assert results == [True, True, True, True, False, True]
    assert u.parent == {0: 3, 1: 3, 2: 3, 3: 3, 4: 5, 5: 5}
    assert u.w == {0: 5, 1: 2, 2: -2, 3: 0, 4: 1, 5: 0}
    assert u.diff(0, 3) == 5
    assert u.diff(1, 2) == 4
    assert u.diff(0, 4) is None


def test_edges() -> None:
    u: WeightedUnionFind[str, int] = WeightedUnionFind()
    u.make_set("a")
    assert u.diff("a", "a") == 0
    assert u.union("a", "a", 0)
    assert not u.union("a", "a", 1)
    with pytest.raises(ValueError):
        u.make_set("a")
    with pytest.raises(KeyError):
        u.find("b")


def test_parity_group() -> None:
    u: WeightedUnionFind[int, int] = WeightedUnionFind(operator.xor, lambda a: a, 0)
    for x in range(4):
        u.make_set(x)
    assert u.union(0, 1, 1) and u.union(1, 2, 1) and u.union(2, 3, 1)
    assert u.diff(0, 3) == 1
    assert not u.union(0, 2, 1)
    u.check_invariant()


def test_long_chain_is_iterative() -> None:
    u: WeightedUnionFind[int, int] = WeightedUnionFind()
    n = 50000
    for x in range(n):
        u.make_set(x)
    for x in range(1, n):
        assert u.union(x, x - 1, 1)
    assert u.diff(n - 1, 0) == n - 1
    u.check_invariant()


def test_random_against_hidden_values() -> None:
    rng = random.Random(37)
    for _ in range(500):
        n = rng.randrange(1, 12)
        val = [rng.randrange(-20, 21) for _ in range(n)]
        u: WeightedUnionFind[int, int] = WeightedUnionFind()
        label = list(range(n))
        for x in range(n):
            u.make_set(x)
        for _ in range(rng.randrange(30)):
            a, b = rng.randrange(n), rng.randrange(n)
            r = rng.random()
            if r < 0.4:
                assert u.union(a, b, val[a] - val[b])
                old, new = label[a], label[b]
                label = [new if v == old else v for v in label]
                u.check_invariant()
            elif r < 0.6:
                wrong = val[a] - val[b] + rng.choice([-2, -1, 1, 2])
                assert u.union(a, b, wrong) == (label[a] != label[b])
                if label[a] != label[b]:
                    val_shift = wrong - (val[a] - val[b])
                    group = label[a]
                    val = [v + val_shift if label[i] == group else v for i, v in enumerate(val)]
                    old, new = label[a], label[b]
                    label = [new if v == old else v for v in label]
            else:
                expect = val[a] - val[b] if label[a] == label[b] else None
                assert u.diff(a, b) == expect
