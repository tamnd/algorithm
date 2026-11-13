# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jigsaw-puzzle-problem/. The authors are listed in prov/9JN0A4.jsonl.

import random

from jigsaw_puzzle_problem import (assemble_unique, count_solutions, has_unique_matches, is_solution,
                                   make_puzzle)


def test_generated_puzzles_are_solved() -> None:
    rng = random.Random(1)
    for _ in range(40):
        m, n = rng.randint(1, 4), rng.randint(2, 4)
        pieces, grid = make_puzzle(m, n, rng.randint(1, 3), rng)
        assert is_solution(pieces, grid)
        assert count_solutions(pieces, m, n, limit=1) == 1


def test_unique_matches_give_one_assembly_found_greedily() -> None:
    rng = random.Random(2)
    for _ in range(40):
        m, n = rng.randint(2, 5), rng.randint(2, 5)
        pieces, grid = make_puzzle(m, n, 10 ** 6, rng)
        assert has_unique_matches(pieces)
        assert assemble_unique(pieces, m, n) == grid
        assert count_solutions(pieces, m, n) == 1
    # a large puzzle is assembled by table lookups alone
    pieces, grid = make_puzzle(60, 80, 10 ** 9, rng)
    assert has_unique_matches(pieces) and assemble_unique(pieces, 60, 80) == grid


def test_few_shapes_give_many_assemblies() -> None:
    rng = random.Random(3)
    counts = []
    for _ in range(10):
        pieces, grid = make_puzzle(4, 5, 1, rng)
        counts.append(count_solutions(pieces, 4, 5))
    assert min(counts) >= 1 and max(counts) > 1


def test_worked_example() -> None:
    pieces = [(0, 1, 2, 0), (0, 0, -3, -1), (-2, 4, 0, 0), (3, 0, 0, -4)]  # A, B, C, D
    assert has_unique_matches(pieces)
    assert assemble_unique(pieces, 2, 2) == [[0, 1], [2, 3]]
    assert count_solutions(pieces, 2, 2) == 1


def test_broken_puzzle() -> None:
    rng = random.Random(4)
    pieces, grid = make_puzzle(3, 4, 10 ** 6, rng)
    i = grid[1][1]
    top, right, bottom, left = pieces[i]
    pieces[i] = (top, right + 1, bottom, left)  # a tab that fits no blank
    assert assemble_unique(pieces, 3, 4) is None
    assert count_solutions(pieces, 3, 4) == 0
