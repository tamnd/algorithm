# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counting-sort/. The authors are listed in prov/FQMV6V.jsonl.

import random

from counting_sort import counting_sort


def test_example() -> None:
    assert counting_sort([2, 5, 3, 0, 2, 3, 0, 3], 6) == [0, 0, 2, 2, 3, 3, 3, 5]


def test_edges() -> None:
    assert counting_sort([], 1) == []
    assert counting_sort([0], 1) == [0]
    assert counting_sort([4, 4, 4], 5) == [4, 4, 4]
    assert counting_sort([3, 2, 1, 0], 4) == [0, 1, 2, 3]
    assert counting_sort([0, 9], 10) == [0, 9]


def test_stable() -> None:
    a = [(2, "a"), (1, "b"), (2, "c"), (0, "d"), (1, "e"), (2, "f")]
    out = counting_sort(a, 3, key=lambda p: p[0])
    assert out == sorted(a, key=lambda p: p[0])
    assert [t for _, t in out] == ["d", "b", "e", "a", "c", "f"]


def test_input_unchanged() -> None:
    a = [3, 1, 2]
    counting_sort(a, 4)
    assert a == [3, 1, 2]


def test_random_against_sorted() -> None:
    rng = random.Random(8021)
    for _ in range(600):
        k = rng.randint(1, 20)
        a = [(rng.randrange(k), j) for j in range(rng.randint(0, 50))]
        assert counting_sort(a, k, key=lambda p: p[0]) == sorted(a, key=lambda p: p[0])
