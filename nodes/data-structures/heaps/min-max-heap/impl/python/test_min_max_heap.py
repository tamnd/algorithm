# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-max-heap/. The authors are listed in prov/HGEHQG.jsonl.

import random

import pytest

from min_max_heap import MinMaxHeap, is_min_level

START = [8, 71, 41, 31, 10, 11, 16, 46, 51, 31, 21, 13]


def test_levels() -> None:
    assert [is_min_level(i) for i in range(16)] == [True] + [False] * 2 + [True] * 4 + [False] * 8 + [True]


def test_example() -> None:
    h = MinMaxHeap(START)
    h.check_invariant()
    assert h.a == START
    h.insert(5)
    assert h.a == [5, 71, 41, 31, 10, 8, 16, 46, 51, 31, 21, 13, 11]
    h.insert(80)
    assert h.a == [5, 71, 80, 31, 10, 8, 16, 46, 51, 31, 21, 13, 11, 41]
    assert h.find_min() == 5 and h.find_max() == 80
    assert h.delete_min() == 5
    assert h.a == [8, 71, 80, 31, 10, 11, 16, 46, 51, 31, 21, 13, 41]
    assert h.delete_max() == 80
    assert h.a == START
    h.check_invariant()


def test_small_and_empty() -> None:
    h: MinMaxHeap[int] = MinMaxHeap()
    for f in (h.find_min, h.find_max, h.delete_min, h.delete_max):
        with pytest.raises(IndexError):
            f()
    h.insert(4)
    assert h.find_min() == 4 and h.find_max() == 4
    assert h.delete_max() == 4 and h.is_empty()
    h = MinMaxHeap([2, 1])
    h.check_invariant()
    assert (h.find_min(), h.find_max()) == (1, 2)
    assert h.delete_max() == 2 and h.delete_min() == 1


def test_build_sorted_and_duplicates() -> None:
    for data in (list(range(100)), list(range(100, 0, -1)), [3] * 40, [1, 2] * 30):
        h = MinMaxHeap(data)
        h.check_invariant()
        out_lo: list[int] = []
        out_hi: list[int] = []
        while len(h):
            out_lo.append(h.delete_min())
            if len(h):
                out_hi.append(h.delete_max())
            h.check_invariant()
        assert out_lo + out_hi[::-1] == sorted(data)


def test_random_against_sorted_list() -> None:
    rng = random.Random(1986)
    for _ in range(600):
        start = [rng.randrange(-30, 30) for _ in range(rng.randrange(0, 20))]
        h = MinMaxHeap(start)
        ref = sorted(start)
        h.check_invariant()
        for _ in range(rng.randrange(1, 50)):
            op = rng.random()
            if op < 0.5:
                x = rng.randrange(-30, 30)
                h.insert(x)
                ref.append(x)
                ref.sort()
            elif ref and op < 0.75:
                assert h.find_min() == ref[0]
                assert h.delete_min() == ref.pop(0)
            elif ref:
                assert h.find_max() == ref[-1]
                assert h.delete_max() == ref.pop()
            h.check_invariant()
            assert sorted(h.a) == ref
