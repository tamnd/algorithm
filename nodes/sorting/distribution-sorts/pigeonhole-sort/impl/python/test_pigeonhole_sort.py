# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pigeonhole-sort/. The authors are listed in prov/Y6SQW0.jsonl.

import random

from pigeonhole_sort import pigeonhole_sort


def test_example() -> None:
    a = [8, 3, 2, 7, 4, 6, 8, 3]
    pigeonhole_sort(a)
    assert a == [2, 3, 3, 4, 6, 7, 8, 8]


def test_edges() -> None:
    for a in ([], [5], [1, 1, 1], [-3, 4, -3, 0], [2, 1]):
        b = list(a)
        pigeonhole_sort(b)
        assert b == sorted(a)


def test_stable() -> None:
    a = [(3, "a"), (1, "b"), (3, "c"), (2, "d"), (1, "e")]
    pigeonhole_sort(a, key=lambda p: p[0])
    assert [t for _, t in a] == ["b", "e", "d", "a", "c"]


def test_random_against_sorted() -> None:
    rng = random.Random(7712)
    for _ in range(600):
        a = [(rng.randint(-20, 20), j) for j in range(rng.randint(0, 50))]
        b = list(a)
        pigeonhole_sort(b, key=lambda p: p[0])
        assert b == sorted(a, key=lambda p: p[0])
