# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hex-game/. The authors are listed in prov/S7E34P.jsonl.

import random
import unittest

from hex_game import connects, first_player_wins, full_board_winners, neighbors, play_out, solver, winner, winning_openings


class TestBoard(unittest.TestCase):
    def test_neighbors(self):
        nb = neighbors(3)
        self.assertEqual(sorted(nb[4]), [1, 2, 3, 5, 6, 7])  # the center has six
        self.assertEqual(sorted(nb[0]), [1, 3])  # an acute corner has two
        self.assertEqual(sorted(nb[2]), [1, 4, 5])  # an obtuse corner has three
        for n in range(1, 6):
            nb = neighbors(n)
            for v in range(n * n):
                for w in nb[v]:
                    self.assertIn(v, nb[w])

    def test_connects(self):
        # a red column on the left joins top and bottom
        self.assertTrue(connects(3, 0b001001001, True))
        # the short diagonal (0,2), (1,1), (2,0) is connected for both players
        diag = 1 << 2 | 1 << 4 | 1 << 6
        self.assertTrue(connects(3, diag, True))
        self.assertTrue(connects(3, diag, False))
        # the long diagonal (0,0), (1,1), (2,2) is not connected
        self.assertFalse(connects(3, 1 << 0 | 1 << 4 | 1 << 8, True))


class TestFullBoards(unittest.TestCase):
    def test_exactly_one_winner_on_every_full_board(self):
        for n in range(1, 5):
            for red in range(1 << (n * n)):
                r, b = full_board_winners(n, red)
                self.assertNotEqual(r, b, (n, red))

    def test_random_full_boards(self):
        rng = random.Random(1952)
        for n in range(5, 12):
            for _ in range(30):
                red, blue, _ = play_out(n, rng)
                self.assertEqual(connects(n, red, True), not connects(n, blue, False))


class TestSolver(unittest.TestCase):
    def test_first_player_wins_small_boards(self):
        for n in range(1, 4):
            self.assertTrue(first_player_wins(n), n)

    def test_winning_openings(self):
        self.assertEqual(winning_openings(1), [(0, 0)])
        self.assertEqual(winning_openings(2), [(0, 1), (1, 0)])
        self.assertEqual(winning_openings(3), [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)])

    def test_four_by_four(self):
        mover_wins = solver(4)
        self.assertTrue(mover_wins(0, 0))
        # the central cell (1, 1) loses on 4 x 4, and (1, 2) on the short diagonal wins
        self.assertTrue(mover_wins(1 << 5, 0))
        self.assertFalse(mover_wins(1 << 6, 0))

    def test_solver_against_plain_search(self):
        # random 3 x 3 positions: the memo solver agrees with plain minimax
        def plain(red, blue):
            if winner(3, red, blue):
                return False
            red_turn = bin(red).count("1") == bin(blue).count("1")
            for v in range(9):
                if not (red | blue) >> v & 1:
                    nr, nb = (red | 1 << v, blue) if red_turn else (red, blue | 1 << v)
                    if not plain(nr, nb):
                        return True
            return False

        rng = random.Random(7)
        mover_wins = solver(3)
        for _ in range(200):
            cells = rng.sample(range(9), rng.randint(0, 6))
            k = len(cells)
            red = sum(1 << v for v in cells[: (k + 1) // 2])
            blue = sum(1 << v for v in cells[(k + 1) // 2 :])
            if winner(3, red, blue):
                continue
            self.assertEqual(mover_wins(red, blue), plain(red, blue))


if __name__ == "__main__":
    unittest.main()
