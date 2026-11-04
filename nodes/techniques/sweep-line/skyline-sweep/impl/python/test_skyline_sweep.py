# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skyline-sweep/. The authors are listed in prov/B8EJVN.jsonl.

import random

from skyline_sweep import get_skyline


def brute_force(buildings: list[list[int]]) -> list[list[int]]:
    """Evaluate f at every integer x and keep the points where it changes."""
    if not buildings:
        return []
    xs = range(min(b[0] for b in buildings), max(b[1] for b in buildings) + 1)
    out: list[list[int]] = []
    prev = 0
    for x in xs:
        h = max([b[2] for b in buildings if b[0] <= x < b[1]], default=0)
        if h != prev:
            out.append([x, h])
            prev = h
    return out


def test_example() -> None:
    b = [[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]
    assert get_skyline(b) == [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]


def test_edges() -> None:
    assert get_skyline([]) == []
    assert get_skyline([[1, 5, 3]]) == [[1, 3], [5, 0]]
    assert get_skyline([[0, 2, 3], [0, 2, 3], [0, 2, 3]]) == [[0, 3], [2, 0]]
    assert get_skyline([[0, 10, 2], [3, 4, 1]]) == [[0, 2], [10, 0]]
    big = 2**62
    assert get_skyline([[-big, big, big]]) == [[-big, big], [big, 0]]


def test_pitfalls() -> None:
    # A start and an end at the same x: no spurious drop to 0.
    assert get_skyline([[0, 2, 5], [2, 4, 3]]) == [[0, 5], [2, 3], [4, 0]]
    # Adjacent buildings of the same height merge into one piece.
    assert get_skyline([[0, 2, 5], [2, 4, 5]]) == [[0, 5], [4, 0]]
    # A gap between buildings gives a point at height 0.
    assert get_skyline([[0, 2, 5], [3, 4, 5]]) == [[0, 5], [2, 0], [3, 5], [4, 0]]
    # Equal left ends with different heights.
    assert get_skyline([[0, 2, 3], [0, 1, 4]]) == [[0, 4], [1, 3], [2, 0]]
    # Equal right ends with different heights.
    assert get_skyline([[0, 3, 3], [1, 3, 4]]) == [[0, 3], [1, 4], [3, 0]]


def test_input_not_changed() -> None:
    b = [[5, 6, 1], [1, 2, 1]]
    get_skyline(b)
    assert b == [[5, 6, 1], [1, 2, 1]]


def test_random_against_brute_force() -> None:
    rng = random.Random(4217)
    for _ in range(1000):
        n = rng.randint(0, 12)
        b = []
        for _ in range(n):
            left = rng.randint(-5, 15)
            b.append([left, left + rng.randint(1, 8), rng.randint(1, 6)])
        got = get_skyline(b)
        assert got == brute_force(b)
        assert len(got) <= 2 * n
        assert all(got[k][1] != got[k + 1][1] for k in range(len(got) - 1))
