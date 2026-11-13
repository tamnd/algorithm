# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sudoku/. The authors are listed in prov/5N96QY.jsonl.

import itertools
import random

from sudoku import (
    exact_cover_model,
    is_complete_solution,
    latin_to_sudoku,
    solve_backtracking,
    solve_exact_cover,
    sudoku_to_latin,
)


def key(grid):
    return tuple(v for row in grid for v in row)


def brute_force_4x4():
    """Every 4 by 4 Sudoku grid: try all choices of a permutation for each row.

    A prefix of rows is dropped as soon as a column or a box repeats a symbol,
    so the loop visits each row choice that a full grid could still use.
    """
    perms = list(itertools.permutations(range(1, 5)))
    found = set()

    def fits(rows):
        k = len(rows)
        for c in range(4):
            if len({rows[r][c] for r in range(k)}) < k:
                return False
        for r0 in range(0, k, 2):
            for c0 in (0, 2):
                cells = [rows[r][c] for r in range(r0, min(r0 + 2, k)) for c in (c0, c0 + 1)]
                if len(set(cells)) < len(cells):
                    return False
        return True

    stack = [[]]
    while stack:
        rows = stack.pop()
        if len(rows) == 4:
            assert is_complete_solution(2, [list(p) for p in rows])
            found.add(key(rows))
            continue
        for p in perms:
            if fits(rows + [p]):
                stack.append(rows + [p])
    return found


ALL_4X4 = brute_force_4x4()

WIKI = ["530070000", "600195000", "098000060", "800060003", "400803001",
        "700020006", "060000280", "000419005", "000080079"]
WIKI_SOLUTION = ["534678912", "672195348", "198342567", "859761423", "426853791",
                 "713924856", "961537284", "287419635", "345286179"]
SEVENTEEN = "000000010400000000020000000000050407008000300001090000300400200050100000000806000"


def parse(rows):
    return [[int(ch) for ch in row] for row in rows]


def test_count_of_4x4_grids() -> None:
    assert len(ALL_4X4) == 288
    empty = [[0] * 4 for _ in range(4)]
    assert {key(g) for g in solve_exact_cover(2, empty)} == ALL_4X4
    assert {key(g) for g in solve_backtracking(2, empty)} == ALL_4X4


def test_exact_cover_size() -> None:
    items, options = exact_cover_model(3, [[0] * 9 for _ in range(9)])
    assert len(items) == 324
    assert len(options) == 729
    assert all(len(its) == 4 for its in options.values())


def test_random_4x4_puzzles_against_brute_force() -> None:
    rng = random.Random(11)
    grids = sorted(ALL_4X4)
    for trial in range(300):
        if trial % 3 == 0:
            # A random partial grid, which may have no completion.
            flat = [rng.choice([0, 0, 0, 1, 2, 3, 4]) for _ in range(16)]
        else:
            source = rng.choice(grids)
            flat = [v if rng.random() < 0.3 else 0 for v in source]
        puzzle = [flat[4 * r:4 * r + 4] for r in range(4)]
        expected = {g for g in ALL_4X4 if all(f == 0 or f == x for f, x in zip(flat, g))}
        assert {key(g) for g in solve_exact_cover(2, puzzle)} == expected
        assert {key(g) for g in solve_backtracking(2, puzzle)} == expected


def test_known_9x9_puzzles_have_one_solution() -> None:
    puzzle = parse(WIKI)
    a = solve_exact_cover(3, puzzle, limit=2)
    b = solve_backtracking(3, puzzle, limit=2)
    assert a == b == [parse(WIKI_SOLUTION)]
    hard = parse([SEVENTEEN[9 * r:9 * r + 9] for r in range(9)])
    assert sum(1 for v in SEVENTEEN if v != "0") == 17
    a = solve_exact_cover(3, hard, limit=2)
    b = solve_backtracking(3, hard, limit=2)
    assert len(a) == 1 and a == b
    assert is_complete_solution(3, a[0])
    assert all(hard[r][c] in (0, a[0][r][c]) for r in range(9) for c in range(9))


def test_nine_by_nine_with_a_clash_has_no_solution() -> None:
    puzzle = parse(WIKI)
    puzzle[0][2] = 5  # two 5s in the first row
    assert solve_exact_cover(3, puzzle) == []
    assert solve_backtracking(3, puzzle) == []


def latin_completions(partial):
    """All Latin squares that agree with the partial array: each row is a permutation."""
    n = len(partial)
    out = set()
    perms = list(itertools.permutations(range(n)))
    for sq in itertools.product(perms, repeat=n):
        if any(partial[i][j] is not None and partial[i][j] != sq[i][j]
               for i in range(n) for j in range(n)):
            continue
        if all(len({sq[i][j] for i in range(n)}) == n for j in range(n)):
            out.add(tuple(v for row in sq for v in row))
    return out


def check_reduction(partial):
    n = len(partial)
    grid = latin_to_sudoku(partial)
    sols = solve_exact_cover(n, grid)
    back = {tuple(v for row in sudoku_to_latin(n, s) for v in row) for s in sols}
    assert len(back) == len(sols)
    assert back == latin_completions(partial)


def test_latin_square_reduction_order_2_all_inputs() -> None:
    for flat in itertools.product([None, 0, 1], repeat=4):
        check_reduction([list(flat[0:2]), list(flat[2:4])])


def test_latin_square_reduction_order_3_random() -> None:
    rng = random.Random(5)
    for _ in range(25):
        flat = [rng.choice([None, None, 0, 1, 2]) for _ in range(9)]
        check_reduction([flat[0:3], flat[3:6], flat[6:9]])
