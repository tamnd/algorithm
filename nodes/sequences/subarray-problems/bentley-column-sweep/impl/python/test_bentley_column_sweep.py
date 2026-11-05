# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bentley-column-sweep/. The authors are listed in prov/B4PWT1.jsonl.

import random

import pytest

from bentley_column_sweep import max_sum_submatrix, max_sum_submatrix_auto


def rect_sum(m: list[list[int]], a: int, b: int, e: int, d: int) -> int:
    return sum(m[i][j] for i in range(a, b + 1) for j in range(e, d + 1))


def brute(m: list[list[int]]) -> int:
    r, c = len(m), len(m[0])
    return max(
        rect_sum(m, a, b, e, d)
        for a in range(r)
        for b in range(a, r)
        for e in range(c)
        for d in range(e, c)
    )


EXAMPLE = [
    [1, 2, -1, -4, -20],
    [-8, -3, 4, 2, 1],
    [3, 8, 10, 1, 3],
    [-4, -1, 1, 7, -6],
]


def test_example() -> None:
    assert max_sum_submatrix(EXAMPLE) == (29, (1, 3, 1, 3))
    assert max_sum_submatrix_auto(EXAMPLE) == 29


def test_edges() -> None:
    assert max_sum_submatrix([[5]]) == (5, (0, 0, 0, 0))
    assert max_sum_submatrix([[-5]]) == (-5, (0, 0, 0, 0))
    assert max_sum_submatrix([[-3, -1], [-2, -4]])[0] == -1
    assert max_sum_submatrix([[1, 2, 3]])[0] == 6
    assert max_sum_submatrix([[1], [-2], [3]])[0] == 3
    assert max_sum_submatrix_auto([[1], [-2], [3]]) == 3
    with pytest.raises(ValueError):
        max_sum_submatrix([])
    with pytest.raises(ValueError):
        max_sum_submatrix([[1, 2], [3]])


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(2000):
        r = rng.randrange(1, 6)
        c = rng.randrange(1, 6)
        m = [[rng.randrange(-9, 10) for _ in range(c)] for _ in range(r)]
        expected = brute(m)
        best, (a, b, e, d) = max_sum_submatrix(m)
        assert best == expected
        assert 0 <= a <= b < r and 0 <= e <= d < c
        assert rect_sum(m, a, b, e, d) == best
        assert max_sum_submatrix_auto(m) == expected
