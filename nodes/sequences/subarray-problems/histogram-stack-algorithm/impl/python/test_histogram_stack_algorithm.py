# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-stack-algorithm/. The authors are listed in prov/PXWH0K.jsonl.

import random

from histogram_stack_algorithm import largest_rectangle, largest_rectangle_span


def brute(h: list[int]) -> int:
    return max(
        ((j - i + 1) * min(h[i : j + 1]) for i in range(len(h)) for j in range(i, len(h))),
        default=0,
    )


def test_example() -> None:
    assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle_span([2, 1, 5, 6, 2, 3]) == (10, 2, 3)


def test_edges() -> None:
    assert largest_rectangle([]) == 0
    assert largest_rectangle_span([]) == (0, 0, -1)
    assert largest_rectangle([0]) == 0
    assert largest_rectangle([7]) == 7
    assert largest_rectangle([1, 2, 3]) == 4
    assert largest_rectangle([1, 2, 3, 4, 5]) == 9
    assert largest_rectangle([3, 3, 3]) == 9
    assert largest_rectangle([2, 4]) == 4
    assert largest_rectangle([0, 0, 1, 0]) == 1
    assert largest_rectangle([1.5, 1.5]) == 3.0


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(3000):
        n = rng.randrange(0, 20)
        h = [rng.randrange(0, 7) for _ in range(n)]
        expected = brute(h)
        assert largest_rectangle(h) == expected
        area, a, b = largest_rectangle_span(h)
        assert area == expected
        if area:
            assert (b - a + 1) * min(h[a : b + 1]) == area
