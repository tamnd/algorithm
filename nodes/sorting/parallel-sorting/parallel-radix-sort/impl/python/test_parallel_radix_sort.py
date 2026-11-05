# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-radix-sort/. The authors are listed in prov/GHWWJ6.jsonl.

import random

import pytest

from parallel_radix_sort import parallel_radix_sort, radix_pass, split_radix_sort


EXAMPLE = [170, 45, 75, 90, 802, 24, 2, 66]


def test_example_passes() -> None:
    first = radix_pass(EXAMPLE, 0, 10, 2)
    assert first == [170, 90, 802, 2, 24, 45, 75, 66]
    second = radix_pass(first, 1, 10, 2)
    assert second == [802, 2, 24, 45, 66, 170, 75, 90]
    assert radix_pass(second, 2, 10, 2) == sorted(EXAMPLE)


def test_example() -> None:
    assert parallel_radix_sort(EXAMPLE, 10, 2) == sorted(EXAMPLE)
    assert split_radix_sort(EXAMPLE, 10) == sorted(EXAMPLE)


def test_edges() -> None:
    assert parallel_radix_sort([]) == []
    assert parallel_radix_sort([0]) == [0]
    assert parallel_radix_sort([3, 3, 3], 2, 5) == [3, 3, 3]
    with pytest.raises(ValueError):
        parallel_radix_sort([-1])


def test_pass_is_stable() -> None:
    a = [13, 23, 3, 41, 11, 33, 1]
    assert radix_pass(a, 0, 10, 3) == [41, 11, 1, 13, 23, 3, 33]


def test_block_count_does_not_change_result() -> None:
    rng = random.Random(4)
    a = [rng.randrange(10**6) for _ in range(500)]
    want = sorted(a)
    for p in (1, 2, 3, 7, 64, 500, 600):
        for radix in (2, 10, 16, 256):
            assert parallel_radix_sort(a, radix, p) == want


def test_random_against_sorted() -> None:
    rng = random.Random(12)
    for _ in range(200):
        a = [rng.randrange(1 << 16) for _ in range(rng.randint(0, 60))]
        assert parallel_radix_sort(a, 16, rng.randint(1, 9)) == sorted(a)
        assert split_radix_sort(a, 16) == sorted(a)
