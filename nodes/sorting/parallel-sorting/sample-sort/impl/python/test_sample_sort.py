# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sample-sort/. The authors are listed in prov/X40DBH.jsonl.

import math
import random

import pytest

from sample_sort import sample_sort


def test_example() -> None:
    a = [41, 7, 93, 25, 60, 12, 88, 3, 54, 31, 76, 19]
    out, sizes = sample_sort(a, 3, 2, random.Random(1))
    assert out == sorted(a)
    assert sum(sizes) == len(a) and len(sizes) == 3


def test_edges() -> None:
    assert sample_sort([], 4) == ([], [0, 0, 0, 0])
    assert sample_sort([5], 4)[0] == [5]
    assert sample_sort([2, 1], 1)[0] == [1, 2]
    with pytest.raises(ValueError):
        sample_sort([1], 0)


def test_bucket_bound_with_high_probability() -> None:
    rng = random.Random(8)
    for n, p in ((2000, 8), (5000, 16), (20000, 32)):
        a = rng.sample(range(10 * n), n)
        out, sizes = sample_sort(a, p, None, rng)
        assert out == sorted(a)
        assert max(sizes) <= math.ceil(2 * n / p)


def test_all_equal_keys_are_spread() -> None:
    out, sizes = sample_sort([7] * 4000, 8, None, random.Random(3))
    assert out == [7] * 4000
    assert max(sizes) <= 1000


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(2)
    a = [Key(rng.randint(0, 4), i) for i in range(300)]
    out, _ = sample_sort(a, 5, 4, rng)
    assert [(x.k, x.tag) for x in out] == sorted((x.k, x.tag) for x in a)


def test_random_against_sorted() -> None:
    rng = random.Random(10)
    for _ in range(200):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(1, 90))]
        out, _ = sample_sort(a, rng.randint(1, 8), rng.randint(1, 5), rng)
        assert out == sorted(a)
