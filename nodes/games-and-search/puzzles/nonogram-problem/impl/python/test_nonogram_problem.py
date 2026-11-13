# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonogram-problem/. The authors are listed in prov/EV9FYH.jsonl.

import itertools
import random

from nonogram_problem import clue_of, line_solve, line_solver_only, solve


def brute_line(clue, line):
    """Forced values of a line by listing all 2^L fillings."""
    fits = [f for f in itertools.product((0, 1), repeat=len(line))
            if clue_of(f) == list(clue) and all(v == -1 or v == x for v, x in zip(line, f))]
    if not fits:
        return None
    return [f0[0] if len(set(f0)) == 1 else -1 for f0 in zip(*fits)]


def clues_of_grid(grid):
    rows = [clue_of(row) for row in grid]
    cols = [clue_of([row[c] for row in grid]) for c in range(len(grid[0]))]
    return rows, cols


def brute_board(rows, cols):
    h, w = len(rows), len(cols)
    out = []
    for bits in itertools.product((0, 1), repeat=h * w):
        grid = [list(bits[r * w:(r + 1) * w]) for r in range(h)]
        if clues_of_grid(grid) == (rows, cols):
            out.append(grid)
    return out


def brute_board_by_rows(rows, cols):
    """All boards: each row is one of its fillings that match its clue."""
    w = len(cols)
    options = [[list(f) for f in itertools.product((0, 1), repeat=w) if clue_of(f) == clue] for clue in rows]
    out = []
    for pick in itertools.product(*options):
        grid = [list(row) for row in pick]
        if clues_of_grid(grid)[1] == cols:
            out.append(grid)
    return out


def key(grid):
    return tuple(tuple(row) for row in grid)


def test_line_solver_examples() -> None:
    # A block of 6 in 10 cells forces the middle 2 cells.
    assert line_solve([6], [-1] * 10) == [-1] * 4 + [1, 1] + [-1] * 4
    assert line_solve([3, 1], [-1] * 5) == [1, 1, 1, 0, 1]
    assert line_solve([], [-1, -1]) == [0, 0]
    assert line_solve([2], [1, -1, -1, 1]) is None
    assert line_solve([1], []) is None


def test_line_solver_against_enumeration() -> None:
    rng = random.Random(7)
    for _ in range(1500):
        n = rng.randint(1, 10)
        filling = [rng.randint(0, 1) for _ in range(n)]
        clue = clue_of(filling) if rng.random() < 0.7 else clue_of([rng.randint(0, 1) for _ in range(n)])
        line = [v if rng.random() < 0.3 else -1 for v in filling]
        if rng.random() < 0.2:
            line = [rng.choice((-1, -1, 0, 1)) for _ in range(n)]
        assert line_solve(clue, line) == brute_line(clue, line)


def test_full_solver_against_brute_force() -> None:
    rng = random.Random(9)
    for _ in range(40):
        h, w = rng.randint(1, 3), rng.randint(1, 4)
        grid = [[rng.randint(0, 1) for _ in range(w)] for _ in range(h)]
        rows, cols = clues_of_grid(grid)
        if rng.random() < 0.3:
            cols[rng.randrange(w)] = clue_of([rng.randint(0, 1) for _ in range(h)])
        expected = {key(g) for g in brute_board(rows, cols)}
        assert {key(g) for g in solve(rows, cols)} == expected


def test_full_solver_on_5x5_against_row_enumeration() -> None:
    rng = random.Random(10)
    for _ in range(12):
        grid = [[1 if rng.random() < 0.55 else 0 for _ in range(5)] for _ in range(5)]
        rows, cols = clues_of_grid(grid)
        expected = {key(g) for g in brute_board_by_rows(rows, cols)}
        assert key(grid) in expected
        assert {key(g) for g in solve(rows, cols)} == expected


def test_line_solving_can_stall() -> None:
    # Two solutions: the diagonal and the antidiagonal. Line solving fixes no cell.
    rows, cols = [[1], [1]], [[1], [1]]
    assert line_solver_only(rows, cols) == [[-1, -1], [-1, -1]]
    assert len(solve(rows, cols)) == 2
    # One solution, and still no cell is fixed by line solving.
    rows, cols = [[1], [1], [1, 1], [2]], [[1], [1], [2], [2]]
    assert line_solver_only(rows, cols) == [[-1] * 4 for _ in range(4)]
    sols = solve(rows, cols)
    assert sols == [[[0, 0, 0, 1], [0, 0, 0, 1], [1, 0, 1, 0], [0, 1, 1, 0]]]
    assert {key(g) for g in sols} == {key(g) for g in brute_board_by_rows(rows, cols)}
