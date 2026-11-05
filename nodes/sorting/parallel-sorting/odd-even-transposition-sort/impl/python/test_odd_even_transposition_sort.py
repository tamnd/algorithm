# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/odd-even-transposition-sort/. The authors are listed in prov/QRMS1F.jsonl.

import itertools
import random

from odd_even_transposition_sort import odd_even_transposition_sort, round_pairs, rounds_until_sorted


def test_example() -> None:
    a = [6, 3, 8, 1, 7, 2, 5, 4]
    odd_even_transposition_sort(a)
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]
    assert rounds_until_sorted([6, 3, 8, 1, 7, 2, 5, 4]) == 5


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [1, 2, 3]):
        b = list(a)
        odd_even_transposition_sort(b)
        assert b == sorted(a)


def test_size_is_n_choose_2() -> None:
    for n in range(1, 30):
        assert sum(len(round_pairs(n, t)) for t in range(1, n + 1)) == n * (n - 1) // 2


def test_all_zero_one_inputs() -> None:
    for n in range(1, 13):
        for bits in itertools.product([0, 1], repeat=n):
            assert rounds_until_sorted(list(bits)) <= n


def test_n_rounds_are_needed() -> None:
    for n in range(3, 12, 2):
        assert rounds_until_sorted(list(range(1, n)) + [0]) == n
    assert rounds_until_sorted([2, 3, 4, 5, 6, 7, 0, 1]) == 8


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    a = [Key(2, "a"), Key(1, "b"), Key(2, "c"), Key(1, "d"), Key(2, "e")]
    odd_even_transposition_sort(a)
    assert [x.tag for x in a] == ["b", "d", "a", "c", "e"]


def test_random_against_sorted() -> None:
    rng = random.Random(7)
    for _ in range(300):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 40))]
        b = list(a)
        odd_even_transposition_sort(b)
        assert b == sorted(a)
