# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/columnsort/. The authors are listed in prov/HTGXH0.jsonl.

import itertools
import random

import pytest

from columnsort import column_major, columnsort, sort_columns, transpose_step, untranspose_step


EXAMPLE = [
    [3, 11, 5, 13, 10, 14, 27, 25, 19],
    [26, 7, 4, 18, 16, 22, 6, 2, 8],
    [15, 1, 17, 21, 23, 12, 24, 9, 20],
]


def test_example() -> None:
    out = columnsort(EXAMPLE)
    assert out == [list(range(1, 10)), list(range(10, 19)), list(range(19, 28))]


def test_example_after_step_five() -> None:
    cols = sort_columns(untranspose_step(sort_columns(transpose_step(sort_columns(EXAMPLE)))))
    assert cols[0] == [1, 2, 3, 4, 5, 6, 8, 10, 12]


def test_steps_two_and_four_are_inverse() -> None:
    cols = [[1, 2, 3, 4], [5, 6, 7, 8]]
    assert transpose_step(cols) == [[1, 3, 5, 7], [2, 4, 6, 8]]
    assert untranspose_step(transpose_step(cols)) == cols


def zero_one_inputs(r: int, s: int):
    """After step 1 a 0-1 matrix depends only on the zeros in each column."""
    for zeros in itertools.product(range(r + 1), repeat=s):
        yield [[0] * z + [1] * (r - z) for z in zeros]


def test_all_zero_one_inputs_small() -> None:
    for r, s in ((2, 2), (4, 2), (9, 3), (12, 3)):
        for cols in zero_one_inputs(r, s):
            out = column_major(columnsort(cols))
            assert out == sorted(out)


def test_condition_is_needed() -> None:
    cols = [[0] * z + [1] * (16 - z) for z in (1, 1, 1, 5)]
    out = column_major(columnsort(cols, check=False))
    assert out != sorted(out)
    with pytest.raises(ValueError):
        columnsort(cols)


def test_random_large() -> None:
    rng = random.Random(3)
    for r, s in ((20, 4), (32, 4), (36, 4), (50, 5)):
        for _ in range(100):
            vals = [rng.randint(0, 40) for _ in range(r * s)]
            cols = [vals[k * r : (k + 1) * r] for k in range(s)]
            assert column_major(columnsort(cols)) == sorted(vals)
