# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-sort/. The authors are listed in prov/HB6K6X.jsonl.

import random

from radix_sort import radix_sort


def test_example() -> None:
    a = [329, 457, 657, 839, 436, 720, 355]
    assert radix_sort(a, 10) == [329, 355, 436, 457, 657, 720, 839]


def test_edges() -> None:
    assert radix_sort([], 10) == []
    assert radix_sort([0], 10) == [0]
    assert radix_sort([0, 0, 0], 2) == [0, 0, 0]
    assert radix_sort([10, 9, 100, 1], 10) == [1, 9, 10, 100]
    big = [2**64 - 1, 0, 2**63, 1]
    assert radix_sort(big) == sorted(big)


def test_stable() -> None:
    a = [(5, "a"), (3, "b"), (5, "c"), (13, "d"), (3, "e")]
    out = radix_sort(a, 2, key=lambda p: p[0])
    assert [t for _, t in out] == ["b", "e", "a", "c", "d"]


def test_random_against_sorted() -> None:
    rng = random.Random(4417)
    for _ in range(600):
        b = rng.choice([2, 3, 10, 16, 256])
        a = [(rng.randrange(0, 10 ** rng.randint(1, 6)), j) for j in range(rng.randint(0, 40))]
        assert radix_sort(a, b, key=lambda p: p[0]) == sorted(a, key=lambda p: p[0])
