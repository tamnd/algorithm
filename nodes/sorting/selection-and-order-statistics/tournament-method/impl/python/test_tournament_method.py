# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tournament-method/. The authors are listed in prov/RB2RMG.jsonl.

import random

import pytest

from tournament_method import tournament_second


class Counted:
    """An int wrapper that counts calls of <."""

    count = 0

    def __init__(self, v: int) -> None:
        self.v = v

    def __lt__(self, other: "Counted") -> bool:
        Counted.count += 1
        return self.v < other.v


def comparisons(a: list[int]) -> tuple[int, int, int]:
    Counted.count = 0
    big, second = tournament_second([Counted(x) for x in a])
    return big.v, second.v, Counted.count


def ceil_lg(n: int) -> int:
    return (n - 1).bit_length()


def test_examples() -> None:
    assert tournament_second([7, 2, 9, 4, 1, 8, 3, 6]) == (9, 8)
    assert tournament_second([9, 8, 1, 2, 3, 4, 5, 6]) == (9, 8)
    assert comparisons([7, 2, 9, 4, 1, 8, 3, 6])[2] == 9


def test_edges() -> None:
    assert tournament_second([1, 2]) == (2, 1)
    assert tournament_second([5, 5]) == (5, 5)
    assert tournament_second([3, 7, 7]) == (7, 7)
    with pytest.raises(ValueError):
        tournament_second([1])


def test_comparison_bound() -> None:
    rng = random.Random(9)
    for n in range(2, 140):
        for _ in range(5):
            a = rng.sample(range(1000), n)
            c = comparisons(a)[2]
            assert c <= n + ceil_lg(n) - 2
            if n & (n - 1) == 0:
                assert c == n + ceil_lg(n) - 2


def test_random_against_sorted() -> None:
    rng = random.Random(1932)
    for _ in range(1000):
        n = rng.randint(2, 70)
        a = [rng.randint(-10, 10) for _ in range(n)]
        b = sorted(a)
        assert tournament_second(a) == (b[-1], b[-2])
