# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peg-solitaire/. The authors are listed in prov/ZW9A3T.jsonl.
import random
import unittest

from peg_solitaire import (
    TRIANGULAR,
    apply,
    cell_index,
    english_board,
    french_board,
    full,
    golden_pagoda,
    is_pagoda,
    jumps,
    legal,
    moves,
    pagoda_value,
    position_class,
    reachable,
    rectangle_board,
    single_peg_finishes,
    solve,
    triangle_board,
)


def replay(start, solution):
    pos = start
    for j in solution:
        assert legal(pos, j)
        pos = apply(pos, j)
    return pos


class TestEnglishBoard(unittest.TestCase):
    def setUp(self):
        self.board = english_board()
        self.jumps = jumps(self.board)
        self.centre = cell_index(self.board)[(0, 0)]

    def test_size(self):
        self.assertEqual(len(self.board), 33)
        self.assertEqual(len(self.jumps), 76)

    def test_central_game(self):
        start = full(self.board) ^ (1 << self.centre)
        sol = solve(self.jumps, start, 1 << self.centre)
        self.assertIsNotNone(sol)
        self.assertEqual(len(sol), 31)
        self.assertEqual(replay(start, sol), 1 << self.centre)
        self.assertGreaterEqual(moves(sol), 18)
        # Reversed, with pegs and holes swapped, a solution is again a solution.
        everything = full(self.board)
        self.assertEqual(replay(everything ^ (1 << self.centre), sol[::-1]), 1 << self.centre)
        self.assertEqual(everything ^ start, 1 << self.centre)

    def test_rule_of_three(self):
        start = full(self.board) ^ (1 << self.centre)
        cls = position_class(self.board, start)
        ends = sorted(self.board[i] for i in range(33) if position_class(self.board, 1 << i) == cls)
        self.assertEqual(ends, [(-3, 0), (0, -3), (0, 0), (0, 3), (3, 0)])


class TestPositionClasses(unittest.TestCase):
    def test_jumps_keep_the_class(self):
        rnd = random.Random(1)
        for board in (english_board(), french_board(), rectangle_board(5, 4)):
            js = jumps(board)
            for _ in range(2000):
                pos = rnd.getrandbits(len(board))
                for j in js:
                    if legal(pos, j):
                        self.assertEqual(position_class(board, apply(pos, j)), position_class(board, pos))

    def test_french_central_game_is_impossible(self):
        board = french_board()
        self.assertEqual(len(board), 37)
        start = full(board) ^ (1 << cell_index(board)[(0, 0)])
        cls = position_class(board, start)
        self.assertEqual([i for i in range(37) if position_class(board, 1 << i) == cls], [])

    def test_finishes_against_breadth_first_search(self):
        expected = {(3, 3): 0, (3, 4): 8, (4, 4): 8, (3, 5): 2}
        for (w, h), count in expected.items():
            board = rectangle_board(w, h)
            js = jumps(board)
            solvable = 0
            for v in range(len(board)):
                start = full(board) ^ (1 << v)
                ends = single_peg_finishes(board, js, start)
                for e in ends:
                    self.assertEqual(position_class(board, 1 << e), position_class(board, start))
                solvable += bool(ends)
            self.assertEqual(solvable, count, (w, h))


class TestTriangle(unittest.TestCase):
    def test_fifteen_holes_every_start_solvable(self):
        board = triangle_board(5)
        js = jumps(board, TRIANGULAR)
        self.assertEqual(len(js), 36)
        for v in range(15):
            start = full(board) ^ (1 << v)
            ends = single_peg_finishes(board, js, start)
            self.assertTrue(ends)
            for e in range(15):
                sol = solve(js, start, 1 << e)
                self.assertEqual(sol is not None, e in ends)
                if sol is not None:
                    self.assertEqual(replay(start, sol), 1 << e)

    def test_ten_holes(self):
        board = triangle_board(4)
        js = jumps(board, TRIANGULAR)
        idx = cell_index(board)
        solvable = {board[v] for v in range(10) if single_peg_finishes(board, js, full(board) ^ (1 << v))}
        self.assertEqual(solvable, set(board) - {(0, 0), (0, 3), (3, 3), (1, 2)})
        self.assertEqual(reachable(js, full(board) ^ (1 << idx[(1, 2)])), {full(board) ^ (1 << idx[(1, 2)])})


class TestPagoda(unittest.TestCase):
    def test_golden_weights_are_pagoda(self):
        for board in (english_board(), french_board(), rectangle_board(6, 5)):
            for t in board:
                self.assertTrue(is_pagoda(golden_pagoda(board, t), jumps(board)))

    def test_not_every_weighting_is_pagoda(self):
        board = rectangle_board(3, 1)
        self.assertFalse(is_pagoda([0, 0, 1], jumps(board)))

    def test_pruning_keeps_answers(self):
        board = rectangle_board(4, 4)
        js = jumps(board)
        for v in range(16):
            start = full(board) ^ (1 << v)
            ends = single_peg_finishes(board, js, start)
            for e in range(16):
                w = golden_pagoda(board, board[e])
                sol = solve(js, start, 1 << e, prune=lambda p: pagoda_value(w, p) < w[e] - 1e-9)
                self.assertEqual(sol is not None, e in ends)

    def test_value_never_increases(self):
        rnd = random.Random(2)
        board = english_board()
        js = jumps(board)
        w = golden_pagoda(board, (0, 0))
        for _ in range(200):
            pos = full(board) ^ (1 << rnd.randrange(33))
            while True:
                legal_jumps = [j for j in js if legal(pos, j)]
                if not legal_jumps:
                    break
                nxt = apply(pos, rnd.choice(legal_jumps))
                self.assertLessEqual(pagoda_value(w, nxt), pagoda_value(w, pos) + 1e-9)
                pos = nxt


class TestMoves(unittest.TestCase):
    def test_runs_count_once(self):
        # A peg jumps 0 -> 2 -> 4 (one move), then another peg jumps (a second move).
        self.assertEqual(moves([(0, 1, 2), (2, 3, 4), (7, 6, 5)]), 2)
        self.assertEqual(moves([]), 0)


if __name__ == "__main__":
    unittest.main()
