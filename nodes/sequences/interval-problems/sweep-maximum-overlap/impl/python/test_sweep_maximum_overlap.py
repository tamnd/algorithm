# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-maximum-overlap/. The authors are listed in prov/KC8DHG.jsonl.

import random

from sweep_maximum_overlap import sweep_maximum_overlap

EXAMPLE = [(1, 3), (2, 5), (3, 4), (5, 8), (6, 7), (8, 9), (7, 10)]


def cover(intervals: list[tuple[int, int]], x: float, closed: bool) -> int:
    if closed:
        return sum(a <= x <= b for a, b in intervals)
    return sum(a <= x < b for a, b in intervals)


def oracle(intervals: list[tuple[int, int]], closed: bool) -> int:
    """Brute force over all half-integer points."""
    if not intervals:
        return 0
    lo = min(a for a, _ in intervals)
    hi = max(b for _, b in intervals)
    return max(cover(intervals, x / 2, closed) for x in range(2 * lo, 2 * hi + 1))


def test_example() -> None:
    assert sweep_maximum_overlap(EXAMPLE) == (3, 3)
    assert sweep_maximum_overlap(EXAMPLE, closed=False) == (2, 2)


def test_touching() -> None:
    assert sweep_maximum_overlap([(1, 3), (3, 5)]) == (2, 3)
    assert sweep_maximum_overlap([(1, 3), (3, 5)], closed=False) == (1, 1)
    assert sweep_maximum_overlap([(4, 4), (4, 4), (4, 4)]) == (3, 4)


def test_edges() -> None:
    assert sweep_maximum_overlap([]) == (0, None)
    assert sweep_maximum_overlap([(2, 9)]) == (1, 2)
    assert sweep_maximum_overlap([(0, 1), (2, 3), (4, 5)]) == (1, 0)
    assert sweep_maximum_overlap([(0, 10)] * 6, closed=False) == (6, 0)
    big = 2**62
    assert sweep_maximum_overlap([(-big, big), (big, big)]) == (2, big)


def test_against_oracle() -> None:
    rng = random.Random(253)
    for _ in range(800):
        closed = rng.random() < 0.5
        iv = []
        for _ in range(rng.randrange(0, 9)):
            a = rng.randrange(0, 12)
            iv.append((a, a + rng.randrange(0 if closed else 1, 6)))
        d, x = sweep_maximum_overlap(iv, closed)
        assert d == oracle(iv, closed)
        if iv:
            assert cover(iv, x, closed) == d
