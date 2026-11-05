# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-merging-sort/. The authors are listed in prov/ZVJBCZ.jsonl.

import random

from interval_merging_sort import interval_merging_sort


def oracle(intervals: list[tuple[int, int]], merge_touching: bool) -> list[tuple[int, int]]:
    """Components of the union on the half-integer grid: x/2 is covered or not."""
    if not intervals:
        return []
    lo = 2 * min(a for a, _ in intervals) - 1
    hi = 2 * max(b for _, b in intervals) + 1

    def covered(x: int) -> bool:
        for a, b in intervals:
            if merge_touching and 2 * a <= x <= 2 * b:
                return True
            if not merge_touching and 2 * a < x < 2 * b:
                return True
        return False

    comps: list[tuple[int, int]] = []
    start = None
    for x in range(lo, hi + 2):
        c = covered(x)
        if c and start is None:
            start = x
        if not c and start is not None:
            a, b = start, x - 1
            if not merge_touching:
                a, b = a - 1, b + 1  # open ends lie one half step outside
            comps.append((a // 2, b // 2))
            start = None
    return comps


def test_example() -> None:
    iv = [(8, 10), (1, 3), (15, 18), (2, 6), (10, 12), (17, 17), (5, 7)]
    assert interval_merging_sort(iv) == [(1, 7), (8, 12), (15, 18)]
    assert iv[0] == (8, 10)


def test_touching() -> None:
    assert interval_merging_sort([(1, 3), (3, 5)]) == [(1, 5)]
    assert interval_merging_sort([(1, 3), (3, 5)], merge_touching=False) == [(1, 3), (3, 5)]
    assert interval_merging_sort([(1, 3), (4, 5)]) == [(1, 3), (4, 5)]
    assert interval_merging_sort([(3, 5), (1, 3), (3, 3)]) == [(1, 5)]


def test_edges() -> None:
    assert interval_merging_sort([]) == []
    assert interval_merging_sort([(2, 4)]) == [(2, 4)]
    assert interval_merging_sort([(2, 4)] * 5) == [(2, 4)]
    assert interval_merging_sort([(1, 10), (2, 3), (4, 5)]) == [(1, 10)]
    big = 2**62
    assert interval_merging_sort([(-big, 0), (0, big)]) == [(-big, big)]
    assert interval_merging_sort([(0.5, 1.5), (1.5, 2.0)]) == [(0.5, 2.0)]


def test_against_oracle() -> None:
    rng = random.Random(56)
    for _ in range(600):
        n = rng.randrange(0, 8)
        touching = rng.random() < 0.5
        iv = []
        for _ in range(n):
            a = rng.randrange(0, 12)
            b = a + rng.randrange(0 if touching else 1, 5)
            iv.append((a, b))
        assert interval_merging_sort(iv, touching) == oracle(iv, touching)
