# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-search/. The authors are listed in prov/V34DA8.jsonl.

import bisect
import random

from exponential_search import exponential_search

A = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91, 99, 104, 120]


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


def test_example() -> None:
    assert exponential_search(A, 23) == 5
    assert exponential_search(A, 72) == 8
    assert exponential_search(A, 2) == 0
    assert exponential_search(A, 120) == 12
    assert exponential_search(A, 1) == -1
    assert exponential_search(A, 121) == -1
    assert exponential_search(A, 13) == -1


def test_edges() -> None:
    assert exponential_search([], 1) == -1
    assert exponential_search([4], 4) == 0
    assert exponential_search([4], 5) == -1
    assert exponential_search([4], 3) == -1
    assert exponential_search([7, 7, 7, 7, 7, 7, 7, 7, 7], 7) == 0


def test_first_occurrence_at_powers_of_two() -> None:
    # The first copy sits exactly at lo = b / 2 or at hi = b - 1.
    for n in range(1, 40):
        for start in range(n):
            a = [0] * start + [1] * (n - start)
            assert exponential_search(a, 1) == start
            assert exponential_search(a, 0) == (0 if start > 0 else -1)


def test_every_position_and_gap() -> None:
    for n in range(0, 70):
        a = list(range(0, 2 * n, 2))
        for i in range(n):
            assert exponential_search(a, 2 * i) == i
        for g in range(-1, 2 * n + 1, 2):
            assert exponential_search(a, g) == -1


def test_comparison_bound() -> None:
    for n in [1, 2, 3, 13, 64, 100, 1000]:
        a = [Key(2 * i) for i in range(n)]
        for v in range(-1, 2 * n + 1):
            lb = (v + 1) // 2
            Key.count = 0
            exponential_search(a, Key(v))
            bound = 2 if lb == 0 else 2 * (lb.bit_length() - 1) + 3
            assert Key.count <= bound


def test_counts_far_from_end() -> None:
    a = [Key(i) for i in range(10**5)]
    for i, want in [(0, 2), (1, 3), (2, 5), (7, 7), (8, 9), (100, 15), (1000, 21)]:
        Key.count = 0
        assert exponential_search(a, Key(i)) == i
        assert Key.count == want


def test_random_against_bisect() -> None:
    rng = random.Random(4417)
    for _ in range(3000):
        a = sorted(rng.randint(-15, 15) for _ in range(rng.randint(0, 50)))
        x = rng.randint(-17, 17)
        i = bisect.bisect_left(a, x)
        want = i if i < len(a) and a[i] == x else -1
        assert exponential_search(a, x) == want


def test_strings() -> None:
    assert exponential_search(["ant", "bee", "cat", "dog", "eel"], "ant") == 0
    assert exponential_search(["ant", "bee", "cat", "dog", "eel"], "fox") == -1
