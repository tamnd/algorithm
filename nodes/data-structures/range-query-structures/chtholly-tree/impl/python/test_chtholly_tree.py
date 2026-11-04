# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chtholly-tree/. The authors are listed in prov/MQYKYZ.jsonl.

import random

import pytest

from chtholly_tree import ChthollyTree


def test_example() -> None:
    t = ChthollyTree([1, 1, 2, 2, 2, 3, 3, 3, 3, 1])
    assert t.runs() == [(0, 2, 1), (2, 5, 2), (5, 9, 3), (9, 10, 1)]
    t.assign(3, 7, 5)
    assert t.runs() == [(0, 2, 1), (2, 3, 2), (3, 7, 5), (7, 9, 3), (9, 10, 1)]
    assert t.range_sum(1, 8) == 26
    t.add(0, 4, 1)
    assert t.to_list() == [2, 2, 3, 6, 5, 5, 5, 3, 3, 1]
    assert t.runs()[:5] == [(0, 1, 2), (1, 2, 2), (2, 3, 3), (3, 4, 6), (4, 7, 5)]
    assert t.kth_smallest(0, 10, 5) == 3
    t.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        ChthollyTree([])
    t = ChthollyTree([7])
    t.assign(0, 1, 3)
    assert t.runs() == [(0, 1, 3)]
    assert t.range_sum(0, 1) == 3 and t.kth_smallest(0, 1, 1) == 3
    with pytest.raises(IndexError):
        t.assign(0, 0, 1)
    with pytest.raises(IndexError):
        t.add(0, 2, 1)
    with pytest.raises(ValueError):
        t.kth_smallest(0, 1, 2)
    u = ChthollyTree(list(range(50)))
    assert len(u.runs()) == 50
    u.assign(0, 50, 0)
    assert u.runs() == [(0, 50, 0)]
    u.assign(10, 20, 1)
    assert len(u.runs()) == 3
    u.check_invariant()


def test_random_against_brute_force() -> None:
    rng = random.Random(896)
    for _ in range(500):
        n = rng.randint(1, 30)
        a = [rng.randint(0, 5) for _ in range(n)]
        t = ChthollyTree(a)
        for _ in range(rng.randint(1, 30)):
            l = rng.randrange(n)
            r = rng.randint(l + 1, n)
            op = rng.randrange(4)
            if op == 0:
                v = rng.randint(-5, 5)
                t.assign(l, r, v)
                a[l:r] = [v] * (r - l)
            elif op == 1:
                d = rng.randint(-3, 3)
                t.add(l, r, d)
                for k in range(l, r):
                    a[k] += d
            elif op == 2:
                assert t.range_sum(l, r) == sum(a[l:r])
            else:
                k = rng.randint(1, r - l)
                assert t.kth_smallest(l, r, k) == sorted(a[l:r])[k - 1]
            t.check_invariant()
            assert t.to_list() == a
