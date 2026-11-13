# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kakuro-problem/. The authors are listed in prov/B6JK8Y.jsonl.

import itertools
import random

from kakuro_problem import digit_sets, runs, solve


def check(run_index, sums, filling):
    for cells, total in zip(run_index, sums):
        digits = [filling[c] for c in cells]
        if len(set(digits)) != len(digits) or sum(digits) != total:
            return False
    return True


def brute_force(board, sums, max_digit):
    """Every assignment of digits 1..max_digit to the white cells."""
    rs = runs(board)
    cells = sorted({cell for run in rs for cell in run})
    out = []
    for digits in itertools.product(range(1, max_digit + 1), repeat=len(cells)):
        filling = dict(zip(cells, digits))
        if check(rs, sums, filling):
            out.append(filling)
    return out


def brute_force_by_rows(board, sums, max_digit=9):
    """Every choice of digit tuples for the horizontal runs, then a test of the columns.

    Each white cell lies in exactly one horizontal run, so the product of the
    tuples of the horizontal runs lists every filling that satisfies the rows.
    """
    rs = runs(board)
    # The horizontal runs come first in runs(board); keep them.
    seen = set()
    horizontal = []
    for i, run in enumerate(rs):
        if not seen & set(run) and all(r == run[0][0] for r, _ in run):
            horizontal.append(i)
            seen |= set(run)
    choices = []
    for i in horizontal:
        k = len(rs[i])
        tuples = [p for p in itertools.permutations(range(1, max_digit + 1), k) if sum(p) == sums[i]]
        choices.append(tuples)
    out = []
    for pick in itertools.product(*choices):
        filling = {}
        for i, t in zip(horizontal, pick):
            filling.update(zip(rs[i], t))
        if check(rs, sums, filling):
            out.append(filling)
    return out


def key(filling):
    return tuple(sorted(filling.items()))


def random_board(rng, h, w, density):
    return ["".join("." if rng.random() < density else "#" for _ in range(w)) for _ in range(h)]


def random_instance(rng, board, max_digit, solvable):
    rs = runs(board)
    cells = sorted({cell for run in rs for cell in run})
    if solvable:
        for _ in range(100):
            trial = {cell: rng.randint(1, max_digit) for cell in cells}
            if all(len({trial[c] for c in run}) == len(run) for run in rs):
                return [sum(trial[c] for c in run) for run in rs]
    return [rng.randint(len(run), max_digit * len(run)) for run in rs]


def test_digit_table() -> None:
    assert digit_sets(2, 3) == [(1, 2)]
    assert digit_sets(2, 17) == [(8, 9)]
    assert digit_sets(3, 6) == [(1, 2, 3)]
    assert digit_sets(9, 45) == [tuple(range(1, 10))]
    assert digit_sets(2, 10) == [(1, 9), (2, 8), (3, 7), (4, 6)]
    total = sum(len(digit_sets(k, s)) for k in range(1, 10) for s in range(1, 46))
    assert total == 2 ** 9 - 1


def test_small_board_example() -> None:
    board = ["..", ".."]
    # Rows sum to 4 and 6, columns to 3 and 7.
    sols = solve(board, [4, 6, 3, 7])
    assert [key(s) for s in sols] == [key({(0, 0): 1, (0, 1): 3, (1, 0): 2, (1, 1): 4})]


def test_against_brute_force_digits_1_to_9() -> None:
    rng = random.Random(1)
    checked = 0
    while checked < 20:
        board = random_board(rng, rng.randint(2, 3), rng.randint(2, 3), 0.7)
        cells = {cell for run in runs(board) for cell in run}
        if not 1 <= len(cells) <= 4:
            continue
        sums = random_instance(rng, board, 9, rng.random() < 0.6)
        expected = {key(s) for s in brute_force(board, sums, 9)}
        got = solve(board, sums)
        assert len(got) == len(expected)
        assert {key(s) for s in got} == expected
        checked += 1


def test_against_brute_force_small_digits() -> None:
    rng = random.Random(2)
    checked = 0
    while checked < 30:
        board = random_board(rng, rng.randint(2, 4), rng.randint(2, 4), 0.75)
        cells = {cell for run in runs(board) for cell in run}
        if not 1 <= len(cells) <= 7:
            continue
        sums = random_instance(rng, board, 4, rng.random() < 0.5)
        expected = {key(s) for s in brute_force(board, sums, 4)}
        assert {key(s) for s in solve(board, sums, max_digit=4)} == expected
        checked += 1


def test_larger_boards_against_row_enumeration() -> None:
    rng = random.Random(4)
    checked = 0
    while checked < 12:
        board = random_board(rng, 4, 4, 0.7)
        cells = {cell for run in runs(board) for cell in run}
        if len(cells) < 8 or max(len(r) for r in runs(board)) > 3:
            continue
        sums = random_instance(rng, board, 9, True)
        expected = {key(s) for s in brute_force_by_rows(board, sums)}
        assert {key(s) for s in solve(board, sums)} == expected
        checked += 1


def test_unique_puzzle_with_blocks() -> None:
    board = ["..#", "...", "#.."]
    sol = {(0, 0): 9, (0, 1): 7, (1, 0): 8, (1, 1): 2, (1, 2): 1, (2, 1): 1, (2, 2): 3}
    sums = [sum(sol[c] for c in run) for run in runs(board)]
    found = solve(board, sums, limit=10)
    assert {key(s) for s in found} == {key(s) for s in brute_force_by_rows(board, sums)}
