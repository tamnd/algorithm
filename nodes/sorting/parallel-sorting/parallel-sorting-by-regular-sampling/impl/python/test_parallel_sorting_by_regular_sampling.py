# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-sorting-by-regular-sampling/. The authors are listed in prov/6H7AM2.jsonl.

import random

import pytest

from parallel_sorting_by_regular_sampling import psrs


EXAMPLE = [15, 46, 48, 93, 39, 6, 72, 91, 14, 36, 69, 40, 89, 61, 97, 12, 21, 54, 53, 97, 84, 58, 32, 27, 33, 72, 20]


def test_example() -> None:
    out, sizes = psrs(EXAMPLE, 3)
    assert out == sorted(EXAMPLE)
    assert sizes == [5, 7, 15]


def test_edges() -> None:
    assert psrs([], 3) == ([], [0, 0, 0])
    assert psrs([4], 2)[0] == [4]
    assert psrs([3, 1, 2], 1) == ([1, 2, 3], [3])
    with pytest.raises(ValueError):
        psrs([1], 0)


def test_bucket_bound_distinct_keys() -> None:
    rng = random.Random(4)
    for p in (2, 3, 4, 5, 8):
        n = p * p * rng.randint(1, 6)
        for _ in range(200):
            a = rng.sample(range(10 * n), n)
            out, sizes = psrs(a, p)
            assert out == sorted(a)
            assert max(sizes) <= 2 * n // p - p


def test_equal_keys_are_balanced_by_tags() -> None:
    out, sizes = psrs([5] * 64, 4)
    assert out == [5] * 64
    assert max(sizes) <= 2 * 64 // 4 - 4


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(9)
    a = [Key(rng.randint(0, 3), i) for i in range(100)]
    out, _ = psrs(a, 4)
    assert [(x.k, x.tag) for x in out] == sorted((x.k, x.tag) for x in a)


def test_random_any_size() -> None:
    rng = random.Random(5)
    for _ in range(300):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 70))]
        out, _ = psrs(a, rng.randint(1, 9))
        assert out == sorted(a)
