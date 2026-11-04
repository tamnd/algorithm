# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shell-sort/. The authors are listed in prov/ZSYXJJ.jsonl.

import random

import pytest

from shell_sort import knuth_gaps, shell_sort


def test_example() -> None:
    a = [62, 83, 18, 53, 7, 17, 95, 86, 47, 69, 25, 28]
    assert knuth_gaps(len(a)) == [4, 1]
    four = list(a)
    for start in range(4):  # the 4-sort of the trace: sort each chain of indices start, start + 4, ...
        four[start::4] = sorted(four[start::4])
    assert four == [7, 17, 18, 28, 47, 69, 25, 53, 62, 83, 95, 86]
    shell_sort(a)
    assert a == [7, 17, 18, 25, 28, 47, 53, 62, 69, 83, 86, 95]


def test_gaps() -> None:
    assert knuth_gaps(0) == [1]
    assert knuth_gaps(13) == [4, 1]
    assert knuth_gaps(1000) == [364, 121, 40, 13, 4, 1]


def test_last_gap_must_be_one() -> None:
    with pytest.raises(ValueError):
        shell_sort([3, 2, 1], [2])


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [1, 2, 3]):
        b = list(a)
        shell_sort(b)
        assert b == sorted(a)


def test_other_gap_sequences() -> None:
    rng = random.Random(3)
    for gaps in ([1], [5, 3, 1], [7, 3, 1], [8, 4, 2, 1], [23, 10, 4, 1]):
        for _ in range(100):
            a = [rng.randint(0, 30) for _ in range(rng.randint(0, 80))]
            b = list(a)
            shell_sort(b, gaps)
            assert b == sorted(a)


def test_random_against_sorted() -> None:
    rng = random.Random(2150)
    for _ in range(500):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 200))]
        b = list(a)
        shell_sort(b)
        assert b == sorted(a)
