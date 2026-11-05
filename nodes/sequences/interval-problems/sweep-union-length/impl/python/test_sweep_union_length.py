# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-union-length/. The authors are listed in prov/BJ70R6.jsonl.

import math
import random

from sweep_union_length import sweep_union_length


def oracle(intervals: list[tuple[int, int]], k: int) -> int:
    """Count the unit cells [x, x + 1) covered by at least k intervals."""
    if not intervals:
        return 0
    lo = min(a for a, _ in intervals)
    hi = max(b for _, b in intervals)
    return sum(1 for x in range(lo, hi) if sum(a <= x and x + 1 <= b for a, b in intervals) >= k)


def test_example() -> None:
    iv = [(1, 4), (7, 9), (2, 5), (9, 12), (8, 9), (14, 14)]
    assert sweep_union_length(iv) == 9
    assert sweep_union_length(iv, k=2) == 3
    assert sweep_union_length(iv, k=3) == 0


def test_touching_and_points() -> None:
    assert sweep_union_length([(1, 3), (3, 5)]) == 4
    assert sweep_union_length([(5, 5), (5, 5)]) == 0
    assert sweep_union_length([(1, 3), (3, 3), (3, 5)], k=2) == 0


def test_integer_points() -> None:
    # closed integer intervals [l, r] cover the integers of [l, r + 1)
    iv = [(1, 3), (3, 5)]
    assert sweep_union_length([(a, b + 1) for a, b in iv]) == 5
    assert sweep_union_length([(a, b + 1) for a, b in [(1, 3), (4, 5)]]) == 5


def test_edges() -> None:
    assert sweep_union_length([]) == 0
    assert sweep_union_length([(2, 7)]) == 5
    assert sweep_union_length([(2, 7)] * 4) == 5
    assert sweep_union_length([(2, 7)] * 4, k=4) == 5
    assert sweep_union_length([(1, 10), (2, 3), (4, 5)]) == 9
    big = 2**62
    assert sweep_union_length([(-big, big), (0, 1)]) == 2 * big
    assert math.isclose(sweep_union_length([(0.1, 0.2), (0.15, 0.3)]), 0.2)


def test_against_oracle() -> None:
    rng = random.Random(1977)
    for _ in range(700):
        n = rng.randrange(0, 9)
        iv = []
        for _ in range(n):
            a = rng.randrange(-5, 15)
            iv.append((a, a + rng.randrange(0, 7)))
        k = rng.randrange(1, 4)
        assert sweep_union_length(iv, k) == oracle(iv, k)
