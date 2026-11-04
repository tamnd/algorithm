# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fusion-tree/. The authors are listed in prov/SD1PX6.jsonl.

import bisect
import random

import pytest

from fusion_tree import FusionNode, FusionTree


def oracle_pred(a, q):
    i = bisect.bisect_right(a, q)
    return a[i - 1] if i else None


def oracle_succ(a, q):
    i = bisect.bisect_left(a, q)
    return a[i] if i < len(a) else None


def test_node_example() -> None:
    v = FusionNode([2, 9, 12, 26])
    assert v.pos == [4, 3, 2]
    assert [v.sketch(x) for x in v.keys] == [0, 2, 3, 6]
    assert v.packed_rank(3) == 2
    assert v.sketch(13) == 3 and v.packed_rank(v.sketch(13)) == 2
    assert v.keys[v.node_pred(13)] == 12  # the sketch rank alone would give 9
    assert v.keys[v.node_pred(21)] == 12
    assert v.node_pred(1) == -1 and v.keys[v.node_pred(31)] == 26


def test_small_and_empty() -> None:
    t = FusionTree([], w=16, b=4)
    t.check_invariant()
    assert t.predecessor(5) is None and t.successor(5) is None and t.keys() == []
    t = FusionTree([7], w=16, b=4)
    assert t.predecessor(6) is None and t.predecessor(7) == 7 and t.successor(8) is None
    with pytest.raises(ValueError):
        FusionTree([1], w=16, b=5)
    with pytest.raises(ValueError):
        FusionTree([1 << 16], w=16, b=4)


def test_exhaustive_small_universe() -> None:
    rng = random.Random(11)
    for _ in range(200):
        a = sorted(rng.sample(range(64), rng.randrange(1, 30)))
        t = FusionTree(a, w=16, b=4)
        t.check_invariant()
        assert t.keys() == a
        for q in range(64):
            assert t.predecessor(q) == oracle_pred(a, q)
            assert t.successor(q) == oracle_succ(a, q)


def test_random_against_bisect() -> None:
    rng = random.Random(20251104)
    for case in range(600):
        w = rng.choice([16, 32, 64])
        b = rng.choice([2, 3, 4]) if w == 16 else rng.choice([4, 5, 8]) if w == 64 else rng.choice([3, 4, 5])
        n = rng.randrange(1, 300)
        if rng.random() < 0.3:
            base = rng.randrange(1 << (w - 8))
            a = sorted({(base << 8) | rng.randrange(256) for _ in range(n)})
        else:
            a = sorted({rng.randrange(1 << w) for _ in range(n)})
        sa = set(a)
        t = FusionTree(a, w=w, b=b)
        if case % 20 == 0:
            t.check_invariant()
            assert t.keys() == a
        for _ in range(30):
            if rng.random() < 0.3:
                q = rng.choice(a) + rng.choice([-1, 0, 1])
                q = min(max(q, 0), (1 << w) - 1)
            else:
                q = rng.randrange(1 << w)
            assert t.predecessor(q) == oracle_pred(a, q)
            assert t.successor(q) == oracle_succ(a, q)
            assert t.contains(q) == (q in sa)


def test_height() -> None:
    a = list(range(0, 3 * 10 ** 5, 3))
    t = FusionTree(a, w=64, b=8)
    assert t.height() <= 7
    assert t.predecessor(299999) == 299997 and t.predecessor(300000 * 7) == 299997
