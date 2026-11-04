# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-pivot-quicksort/. The authors are listed in prov/8SHK9M.jsonl.

import itertools
import random

from dual_pivot_quicksort import dual_pivot_quicksort, partition


class Counted:
    count = 0

    def __init__(self, k: int) -> None:
        self.k = k

    def __lt__(self, other: "Counted") -> bool:
        Counted.count += 1
        return self.k < other.k


def test_example_partition() -> None:
    a = [Counted(x) for x in [3, 7, 1, 8, 5, 2, 9, 4, 6]]
    Counted.count = 0
    assert partition(a, 0, 8) == (2, 5)
    assert [x.k for x in a] == [2, 1, 3, 4, 5, 6, 9, 7, 8]
    assert Counted.count == 13


def test_example_sort() -> None:
    a = [3, 7, 1, 8, 5, 2, 9, 4, 6]
    dual_pivot_quicksort(a)
    assert a == list(range(1, 10))


def test_partition_postcondition() -> None:
    for n in range(2, 8):
        for p in itertools.product(range(4), repeat=n):
            a = list(p)
            l, g = partition(a, 0, n - 1)
            x, y = a[l], a[g]
            assert 0 <= l < g <= n - 1
            assert sorted(a) == sorted(p)
            assert all(v < x for v in a[:l])
            assert all(x <= v <= y for v in a[l + 1 : g])
            assert all(v >= y for v in a[g + 1 :])


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)], [0, 2**63 - 1, -(2**63), 0]):
        b = list(a)
        dual_pivot_quicksort(b)
        assert b == sorted(a)


def test_all_small_permutations() -> None:
    for n in range(0, 8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            dual_pivot_quicksort(b)
            assert b == list(range(n))


def test_sorted_equal_and_reversed_large() -> None:
    for a in (list(range(3000)), [5] * 3000, list(range(3000, 0, -1))):
        b = list(a)
        dual_pivot_quicksort(b)
        assert b == sorted(a)


def test_not_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    a = [Key(0, "a"), Key(1, "b"), Key(1, "c"), Key(0, "d")]
    partition(a, 0, 3)
    assert [x.k for x in a] == [0, 0, 1, 1]
    assert [x.tag for x in a] == ["a", "d", "c", "b"]


def test_random_against_sorted() -> None:
    rng = random.Random(2012)
    for _ in range(600):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 60))]
        b = list(a)
        dual_pivot_quicksort(b, seed=rng.randrange(1000))
        assert b == sorted(a)


def test_strings() -> None:
    a = ["pear", "fig", "apple", "fig", "kiwi"]
    dual_pivot_quicksort(a)
    assert a == ["apple", "fig", "fig", "kiwi", "pear"]
