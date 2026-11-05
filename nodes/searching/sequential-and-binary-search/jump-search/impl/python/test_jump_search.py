# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jump-search/. The authors are listed in prov/FX08EH.jsonl.

import bisect
import random

from jump_search import jump_search

A = [3, 8, 11, 15, 19, 23, 27, 31, 35, 40, 44, 50, 57, 62, 68, 71]


def test_example() -> None:
    assert jump_search(A, 57) == 12
    assert jump_search(A, 20) == -1
    assert jump_search(A, 80) == -1
    assert jump_search(A, 3) == 0
    assert jump_search(A, 71) == 15
    assert jump_search(A, 1) == -1


def test_edges() -> None:
    assert jump_search([], 1) == -1
    assert jump_search([4], 4) == 0
    assert jump_search([4], 5) == -1
    assert jump_search([4], 3) == -1
    assert jump_search([2, 2, 2, 2, 2], 2) == 0


def test_first_occurrence_across_block_boundary() -> None:
    # n = 9, m = 3: the copies of 5 start in the first block and fill the second.
    a = [1, 2, 5, 5, 5, 5, 6, 7, 8]
    assert jump_search(a, 5) == 2
    a = [1, 2, 3, 5, 5, 5, 5, 7, 8]
    assert jump_search(a, 5) == 3


def test_every_position_and_gap() -> None:
    for n in range(0, 70):
        a = list(range(0, 2 * n, 2))
        for i in range(n):
            assert jump_search(a, 2 * i) == i
        for g in range(-1, 2 * n + 1, 2):
            assert jump_search(a, g) == -1


def test_comparison_bound() -> None:
    class Key:
        count = 0

        def __init__(self, v: int) -> None:
            self.v = v

        def __lt__(self, other: "Key") -> bool:
            Key.count += 1
            return self.v < other.v

        def __eq__(self, other: object) -> bool:
            Key.count += 1
            return isinstance(other, Key) and self.v == other.v

    for n in [1, 2, 5, 16, 100, 1000]:
        a = [Key(2 * i) for i in range(n)]
        m = max(1, int(n**0.5))
        while m * m > n:
            m -= 1
        bound = -(-n // m) + m
        worst = 0
        for v in range(-1, 2 * n + 1):
            Key.count = 0
            jump_search(a, Key(v))
            worst = max(worst, Key.count)
        assert worst <= bound
        if n == 16:
            assert worst == 8


def test_random_against_bisect() -> None:
    rng = random.Random(6021)
    for _ in range(3000):
        a = sorted(rng.randint(-15, 15) for _ in range(rng.randint(0, 40)))
        x = rng.randint(-17, 17)
        i = bisect.bisect_left(a, x)
        want = i if i < len(a) and a[i] == x else -1
        assert jump_search(a, x) == want


def test_strings() -> None:
    assert jump_search(["ant", "bee", "cat", "dog", "eel"], "dog") == 3
