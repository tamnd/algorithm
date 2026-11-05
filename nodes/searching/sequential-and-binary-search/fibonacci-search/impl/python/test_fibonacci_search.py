# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-search/. The authors are listed in prov/8R17S9.jsonl.

import bisect
import random

from fibonacci_search import fibonacci_search

A = [3, 8, 11, 15, 19, 23, 27, 31, 35, 40, 44, 50]


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
    assert fibonacci_search(A, 40) == 9
    assert fibonacci_search(A, 12) == -1
    assert fibonacci_search(A, 3) == 0
    assert fibonacci_search(A, 50) == 11
    assert fibonacci_search(A, 2) == -1
    assert fibonacci_search(A, 51) == -1


def test_edges() -> None:
    assert fibonacci_search([], 1) == -1
    assert fibonacci_search([4], 4) == 0
    assert fibonacci_search([4], 5) == -1
    assert fibonacci_search([4], 3) == -1
    assert fibonacci_search([4, 4], 4) == 0
    assert fibonacci_search([1, 4], 4) == 1


def test_every_size_position_and_gap() -> None:
    for n in range(0, 90):
        a = list(range(0, 2 * n, 2))
        for i in range(n):
            assert fibonacci_search(a, 2 * i) == i
        for g in range(-1, 2 * n + 1, 2):
            assert fibonacci_search(a, g) == -1


def test_first_of_duplicates() -> None:
    for n in range(1, 40):
        for start in range(n):
            a = [0] * start + [1] * (n - start)
            assert fibonacci_search(a, 1) == start


def test_comparison_bound() -> None:
    fib = [0, 1]
    while fib[-1] < 20000:
        fib.append(fib[-1] + fib[-2])
    for n in [1, 2, 3, 12, 20, 143, 986, 1000]:
        k = next(j for j in range(1, len(fib)) if fib[j] - 1 >= n)
        a = [Key(2 * i) for i in range(n)]
        worst = 0
        for v in range(-1, 2 * n + 1):
            Key.count = 0
            fibonacci_search(a, Key(v))
            worst = max(worst, Key.count)
        assert worst <= k - 1


def test_random_against_bisect() -> None:
    rng = random.Random(1960)
    for _ in range(3000):
        a = sorted(rng.randint(-15, 15) for _ in range(rng.randint(0, 50)))
        x = rng.randint(-17, 17)
        i = bisect.bisect_left(a, x)
        want = i if i < len(a) and a[i] == x else -1
        assert fibonacci_search(a, x) == want


def test_strings() -> None:
    words = ["ant", "bee", "cat", "dog", "eel", "fox"]
    for i, w in enumerate(words):
        assert fibonacci_search(words, w) == i
    assert fibonacci_search(words, "cow") == -1
