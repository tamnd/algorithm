# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inversion-count-with-fenwick-tree/. The authors are listed in prov/XH0RVP.jsonl.

import random

from inversion_count_with_fenwick_tree import count_inversions_bit, prefix_inversion_counts


def brute(a: list) -> int:
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def test_example() -> None:
    assert count_inversions_bit([3, 1, 6, 2, 5, 4]) == 6
    assert prefix_inversion_counts([3, 1, 6, 2, 5, 4]) == [0, 1, 1, 3, 4, 6]


def test_repeated_values() -> None:
    assert count_inversions_bit([40, 10, 40, 30, 10]) == 6
    assert count_inversions_bit([7, 7, 7]) == 0
    assert count_inversions_bit([2, 2, 1]) == 2


def test_edges() -> None:
    assert count_inversions_bit([]) == 0
    assert count_inversions_bit([1]) == 0
    assert count_inversions_bit(list(range(10))) == 0
    assert count_inversions_bit(list(range(10, 0, -1))) == 45
    assert count_inversions_bit([1.5, -2.0, 10**18, -(10**18)]) == 4
    assert count_inversions_bit(["b", "a", "c"]) == 1


def test_random_against_brute_force() -> None:
    rng = random.Random(9103)
    for _ in range(600):
        a = [rng.randint(-5, 15) for _ in range(rng.randint(0, 40))]
        assert count_inversions_bit(a) == brute(a)
        assert prefix_inversion_counts(a) == [brute(a[: j + 1]) for j in range(len(a))]
