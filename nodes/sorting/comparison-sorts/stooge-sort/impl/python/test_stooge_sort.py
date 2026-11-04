# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stooge-sort/. The authors are listed in prov/Y4SMX5.jsonl.

import itertools
import random

from stooge_sort import stooge_range, stooge_sort


def test_example() -> None:
    a = [5, 1, 4, 2, 3]
    assert stooge_range(a, 0, 4) == 40
    assert a == [1, 2, 3, 4, 5]


def test_call_counts() -> None:
    expected = {1: 1, 2: 1, 3: 4, 4: 13, 5: 40, 6: 40, 7: 121, 9: 121, 10: 364, 100: 265720}
    for n, c in expected.items():
        assert stooge_range(list(range(n, 0, -1)), 0, n - 1) == c


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [0, 2, 1, 3]):
        b = list(a)
        stooge_sort(b)
        assert b == sorted(a)


def test_all_permutations() -> None:
    for n in range(1, 8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            stooge_sort(b)
            assert b == list(range(n))


def test_not_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    b = [Key(1, "a"), Key(1, "b"), Key(0, "c")]
    stooge_sort(b)
    assert [x.tag for x in b] == ["c", "b", "a"]


def test_random_against_sorted() -> None:
    rng = random.Random(7)
    for _ in range(100):
        a = [rng.randint(-5, 5) for _ in range(rng.randint(0, 40))]
        b = list(a)
        stooge_sort(b)
        assert b == sorted(a)
