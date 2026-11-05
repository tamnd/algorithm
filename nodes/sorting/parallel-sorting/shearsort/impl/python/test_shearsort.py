# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shearsort/. The authors are listed in prov/YNCX5H.jsonl.

import itertools
import random

from shearsort import shearsort, snake


def grid(values: list[int], c: int) -> list[list[int]]:
    return [values[i : i + c] for i in range(0, len(values), c)]


def test_example() -> None:
    m = [[13, 2, 7, 10], [5, 16, 1, 12], [9, 4, 15, 8], [3, 14, 6, 11]]
    steps = shearsort(m)
    assert m == [[1, 2, 3, 4], [8, 7, 6, 5], [9, 10, 11, 12], [16, 15, 14, 13]]
    assert steps == 2 * (4 + 4) + 4


def test_two_by_two() -> None:
    m = [[4, 1], [3, 2]]
    shearsort(m)
    assert m == [[1, 2], [4, 3]]


def test_all_zero_one_inputs() -> None:
    for r, c in ((1, 5), (2, 3), (3, 3), (3, 4), (4, 3), (2, 5), (5, 2)):
        for bits in itertools.product((0, 1), repeat=r * c):
            m = grid(list(bits), c)
            shearsort(m)
            assert snake(m) == sorted(bits)


def test_step_count_square() -> None:
    for side in (2, 4, 8, 16):
        m = [[0] * side for _ in range(side)]
        n = side * side
        assert shearsort(m) == side * (n.bit_length() - 1 + 1)


def test_random_against_sorted() -> None:
    rng = random.Random(6)
    for _ in range(200):
        r, c = rng.randint(1, 7), rng.randint(1, 7)
        vals = [rng.randint(0, 30) for _ in range(r * c)]
        m = grid(vals, c)
        shearsort(m)
        assert snake(m) == sorted(vals)
