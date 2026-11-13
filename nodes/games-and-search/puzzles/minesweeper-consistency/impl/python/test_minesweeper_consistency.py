# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minesweeper-consistency/. The authors are listed in prov/G792KA.jsonl.

import random
from fractions import Fraction

from minesweeper_consistency import analyze, brute_force, consistent, mine_cells, safe_cells


def random_board(rng, h, w, density, reveal):
    mines = {(r, c) for r in range(h) for c in range(w) if rng.random() < density}
    board = [[None] * w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if (r, c) not in mines and rng.random() < reveal:
                board[r][c] = sum((r + dr, c + dc) in mines
                                  for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc)
    return board, len(mines)


def test_one_two_one() -> None:
    board = [[None, None, None],
             [1, 2, 1]]
    assert mine_cells(board) == [(0, 0), (0, 2)]
    assert safe_cells(board) == [(0, 1)]


def test_fifty_fifty() -> None:
    board = [[None, None],
             [1, 1]]
    assert analyze(board) == {(0, 0): Fraction(1, 2), (0, 1): Fraction(1, 2)}
    assert safe_cells(board) == [] and mine_cells(board) == []


def test_inconsistent() -> None:
    assert not consistent([[None, 3], [1, None]])
    assert not consistent([[1, 0]])
    assert not consistent([[None, None], [1, 1]], total=0)
    assert consistent([[None, None], [1, 1]], total=1)


def test_against_enumeration_of_placements() -> None:
    rng = random.Random(51)
    for _ in range(150):
        h, w = rng.randint(1, 4), rng.randint(1, 4)
        board, total = random_board(rng, h, w, rng.uniform(0.1, 0.5), rng.uniform(0.2, 0.8))
        if rng.random() < 0.2:
            r, c = rng.randrange(h), rng.randrange(w)
            board[r][c] = rng.randint(0, 3)
        assert analyze(board) == brute_force(board)
        assert analyze(board, total) == brute_force(board, total)
        t = rng.randint(0, h * w)
        assert analyze(board, t) == brute_force(board, t)


def test_larger_boards_with_two_components() -> None:
    rng = random.Random(52)
    for _ in range(8):
        board, total = random_board(rng, 3, 5, 0.3, 0.5)
        unknown = sum(v is None for row in board for v in row)
        if unknown > 13:
            continue
        assert analyze(board, total) == brute_force(board, total)
