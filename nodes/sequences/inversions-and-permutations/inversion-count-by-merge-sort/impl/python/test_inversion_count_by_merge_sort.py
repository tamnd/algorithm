# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inversion-count-by-merge-sort/. The authors are listed in prov/GBRJQD.jsonl.

import random

from inversion_count_by_merge_sort import count_inversions, smaller_to_the_right, sort_and_count


def brute(a: list[int]) -> int:
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def test_example() -> None:
    a = [7, 5, 3, 1, 8, 6, 4, 2]
    assert sort_and_count(a) == 18
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]
    assert count_inversions([2, 4, 1, 3, 5]) == 3


def test_edges() -> None:
    assert count_inversions([]) == 0
    assert count_inversions([5]) == 0
    assert count_inversions([1, 2, 3, 4]) == 0
    assert count_inversions([4, 3, 2, 1]) == 6
    assert count_inversions([2, 2, 2, 2]) == 0
    assert count_inversions([2, 2, 1]) == 2
    assert count_inversions([1, 3, 2, 3, 1]) == 4


def test_large_count_is_exact() -> None:
    n = 70000
    assert count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2


def test_input_kept() -> None:
    a = [3, 1, 2]
    assert count_inversions(a) == 2
    assert a == [3, 1, 2]


def test_subrange() -> None:
    a = [9, 3, 2, 1, 0]
    assert sort_and_count(a, 1, 4) == 3
    assert a == [9, 1, 2, 3, 0]


def test_random_against_brute_force() -> None:
    rng = random.Random(4417)
    for _ in range(600):
        a = [rng.randint(0, 12) for _ in range(rng.randint(0, 40))]
        b = list(a)
        assert sort_and_count(b) == brute(a)
        assert b == sorted(a)
        want = [sum(1 for q in range(p + 1, len(a)) if a[q] < a[p]) for p in range(len(a))]
        assert smaller_to_the_right(a) == want
