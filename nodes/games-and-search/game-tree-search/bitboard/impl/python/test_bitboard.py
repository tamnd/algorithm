# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitboard/. The authors are listed in prov/EHAYPB.jsonl.

import random
import unittest

from bitboard import ConnectFour, bits, popcount, ttt_has_line, ttt_moves, ttt_play

# ---------------------------------------------------------------- array versions

ARRAY_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def arr_ttt_winner(board):
    for a, b, c in ARRAY_LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]
    return None


def arr_ttt_moves(board):
    if arr_ttt_winner(board) is not None:
        return []
    return [i for i in range(9) if board[i] == "."]


def arr_ttt_play(board, i):
    p = "X" if board.count("X") == board.count("O") else "O"
    return board[:i] + p + board[i + 1 :]


def arr_c4_moves(grid, h):
    if arr_c4_last_won(grid, h):
        return []
    return [c for c in range(len(grid)) if grid[c][h - 1] == 0]


def arr_c4_play(grid, c):
    n = sum(v != 0 for col in grid for v in col)
    g = [col[:] for col in grid]
    r = g[c].index(0)
    g[c][r] = 1 if n % 2 == 0 else 2
    return g


LINE_CACHE = {}


def arr_c4_lines(w, h):
    """All lines of four cells, as lists of (column, row), found by a scan of the grid."""
    if (w, h) not in LINE_CACHE:
        out = []
        for c in range(w):
            for r in range(h):
                for dc, dr in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    cells = [(c + k * dc, r + k * dr) for k in range(4)]
                    if all(0 <= x < w and 0 <= y < h for x, y in cells):
                        out.append(cells)
        LINE_CACHE[(w, h)] = out
    return LINE_CACHE[(w, h)]


def arr_c4_has_four(grid, h, p):
    return any(all(grid[x][y] == p for x, y in cells) for cells in arr_c4_lines(len(grid), h))


def arr_c4_last_won(grid, h):
    n = sum(v != 0 for col in grid for v in col)
    if n == 0:
        return False
    return arr_c4_has_four(grid, h, 1 if n % 2 == 1 else 2)


class TestBitboard(unittest.TestCase):
    def test_bit_tools(self):
        rng = random.Random(3)
        for _ in range(500):
            b = rng.getrandbits(rng.randint(0, 80))
            self.assertEqual(list(bits(b)), [i for i in range(b.bit_length()) if b >> i & 1])
            self.assertEqual(popcount(b), sum(1 for i in range(b.bit_length()) if b >> i & 1))

    def test_tictactoe_all_reachable_positions(self):
        seen = {}
        stack = [(0, 0, "." * 9)]
        while stack:
            x, o, board = stack.pop()
            if board in seen:
                self.assertEqual(seen[board], (x, o))
                continue
            seen[board] = (x, o)
            self.assertEqual(ttt_has_line(x), arr_ttt_winner(board) == "X")
            self.assertEqual(ttt_has_line(o), arr_ttt_winner(board) == "O")
            mv = ttt_moves(x, o)
            self.assertEqual(mv, arr_ttt_moves(board))
            for i in mv:
                nx, no = ttt_play(x, o, i)
                stack.append((nx, no, arr_ttt_play(board, i)))
        self.assertEqual(len(seen), 5478)

    def check_connect_four(self, w, h):
        game = ConnectFour(w, h)
        seen = {}
        stack = [(0, 0, [[0] * h for _ in range(w)])]
        while stack:
            cur, mask, grid = stack.pop()
            key = tuple(map(tuple, grid))
            if key in seen:
                self.assertEqual(seen[key], (cur, mask))
                continue
            seen[key] = (cur, mask)
            self.assertEqual(game.to_grid(cur, mask), grid)
            self.assertEqual(mask & ~game.board, 0)  # no stone in a guard bit
            self.assertEqual(game.won(cur ^ mask), arr_c4_last_won(grid, h))
            to_move = 1 if popcount(mask) % 2 == 0 else 2
            self.assertEqual(game.won(cur), arr_c4_has_four(grid, h, to_move))
            mv = game.moves(cur, mask)
            self.assertEqual(mv, arr_c4_moves(grid, h))
            for c in mv:
                ncur, nmask = game.play(cur, mask, c)
                stack.append((ncur, nmask, arr_c4_play(grid, c)))
        return len(seen)

    def test_connect_four_4x4_all_reachable_positions(self):
        self.assertEqual(self.check_connect_four(4, 4), 161029)

    def test_connect_four_other_shapes(self):
        for w, h in ((1, 6), (6, 1), (2, 5), (5, 2), (3, 4)):
            self.check_connect_four(w, h)

    def test_connect_four_random_games_7x6(self):
        rng = random.Random(42)
        game = ConnectFour(7, 6)
        for _ in range(100):
            cur, mask, grid = 0, 0, [[0] * 6 for _ in range(7)]
            while True:
                mv = game.moves(cur, mask)
                self.assertEqual(mv, arr_c4_moves(grid, 6))
                self.assertEqual(game.won(cur ^ mask), arr_c4_last_won(grid, 6))
                if not mv:
                    break
                c = rng.choice(mv)
                cur, mask = game.play(cur, mask, c)
                grid = arr_c4_play(grid, c)
                self.assertEqual(game.to_grid(cur, mask), grid)


if __name__ == "__main__":
    unittest.main()
