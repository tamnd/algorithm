# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniform-binary-search/. The authors are listed in prov/MG89TJ.jsonl.

import bisect
import random

from uniform_binary_search import delta_table, three_way_uniform_search, uniform_binary_search

A = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]


def first_index(a: list[int], x: int) -> int:
    i = bisect.bisect_left(a, x)
    return i if i < len(a) and a[i] == x else -1


def test_example() -> None:
    assert uniform_binary_search(A, 14) == 6
    assert uniform_binary_search(A, 19) == -1
    assert uniform_binary_search(A, 2) == 0
    assert uniform_binary_search(A, 20) == 9
    assert uniform_binary_search(A, 1) == -1
    assert uniform_binary_search(A, 21) == -1


def test_edges() -> None:
    assert uniform_binary_search([], 3) == -1
    assert uniform_binary_search([3], 3) == 0
    assert uniform_binary_search([3], 2) == -1
    assert uniform_binary_search([3], 4) == -1
    assert uniform_binary_search([3, 3], 3) == 0
    assert uniform_binary_search([1, 3], 3) == 1
    assert uniform_binary_search([5, 5, 5, 5, 5, 5, 5, 5], 5) == 0


def test_powers_of_two_and_neighbours() -> None:
    # n = p, p - 1 and p + 1 are the cases where the first offset n - p is 0, p - 1 or 1.
    for k in range(0, 8):
        for n in {(1 << k) - 1, 1 << k, (1 << k) + 1}:
            a = list(range(0, 2 * n, 2))
            for i in range(n):
                assert uniform_binary_search(a, 2 * i) == i
            for g in range(-1, 2 * n + 1, 2):
                assert uniform_binary_search(a, g) == -1


def test_exact_comparison_count() -> None:
    class Key:
        lt = 0

        def __init__(self, v: int) -> None:
            self.v = v

        def __lt__(self, other: "Key") -> bool:
            Key.lt += 1
            return self.v < other.v

        def __eq__(self, other: object) -> bool:
            return isinstance(other, Key) and self.v == other.v

    for n in range(1, 130):
        a = [Key(2 * i) for i in range(n)]
        for v in range(-1, 2 * n + 1):
            Key.lt = 0
            uniform_binary_search(a, Key(v))
            assert Key.lt == n.bit_length()


def test_delta_table() -> None:
    assert delta_table(10) == [5, 3, 1, 1, 0]
    assert delta_table(16) == [8, 4, 2, 1, 1, 0]
    assert delta_table(1) == [1, 0]


def test_three_way_every_n() -> None:
    for n in range(0, 200):
        a = list(range(0, 2 * n, 2))
        for i in range(n):
            assert three_way_uniform_search(a, 2 * i) == i
        for g in range(-1, 2 * n + 1, 2):
            assert three_way_uniform_search(a, g) == -1


def test_random_against_bisect() -> None:
    rng = random.Random(8803)
    for _ in range(3000):
        a = sorted(rng.randint(-12, 12) for _ in range(rng.randint(0, 40)))
        x = rng.randint(-14, 14)
        assert uniform_binary_search(a, x) == first_index(a, x)
        r = three_way_uniform_search(a, x)
        assert (r == -1) == (x not in a)
        assert r == -1 or a[r] == x


def test_strings() -> None:
    words = ["ant", "bee", "cat", "dog", "eel", "fox"]
    assert uniform_binary_search(words, "eel") == 4
    assert uniform_binary_search(words, "cow") == -1
