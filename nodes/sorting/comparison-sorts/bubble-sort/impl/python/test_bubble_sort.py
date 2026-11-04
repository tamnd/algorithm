# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bubble-sort/. The authors are listed in prov/JS56R4.jsonl.

import itertools
import random

from bubble_sort import bubble_sort


def test_example() -> None:
    a = [5, 1, 4, 2, 8, 0, 3]
    assert bubble_sort(a) == 5
    assert a == [0, 1, 2, 3, 4, 5, 8]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)]):
        b = list(a)
        bubble_sort(b)
        assert b == sorted(a)


def test_sorted_input_takes_one_pass() -> None:
    a = list(range(20))
    assert bubble_sort(a) == 1


def test_passes_bound() -> None:
    for n in range(1, 7):
        for p in itertools.permutations(range(n)):
            m = max([sum(1 for i in range(p.index(v)) if p[i] > v) for v in p])
            b = list(p)
            passes = bubble_sort(b)
            assert b == list(range(n))
            assert m <= passes <= m + 1


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    a = [Key(2, "a"), Key(1, "b"), Key(2, "c"), Key(1, "d")]
    bubble_sort(a)
    assert [x.tag for x in a] == ["b", "d", "a", "c"]


def test_random_against_sorted() -> None:
    rng = random.Random(1956)
    for _ in range(600):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 50))]
        b = list(a)
        bubble_sort(b)
        assert b == sorted(a)
