# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-sort/. The authors are listed in prov/FAY1AX.jsonl.

import itertools
import random

from cycle_sort import cycle_sort


def misplaced(a: list[int]) -> int:
    s = sorted(a)
    return sum(1 for x, y in zip(a, s) if x != y)


def test_example() -> None:
    a = [3, 0, 4, 1, 2]
    assert cycle_sort(a) == 5
    assert a == [0, 1, 2, 3, 4]


def test_example_with_duplicates() -> None:
    a = [2, 4, 1, 2, 0, 4]
    assert cycle_sort(a) == 4
    assert a == [0, 1, 2, 2, 4, 4]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)], [2**63 - 1, 0, -(2**63), 2**63 - 1]):
        b = list(a)
        cycle_sort(b)
        assert b == sorted(a)


def test_sorted_input_has_no_writes() -> None:
    a = list(range(50))
    assert cycle_sort(a) == 0
    assert a == list(range(50))


def test_writes_are_minimal_on_permutations() -> None:
    for n in range(0, 7):
        for p in itertools.permutations(range(n)):
            b = list(p)
            fixed = sum(1 for i in range(n) if p[i] == i)
            assert cycle_sort(b) == n - fixed
            assert b == list(range(n))


def test_writes_are_minimal_with_duplicates() -> None:
    rng = random.Random(7)
    for _ in range(600):
        a = [rng.randint(0, 4) for _ in range(rng.randint(0, 14))]
        b = list(a)
        assert cycle_sort(b) == misplaced(a)
        assert b == sorted(a)


def test_not_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    a = [Key(1, "a"), Key(1, "b"), Key(0, "c")]
    cycle_sort(a)
    assert [x.k for x in a] == [0, 1, 1]
    assert [x.tag for x in a] == ["c", "b", "a"]


def test_random_against_sorted() -> None:
    rng = random.Random(1990)
    for _ in range(600):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 50))]
        b = list(a)
        cycle_sort(b)
        assert b == sorted(a)


def test_strings() -> None:
    a = ["pear", "fig", "apple", "fig", "kiwi"]
    cycle_sort(a)
    assert a == ["apple", "fig", "fig", "kiwi", "pear"]
