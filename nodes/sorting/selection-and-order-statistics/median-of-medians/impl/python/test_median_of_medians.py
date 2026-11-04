# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/median-of-medians/. The authors are listed in prov/A5DV6Z.jsonl.

import random

import pytest

from median_of_medians import lower_median, median_of_medians


def test_example() -> None:
    a = [12, 3, 45, 7, 29, 18, 1, 33, 26, 9, 40, 15, 21, 4, 37]
    assert median_of_medians(a, 8) == 18
    assert [median_of_medians(a, k) for k in range(1, 16)] == sorted(a)


def test_group_medians() -> None:
    assert lower_median([12, 3, 45, 7, 29]) == 12
    assert lower_median([4, 1]) == 1
    assert lower_median([9]) == 9


def test_edges() -> None:
    assert median_of_medians([5], 1) == 5
    assert median_of_medians([2, 2, 2, 2, 2, 2, 2], 4) == 2
    assert median_of_medians(list(range(100, 0, -1)), 1) == 1
    assert median_of_medians(list(range(100)), 100) == 99
    with pytest.raises(ValueError):
        median_of_medians([], 1)
    with pytest.raises(ValueError):
        median_of_medians([1], 0)


def test_input_unchanged() -> None:
    a = [3, 1, 2, 5, 4, 9, 7, 8, 6]
    b = list(a)
    median_of_medians(a, 5)
    assert a == b


def test_pivot_split_bound() -> None:
    rng = random.Random(55)
    for _ in range(300):
        n = rng.randint(6, 200)
        s = [rng.randint(0, 30) for _ in range(n)]
        meds = [lower_median(s[i : i + 5]) for i in range(0, n, 5)]
        x = sorted(meds)[(len(meds) + 1) // 2 - 1]
        less = sum(1 for v in s if v < x)
        greater = sum(1 for v in s if v > x)
        assert 10 * less <= 7 * n + 20 and 10 * greater <= 7 * n + 20


def test_random_against_sorted() -> None:
    rng = random.Random(4417)
    for _ in range(600):
        n = rng.randint(1, 120)
        a = [rng.randint(-40, 40) for _ in range(n)]
        k = rng.randint(1, n)
        assert median_of_medians(a, k) == sorted(a)[k - 1]
