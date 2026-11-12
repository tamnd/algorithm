# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-separability/. The authors are listed in prov/7A99T5.jsonl.

import random
from itertools import product

from linear_separability import (
    count_separable_dichotomies,
    cover_count,
    in_general_position,
    is_separable,
    separator,
)

SQUARE = [(0, 0), (0, 1), (1, 0), (1, 1)]


def check(xs, ys, sep, bias=True) -> bool:
    w, b = sep
    return all(y * (sum(a * v for a, v in zip(w, x)) + b) >= 1 for x, y in zip(xs, ys))


def test_xor_is_not_separable() -> None:
    assert separator(SQUARE, [-1, 1, 1, -1]) is None
    assert separator(SQUARE, [1, -1, -1, 1]) is None


def test_and_or_are_separable_with_a_certificate() -> None:
    for ys in ([-1, -1, -1, 1], [-1, 1, 1, 1]):
        sep = separator(SQUARE, ys)
        assert sep is not None and check(SQUARE, ys, sep)


def test_fourteen_of_sixteen_boolean_functions_of_two_inputs() -> None:
    assert count_separable_dichotomies(SQUARE, bias=True) == 14


def test_every_yes_answer_is_checked_and_every_no_has_no_grid_separator() -> None:
    rng = random.Random(4)
    grid = [(a, b, c) for a in range(-3, 4) for b in range(-3, 4) for c in range(-3, 4)]
    for _ in range(150):
        xs = [(rng.randint(-3, 3), rng.randint(-3, 3)) for _ in range(rng.randint(1, 6))]
        ys = [rng.choice((-1, 1)) for _ in xs]
        sep = separator(xs, ys)
        if sep is not None:
            assert check(xs, ys, sep)
        else:
            # no small integer (w, b) separates either
            assert not any(
                all(y * (g[0] * x[0] + g[1] * x[1] + g[2]) > 0 for x, y in zip(xs, ys)) for g in grid
            )


def test_cover_formula_values() -> None:
    assert [cover_count(n, 1) for n in range(1, 6)] == [2, 2, 2, 2, 2]
    assert [cover_count(n, 2) for n in range(1, 7)] == [2, 4, 6, 8, 10, 12]
    assert [cover_count(n, 3) for n in range(1, 7)] == [2, 4, 8, 14, 22, 32]
    for d in range(1, 6):
        assert cover_count(2 * d, d) * 2 == 2 ** (2 * d)
        for n in range(1, d + 1):
            assert cover_count(n, d) == 2**n


def test_cover_counting_theorem_by_enumeration() -> None:
    rng = random.Random(1965)
    for d in (1, 2, 3):
        for n in range(1, 7):
            while True:
                xs = [tuple(rng.randint(-9, 9) for _ in range(d)) for _ in range(n)]
                if in_general_position(xs):
                    break
            assert count_separable_dichotomies(xs, bias=False) == cover_count(n, d)


def test_affine_version_counts_with_d_plus_one() -> None:
    rng = random.Random(7)
    for d in (1, 2):
        for n in range(1, 7):
            while True:
                xs = [tuple(rng.randint(-9, 9) for _ in range(d)) for _ in range(n)]
                lifted = [x + (1,) for x in xs]
                if in_general_position(lifted):
                    break
            assert count_separable_dichotomies(xs, bias=True) == cover_count(n, d + 1)


def test_not_general_position_gives_fewer() -> None:
    xs = [(1, 0), (2, 0), (-1, 0)]  # all on one line through the origin
    assert not in_general_position(xs)
    assert count_separable_dichotomies(xs, bias=False) == 2 < cover_count(3, 2)


def test_empty_and_single_point() -> None:
    assert separator([], []) == ([], 0)
    assert is_separable([(0, 0)], [1])
    assert not is_separable([(0, 0)], [1], bias=False)
    assert all(is_separable([(2, 5)], [y], bias=False) for y in (-1, 1))
    assert list(product((-1, 1), repeat=0)) == [()]
