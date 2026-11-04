# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ford-johnson-algorithm/. The authors are listed in prov/311MZG.jsonl.

import itertools
import math
import random

from ford_johnson_algorithm import ford_johnson_algorithm


class Counted:
    count = 0

    def __init__(self, k: int) -> None:
        self.k = k

    def __lt__(self, other: "Counted") -> bool:
        Counted.count += 1
        return self.k < other.k


def comparisons(p: list[int]) -> int:
    a = [Counted(x) for x in p]
    Counted.count = 0
    ford_johnson_algorithm(a)
    assert [x.k for x in a] == sorted(p)
    return Counted.count


def worst_case(n: int) -> int:
    return sum(math.ceil(math.log2(3 * k / 4)) for k in range(1, n + 1))


def test_example() -> None:
    assert comparisons([5, 1, 4, 2, 8, 0, 3]) == 12
    a = [5, 1, 4, 2, 8, 0, 3]
    ford_johnson_algorithm(a)
    assert a == [0, 1, 2, 3, 4, 5, 8]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)], [0, 2**63 - 1, -(2**63), 0]):
        b = list(a)
        ford_johnson_algorithm(b)
        assert b == sorted(a)


def test_worst_case_is_exact_for_small_n() -> None:
    for n in range(0, 9):
        worst = max(comparisons(list(p)) for p in itertools.permutations(range(n)))
        assert worst == worst_case(n)
        assert worst == math.ceil(math.log2(math.factorial(n)))


def test_never_above_the_bound() -> None:
    rng = random.Random(1959)
    for n in (12, 13, 16, 22, 50, 200):
        for _ in range(20):
            p = list(range(n))
            rng.shuffle(p)
            assert comparisons(p) <= worst_case(n)


def test_not_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    a = [Key(0, "a"), Key(1, "b"), Key(0, "c"), Key(0, "d")]
    ford_johnson_algorithm(a)
    assert [x.k for x in a] == [0, 0, 0, 1]
    assert [x.tag for x in a] == ["c", "d", "a", "b"]


def test_random_against_sorted() -> None:
    rng = random.Random(1965)
    for _ in range(600):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 60))]
        b = list(a)
        ford_johnson_algorithm(b)
        assert b == sorted(a)


def test_strings() -> None:
    a = ["pear", "fig", "apple", "fig", "kiwi"]
    ford_johnson_algorithm(a)
    assert a == ["apple", "fig", "fig", "kiwi", "pear"]
