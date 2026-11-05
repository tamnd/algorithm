# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cole-merge-sort/. The authors are listed in prov/342B4P.jsonl.

import itertools
import random

from cole_merge_sort import cole_merge_sort


def test_example() -> None:
    stats: dict = {}
    a = [42, 7, 93, 25, 60, 12, 88, 3]
    assert cole_merge_sort(a, stats) == [3, 7, 12, 25, 42, 60, 88, 93]
    assert stats["stages"] == 9


def test_edges() -> None:
    assert cole_merge_sort([]) == []
    assert cole_merge_sort([5]) == [5]
    assert cole_merge_sort([2, 1]) == [1, 2]
    assert cole_merge_sort([3, 1, 2]) == [1, 2, 3]


def test_all_permutations() -> None:
    for n in range(1, 8):
        for perm in itertools.permutations(range(n)):
            assert cole_merge_sort(list(perm)) == list(range(n))


def test_random_and_cover() -> None:
    rng = random.Random(3)
    for n in [5, 16, 31, 64, 100, 256, 512]:
        a = [rng.randrange(n) for _ in range(n)]
        stats: dict = {}
        assert cole_merge_sort(a, stats) == sorted(a)
        assert stats["max_candidates"] <= 3
        k = (n - 1).bit_length()
        assert stats["stages"] == 3 * k
        assert stats["max_live"] <= 4 * (1 << k)


def test_stable() -> None:
    rng = random.Random(5)
    pairs = [(rng.randrange(4), i) for i in range(50)]

    class K:
        def __init__(self, p: tuple[int, int]) -> None:
            self.p = p

        def __lt__(self, other: "K") -> bool:
            return self.p[0] < other.p[0]

    out = cole_merge_sort([K(p) for p in pairs])
    assert [k.p for k in out] == sorted(pairs, key=lambda p: p[0])
