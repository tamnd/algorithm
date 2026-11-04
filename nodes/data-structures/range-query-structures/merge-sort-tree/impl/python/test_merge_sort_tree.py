# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-sort-tree/. The authors are listed in prov/8KPVMD.jsonl.

import random

import pytest

from merge_sort_tree import MergeSortTree


def test_example() -> None:
    a = [5, 2, 8, 6, 3, 7, 9, 1]
    t = MergeSortTree(a)
    t.check_invariant()
    assert t.lists[2] == [2, 5, 6, 8]
    assert t.lists[3] == [1, 3, 7, 9]
    assert t.lists[4:8] == [[2, 5], [6, 8], [3, 7], [1, 9]]
    assert t.lists[1] == [1, 2, 3, 5, 6, 7, 8, 9]
    assert t.count_less(1, 7, 7) == 3
    assert t.count_leq(1, 7, 6) == 3
    assert t.kth_smallest(1, 7, 3) == 6
    assert t.successor(1, 7, 4) == 6
    assert t.successor(1, 7, 10) is None


def test_edges() -> None:
    t = MergeSortTree([])
    t.check_invariant()
    assert t.count_less(0, 0, 5) == 0
    assert t.successor(0, 0, 5) is None
    with pytest.raises(ValueError):
        t.kth_smallest(0, 0, 1)
    t = MergeSortTree([4])
    assert t.kth_smallest(0, 1, 1) == 4
    assert t.count_leq(0, 1, 4) == 1
    assert t.count_less(0, 1, 4) == 0
    t = MergeSortTree([2, 2, 2, 1, 1])
    t.check_invariant()
    assert [t.kth_smallest(0, 5, k) for k in range(1, 6)] == [1, 1, 2, 2, 2]
    with pytest.raises(IndexError):
        t.count_less(3, 2, 0)
    with pytest.raises(IndexError):
        t.count_less(0, 6, 0)
    with pytest.raises(ValueError):
        t.kth_smallest(1, 3, 3)


def test_random() -> None:
    rng = random.Random(8)
    for _ in range(600):
        n = rng.randint(1, 20)
        a = [rng.randint(-5, 5) for _ in range(n)]
        t = MergeSortTree(a)
        t.check_invariant()
        for _ in range(5):
            l = rng.randint(0, n)
            r = rng.randint(l, n)
            x = rng.randint(-6, 6)
            part = a[l:r]
            assert t.count_less(l, r, x) == sum(1 for y in part if y < x)
            assert t.count_leq(l, r, x) == sum(1 for y in part if y <= x)
            big = [y for y in part if y >= x]
            assert t.successor(l, r, x) == (min(big) if big else None)
            if part:
                k = rng.randint(1, len(part))
                assert t.kth_smallest(l, r, k) == sorted(part)[k - 1]
