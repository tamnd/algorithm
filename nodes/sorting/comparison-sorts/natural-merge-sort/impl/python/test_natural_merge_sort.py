# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/natural-merge-sort/. The authors are listed in prov/8CJ9C7.jsonl.

import itertools
import random

from natural_merge_sort import natural_merge_sort, run_bounds


class Counted:
    count = 0

    def __init__(self, key: int, tag: int = 0) -> None:
        self.key = key
        self.tag = tag

    def __lt__(self, other: "Counted") -> bool:
        Counted.count += 1
        return self.key < other.key


def test_example() -> None:
    a = [3, 8, 9, 2, 5, 1, 4, 6, 7, 0]
    assert run_bounds(a) == [0, 3, 5, 9, 10]
    natural_merge_sort(a)
    assert a == list(range(10))


def test_example_count() -> None:
    a = [Counted(x) for x in [3, 8, 9, 2, 5, 1, 4, 6, 7, 0]]
    Counted.count = 0
    natural_merge_sort(a)
    assert Counted.count == 9 + 3 + 1 + 8


def test_sorted_is_linear() -> None:
    n = 1000
    a = [Counted(i) for i in range(n)]
    Counted.count = 0
    natural_merge_sort(a)
    assert Counted.count == n - 1


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1], [3, 2, 1], [1, 3, 2]):
        b = list(a)
        natural_merge_sort(b)
        assert b == sorted(a)
    assert run_bounds([]) == [0]


def test_all_permutations() -> None:
    for n in range(8):
        for p in itertools.permutations(range(n)):
            a = list(p)
            natural_merge_sort(a)
            assert a == list(range(n))


def test_stable() -> None:
    rng = random.Random(2)
    for _ in range(200):
        keys = [rng.randint(0, 4) for _ in range(rng.randint(0, 40))]
        a = [Counted(k, t) for t, k in enumerate(keys)]
        natural_merge_sort(a)
        assert [(x.key, x.tag) for x in a] == sorted((x.key, x.tag) for x in a)


def test_random() -> None:
    rng = random.Random(8)
    for _ in range(100):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 300))]
        b = list(a)
        natural_merge_sort(b)
        assert b == sorted(a)
