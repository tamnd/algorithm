# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimax-theorem/. The authors are listed in prov/C14532.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from minimax_theorem import (
    column_payoffs,
    pure_maximin,
    pure_minimax,
    row_payoffs,
    solve_matrix_game,
)


def check_certificate(m, v, x, y):
    assert all(p >= 0 for p in x) and sum(x) == 1
    assert all(q >= 0 for q in y) and sum(y) == 1
    # x guarantees at least v against every column, y at most v against every row.
    assert min(column_payoffs(m, x)) == v
    assert max(row_payoffs(m, y)) == v


def exact_two_row_value(m):
    """Independent oracle for 2 by c games: max over p of min_j f_j(p) is at a breakpoint."""
    cols = len(m[0])
    cands = {Fraction(0), Fraction(1)}
    for j, k in itertools.combinations(range(cols), 2):
        # f_j(p) = p m0j + (1 - p) m1j; solve f_j = f_k.
        den = (m[0][j] - m[1][j]) - (m[0][k] - m[1][k])
        if den != 0:
            p = Fraction(m[1][k] - m[1][j], den)
            if 0 <= p <= 1:
                cands.add(p)
    return max(min(p * m[0][j] + (1 - p) * m[1][j] for j in range(cols)) for p in cands)


def grid_points(r, n):
    """All mixed strategies over r pure strategies with coordinates in multiples of 1/n, times n."""
    for c in itertools.product(range(n + 1), repeat=r - 1):
        if sum(c) <= n:
            yield list(c) + [n - sum(c)]


def grid_maxmin(m, n):
    """Brute force max over the grid of min over columns, for an integer matrix."""
    cols = range(len(m[0]))
    best = max(min(sum(k * row[j] for k, row in zip(x, m)) for j in cols) for x in grid_points(len(m), n))
    return Fraction(best, n)


def grid_minmax(m, n):
    """Brute force min over the grid of max over rows, for an integer matrix."""
    best = min(max(sum(k * a for k, a in zip(y, row)) for row in m) for y in grid_points(len(m[0]), n))
    return Fraction(best, n)


def test_matching_pennies():
    m = [[1, -1], [-1, 1]]
    v, x, y = solve_matrix_game(m)
    assert v == 0
    assert x == [Fraction(1, 2)] * 2 and y == [Fraction(1, 2)] * 2
    # In pure strategies the two security levels differ.
    assert pure_maximin(m) == -1 and pure_minimax(m) == 1


def test_rock_paper_scissors():
    m = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
    v, x, y = solve_matrix_game(m)
    assert v == 0
    assert x == [Fraction(1, 3)] * 3 and y == [Fraction(1, 3)] * 3


def test_page_example():
    m = [[3, -1], [-2, 1]]
    v, x, y = solve_matrix_game(m)
    assert v == Fraction(1, 7)
    assert x == [Fraction(3, 7), Fraction(4, 7)]
    assert y == [Fraction(2, 7), Fraction(5, 7)]
    check_certificate(m, v, x, y)
    assert grid_maxmin(m, 7) == v and grid_minmax(m, 7) == v
    assert grid_maxmin(m, 10) < v < grid_minmax(m, 10)


def test_saddle_point():
    m = [[4, 2, 5], [1, 0, 3], [3, 1, 2]]
    v, x, y = solve_matrix_game(m)
    assert v == 2 == pure_maximin(m) == pure_minimax(m)
    check_certificate(m, v, x, y)


def test_dominated_and_single():
    assert solve_matrix_game([[5]])[0] == 5
    v, x, y = solve_matrix_game([[0, 0], [0, 0]])
    assert v == 0
    v, x, y = solve_matrix_game([[2, 7, -3]])
    assert v == -3 and y == [0, 0, 1]
    v, x, y = solve_matrix_game([[2], [7], [-3]])
    assert v == 7 and x == [0, 1, 0]


def test_bad_input():
    with pytest.raises(ValueError):
        solve_matrix_game([[1, 2], [3]])


def test_random_two_row_against_breakpoints_and_grid():
    rng = random.Random(1928)
    n = 40
    for _ in range(300):
        c = rng.randint(1, 4)
        m = [[rng.randint(-5, 5) for _ in range(c)] for _ in range(2)]
        v, x, y = solve_matrix_game(m)
        check_certificate(m, v, x, y)
        assert v == exact_two_row_value(m)
        lo, hi = grid_maxmin(m, n), grid_minmax(m, 8)
        assert lo <= v <= hi
        # A grid point is within 1/(2n) of x[0], which moves each payoff by at most 10/(2n).
        assert v - lo <= Fraction(10, 2 * n)


def test_random_square_against_grid():
    rng = random.Random(1938)
    n = 24
    for _ in range(40):
        m = [[rng.randint(-4, 4) for _ in range(3)] for _ in range(3)]
        v, x, y = solve_matrix_game(m)
        check_certificate(m, v, x, y)
        lo, hi = grid_maxmin(m, n), grid_minmax(m, n)
        assert lo <= v <= hi
        assert pure_maximin(m) <= v <= pure_minimax(m)
        # The nearest grid point is within L1 distance 2/n, and entries have size at most 4.
        assert v - lo <= Fraction(8, n) and hi - v <= Fraction(8, n)


def test_random_rectangular_certificates_fractions():
    rng = random.Random(1958)
    for _ in range(200):
        r, c = rng.randint(1, 5), rng.randint(1, 5)
        m = [[Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(c)] for _ in range(r)]
        v, x, y = solve_matrix_game(m)
        check_certificate(m, v, x, y)
        # The value of the transposed negated game is -v (swap the roles).
        mt = [[-m[i][j] for i in range(r)] for j in range(c)]
        assert solve_matrix_game(mt)[0] == -v
        # Adding a constant shifts the value by the same constant.
        assert solve_matrix_game([[a + 3 for a in row] for row in m])[0] == v + 3
