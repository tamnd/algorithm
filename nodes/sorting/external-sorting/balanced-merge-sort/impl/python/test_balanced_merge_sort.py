# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-merge-sort/. The authors are listed in prov/K6SD9E.jsonl.

import random

import pytest

from balanced_merge_sort import balanced_merge_sort


def ceil_log(s: int, p: int) -> int:
    k, q = 0, 1
    while q < s:
        q *= p
        k += 1
    return k


def test_example() -> None:
    f = [12, 3, 8, 1, 14, 6, 2, 11, 9, 5, 13, 4, 10, 7]
    assert balanced_merge_sort(f, 2, 4) == 3
    assert f == list(range(1, 15))


def test_edges() -> None:
    a: list[int] = []
    assert balanced_merge_sort(a) == 0 and a == []
    a = [1]
    assert balanced_merge_sort(a) == 0 and a == [1]
    a = [4, 3, 2, 1]
    assert balanced_merge_sort(a, 4, 4) == 0 and a == [1, 2, 3, 4]
    a = [5] * 9
    balanced_merge_sort(a, 2, 6)
    assert a == [5] * 9
    a = list(range(30, 0, -1))
    assert balanced_merge_sort(a, 1, 8) == 3 and a == list(range(1, 31))
    with pytest.raises(ValueError):
        balanced_merge_sort([1], 2, 3)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(3)
    for _ in range(50):
        a = [Key(rng.randint(0, 3), i) for i in range(rng.randint(0, 60))]
        want = sorted((x.k, x.tag) for x in a)
        balanced_merge_sort(a, rng.randint(1, 5), rng.randint(4, 9))
        assert [(x.k, x.tag) for x in a] == want


def test_random_against_sorted() -> None:
    rng = random.Random(1961)
    for _ in range(600):
        n = rng.randint(0, 100)
        m = rng.randint(1, 6)
        t = rng.randint(4, 10)
        f = [rng.randint(-40, 40) for _ in range(n)]
        want = sorted(f)
        passes = balanced_merge_sort(f, m, t)
        assert f == want
        assert passes == ceil_log(-(-n // m), t // 2)
