# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strategy-stealing-argument/. The authors are listed in prov/G3BS01.jsonl.

import random
import unittest

from strategy_stealing_argument import (
    chomp_mover_wins,
    chomp_steal_holds,
    chomp_winning_moves,
    hex_connects,
    hex_game,
    optimal_second_player,
    play_stolen,
    random_strategy,
    rectangle,
    tic_tac_toe,
)


def random_position(rng, game, max_stones):
    """A position where nobody has a winning set yet."""
    while True:
        cells = rng.sample(range(game.cells), rng.randint(0, max_stones))
        k = len(cells)
        a = sum(1 << v for v in cells[: (k + 1) // 2])
        b = sum(1 << v for v in cells[(k + 1) // 2 :])
        if not game.wins1(a) and not game.wins2(b):
            return a, b


class TestConclusion(unittest.TestCase):
    def test_hex_first_player_wins(self):
        for n in range(1, 4):
            self.assertEqual(hex_game(n, n).value(0, 0, 1), 1, n)

    def test_hex_full_boards_have_a_winner(self):
        # no draws: the hypothesis that turns "at least a draw" into a win
        for n in range(1, 4):
            full = (1 << (n * n)) - 1
            for a in range(full + 1):
                self.assertNotEqual(hex_connects(n, n, a, True), hex_connects(n, n, full & ~a, False))

    def test_tic_tac_toe_first_player_draws(self):
        # the argument gives "at least a draw"; search shows it is exactly a draw
        self.assertEqual(tic_tac_toe().value(0, 0, 1), 0)

    def test_chomp_first_player_wins_every_rectangle(self):
        for r in range(1, 6):
            for c in range(1, 8):
                self.assertEqual(chomp_mover_wins(rectangle(r, c)), (r, c) != (1, 1))
                if (r, c) != (1, 1):
                    self.assertTrue(chomp_steal_holds(rectangle(r, c)))

    def test_chomp_explicit_strategies(self):
        # squares: take (1, 1) and leave two equal arms; two rows: take the corner
        for n in range(2, 7):
            self.assertIn((1, 1), chomp_winning_moves(rectangle(n, n)))
            self.assertIn((1, n - 1), chomp_winning_moves(rectangle(2, n)))


class TestExtraStoneNeverHurts(unittest.TestCase):
    def check(self, game, seed, trials, max_stones):
        rng = random.Random(seed)
        for _ in range(trials):
            a, b = random_position(rng, game, max_stones)
            mover = rng.choice([1, 2])
            base = game.value(a, b, mover)
            for v in range(game.cells):
                if not (a | b) >> v & 1:
                    self.assertGreaterEqual(game.value(a | 1 << v, b, mover), base)
                    self.assertLessEqual(game.value(a, b | 1 << v, mover), base)

    def test_tic_tac_toe(self):
        self.check(tic_tac_toe(), 1, 300, 6)

    def test_hex(self):
        self.check(hex_game(3, 3), 2, 300, 6)


class TestStolenStrategy(unittest.TestCase):
    def all_opponent_plays(self, game, steal_from, first_cell):
        """Run the stolen strategy against every sequence of opponent moves."""
        results = []

        def explore(prefix):
            moves = iter(prefix)
            branch = {}

            def opponent(a, b):
                try:
                    return next(moves)
                except StopIteration:
                    branch["free"] = [i for i in range(game.cells) if not (a | b) >> i & 1]
                    raise

            try:
                results.append(play_stolen(game, steal_from, opponent, first_cell))
            except StopIteration:
                for c in branch["free"]:
                    explore(prefix + [c])

        explore([])
        return results

    def test_tic_tac_toe_never_loses(self):
        game = tic_tac_toe()
        s = optimal_second_player(game)
        for first in (0, 4, 1):
            results = self.all_opponent_plays(game, s, first)
            self.assertGreater(len(results), 10)
            self.assertTrue(all(real >= 0 for real, _ in results))

    def test_real_result_dominates_imagined(self):
        # with any stolen strategy: if the imagined second player wins first,
        # the real first player wins; the real first player loses only if the
        # imagined first player completed a set first
        rng = random.Random(3)
        for game in (tic_tac_toe(), hex_game(3, 3)):
            for _ in range(400):
                s = random_strategy(rng, game.cells)
                t = random_strategy(rng, game.cells)
                real, imagined = play_stolen(game, s, t, rng.randrange(game.cells))
                if imagined == 2:
                    self.assertEqual(real, 1)
                if real == -1:
                    self.assertEqual(imagined, 1)


class TestHypotheses(unittest.TestCase):
    def test_without_symmetry_the_second_player_can_win(self):
        # 3 rows and 2 columns: the first player must cross three rows
        self.assertEqual(hex_game(3, 2).value(0, 0, 1), -1)
        self.assertEqual(hex_game(2, 3).value(0, 0, 1), 1)

    def test_when_a_move_can_hurt(self):
        # Nim with heaps 1 and 1: the start looks the same to both players,
        # but every move helps the opponent, and the second player wins
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def wins(heaps):
            return any(not wins(tuple(sorted(heaps[:i] + (h - k,) + heaps[i + 1 :])))
                       for i, h in enumerate(heaps) for k in range(1, h + 1))

        self.assertFalse(wins((1, 1)))
        self.assertFalse(wins((2, 2)))


if __name__ == "__main__":
    unittest.main()
