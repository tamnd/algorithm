# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-merge-sort/. The authors are listed in prov/V917JH.jsonl.

import random

import pytest

from external_merge_sort import external_merge_sort


def passes(n: int, m: int, b: int) -> int:
    k = m // b - 1
    r = -(-n // m)
    p = 0
    while r > 1:
        r = -(-r // k)
        p += 1
    return p


def test_example() -> None:
    f = [41, 7, 63, 18, 90, 2, 55, 34, 12, 77, 29, 5, 68, 23, 81, 46, 9, 60]
    want = sorted(f)
    ios = external_merge_sort(f, 6, 2)
    assert f == want
    assert ios == 18 + 12 + 18


def test_edges() -> None:
    a: list[int] = []
    assert external_merge_sort(a, 6, 2) == 0 and a == []
    a = [5]
    assert external_merge_sort(a, 6, 2) == 2 and a == [5]
    a = [3] * 7
    external_merge_sort(a, 6, 2)
    assert a == [3] * 7
    a = list(range(20, 0, -1))
    external_merge_sort(a, 6, 2)
    assert a == list(range(1, 21))
    a = list(range(50))
    assert external_merge_sort(a) > 0 and a == list(range(50))
    with pytest.raises(ValueError):
        external_merge_sort([1, 2], 4, 2)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(7)
    a = [Key(rng.randint(0, 3), i) for i in range(40)]
    want = sorted((x.k, x.tag) for x in a)
    external_merge_sort(a, 6, 2)
    assert [(x.k, x.tag) for x in a] == want


def test_random_against_sorted() -> None:
    rng = random.Random(4417)
    for _ in range(600):
        n = rng.randint(0, 120)
        b = rng.randint(1, 4)
        m = b * rng.randint(3, 6)
        f = [rng.randint(-30, 30) for _ in range(n)]
        want = sorted(f)
        ios = external_merge_sort(f, m, b)
        assert f == want
        assert ios <= 2 * (-(-n // b)) * (1 + passes(n, m, b))
