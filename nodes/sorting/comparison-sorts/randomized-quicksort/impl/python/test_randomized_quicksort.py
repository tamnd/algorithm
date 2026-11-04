# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-quicksort/. The authors are listed in prov/PP7XPG.jsonl.

import itertools
import random

from randomized_quicksort import randomized_quicksort


class Counted:
    count = 0

    def __init__(self, v: int) -> None:
        self.v = v

    def __lt__(self, other: "Counted") -> bool:
        Counted.count += 1
        return self.v < other.v


def test_example() -> None:
    a = [1, 2, 3, 4, 5, 6, 7, 8]
    randomized_quicksort(a, random.Random(1))
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, -1, 3, 0]):
        b = list(a)
        randomized_quicksort(b, random.Random(0))
        assert b == sorted(a)


def test_all_permutations() -> None:
    rng = random.Random(3)
    for n in range(7):
        for p in itertools.permutations(range(n)):
            a = list(p)
            randomized_quicksort(a, rng)
            assert a == list(range(n))


def test_random_with_duplicates() -> None:
    rng = random.Random(11)
    for _ in range(200):
        a = [rng.randint(0, 20) for _ in range(rng.randint(0, 60))]
        b = list(a)
        randomized_quicksort(b, rng)
        assert b == sorted(a)


def test_default_rng() -> None:
    a = list(range(500, 0, -1))
    randomized_quicksort(a)
    assert a == list(range(1, 501))


def test_mean_on_sorted_input() -> None:
    # The expected count on distinct keys is 2(n + 1)H_n - 4n on every input.
    n = 200
    h = sum(1 / k for k in range(1, n + 1))
    expected = 2 * (n + 1) * h - 4 * n
    rng = random.Random(5)
    total = 0
    runs = 200
    for _ in range(runs):
        a = [Counted(i) for i in range(n)]
        Counted.count = 0
        randomized_quicksort(a, rng)
        total += Counted.count
    assert abs(total / runs - expected) < 0.05 * expected
