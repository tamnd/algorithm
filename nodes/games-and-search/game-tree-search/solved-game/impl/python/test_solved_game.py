# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/solved-game/. The authors are listed in prov/97PW5C.jsonl.

import unittest
from collections import Counter
from fractions import Fraction

from solved_game import (
    EMPTY,
    guaranteed,
    reachable,
    solve_all,
    tree_statistics,
    ttt_canonical,
    ttt_max_to_move,
    ttt_moves,
    ttt_outcome,
    value_keeping_strategy,
)


def walk_tree(start, moves, outcome):
    """Brute force: visit every node of the game tree with an explicit stack."""
    per_depth, leaves, edges, outcomes = Counter(), 0, 0, Counter()
    stack = [(start, 0)]
    while stack:
        p, d = stack.pop()
        per_depth[d] += 1
        kids = moves(p)
        if not kids:
            leaves += 1
            outcomes[outcome(p)] += 1
        edges += len(kids)
        stack.extend((c, d + 1) for c in kids)
    return [per_depth[i] for i in range(len(per_depth))], leaves, edges, dict(outcomes)


def recursive_value(p):
    """Direct recursive minimax, as a reference for the strong solution."""
    kids = ttt_moves(p)
    if not kids:
        return ttt_outcome(p)
    vals = [recursive_value(c) for c in kids]
    return max(vals) if ttt_max_to_move(p) else min(vals)


class TestTicTacToe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.positions = reachable(EMPTY, ttt_moves)
        cls.value = solve_all(EMPTY, ttt_moves, ttt_outcome, ttt_max_to_move)
        cls.stats = tree_statistics(EMPTY, ttt_moves, ttt_outcome)

    def test_tictactoe_is_a_draw(self):
        self.assertEqual(self.value[EMPTY], 0)

    def test_position_counts(self):
        self.assertEqual(len(self.positions), 5478)
        self.assertEqual(len(self.value), 5478)
        terminal = [p for p in self.positions if not ttt_moves(p)]
        self.assertEqual(len(terminal), 958)
        self.assertEqual(len({ttt_canonical(p) for p in self.positions}), 765)
        self.assertEqual(len({ttt_canonical(p) for p in terminal}), 138)
        live = [p for p in self.positions if ttt_moves(p)]
        self.assertEqual(len(live), 4520)
        self.assertEqual(sum(len(ttt_moves(p)) for p in live), 16167)

    def test_values_of_all_positions(self):
        self.assertEqual(Counter(self.value.values()), {1: 2936, -1: 1474, 0: 1068})

    def test_strong_solution_matches_recursion(self):
        # Every position with at least 4 marks, and samples of those with 2 and 3.
        two = sorted(p for p in self.positions if p.count(".") == 7)
        three = sorted(p for p in self.positions if p.count(".") == 6)
        many = [p for p in self.positions if p.count(".") <= 5]
        for p in two[::12] + three[::4] + many:
            self.assertEqual(self.value[p], recursive_value(p))

    def test_first_moves_and_replies(self):
        for i in range(9):
            self.assertEqual(self.value[EMPTY[:i] + "X" + EMPTY[i + 1 :]], 0)
        centre = "....X...."
        replies = {i: self.value[centre[:i] + "O" + centre[i + 1 :]] for i in range(9) if i != 4}
        self.assertEqual(replies, {0: 0, 2: 0, 6: 0, 8: 0, 1: 1, 3: 1, 5: 1, 7: 1})
        corner = "X........"
        replies = {i: self.value[corner[:i] + "O" + corner[i + 1 :]] for i in range(1, 9)}
        self.assertEqual([i for i, v in replies.items() if v == 0], [4])
        self.assertTrue(all(v == 1 for i, v in replies.items() if i != 4))

    def test_tree_counts(self):
        s = self.stats
        self.assertEqual(s["per_depth"], [1, 9, 72, 504, 3024, 15120, 54720, 148176, 200448, 127872])
        self.assertEqual(s["nodes"], 549946)
        self.assertEqual(s["leaves"], 255168)
        self.assertEqual(s["inner"], 294778)
        self.assertEqual(s["edges"], 549945)
        self.assertEqual(s["outcomes"], {1: 131184, -1: 77904, 0: 46080})
        self.assertEqual(round(s["edges"] / s["inner"], 4), 1.8656)
        self.assertEqual(round(s["total_length"] / s["leaves"], 4), 8.2545)

    def test_tree_counts_match_a_full_walk_of_a_subtree(self):
        for start in ("....X....", "X...O....", "X........"):
            per_depth, leaves, edges, outcomes = walk_tree(start, ttt_moves, ttt_outcome)
            s = tree_statistics(start, ttt_moves, ttt_outcome)
            self.assertEqual(s["per_depth"], per_depth)
            self.assertEqual(s["leaves"], leaves)
            self.assertEqual(s["edges"], edges)
            self.assertEqual(s["outcomes"], outcomes)
        self.assertEqual(walk_tree("....X....", ttt_moves, ttt_outcome)[1], 25872)

    def test_weak_solution_never_loses(self):
        strat = value_keeping_strategy(self.value, ttt_moves)
        # X follows the strategy against every line of O, and the other way round.
        self.assertEqual(guaranteed(EMPTY, ttt_moves, ttt_outcome, ttt_max_to_move, strat, True), 0)
        self.assertEqual(guaranteed(EMPTY, ttt_moves, ttt_outcome, ttt_max_to_move, strat, False), 0)
        # The strategy keeps the value from every position, not only from the start.
        for p in sorted(self.positions)[::11]:
            if ttt_moves(p):
                self.assertGreaterEqual(guaranteed(p, ttt_moves, ttt_outcome, ttt_max_to_move, strat, True), self.value[p])
                self.assertLessEqual(guaranteed(p, ttt_moves, ttt_outcome, ttt_max_to_move, strat, False), self.value[p])

    def test_a_poor_strategy_is_caught(self):
        # X always takes the first empty square: O can then win.
        naive = {p: ttt_moves(p)[0] for p in self.positions if ttt_moves(p)}
        self.assertEqual(guaranteed(EMPTY, ttt_moves, ttt_outcome, ttt_max_to_move, naive, True), -1)


class TestSubtractionGame(unittest.TestCase):
    """Take 1 or 2 counters; the player who takes the last counter wins.
    A position is (counters, MAX to move). Closed form: the mover wins iff n % 3 != 0."""

    @staticmethod
    def moves(p):
        n, mx = p
        return [(n - k, not mx) for k in (1, 2) if k <= n]

    @staticmethod
    def outcome(p):
        n, mx = p
        return -1 if mx else 1  # the player to move at 0 counters has lost

    def test_strong_solution_matches_formula(self):
        for n in range(0, 60):
            for mx in (True, False):
                value = solve_all((n, mx), self.moves, self.outcome, lambda p: p[1])
                for (m, who), v in value.items():
                    mover_wins = m % 3 != 0
                    self.assertEqual(v, (1 if who else -1) if mover_wins else (-1 if who else 1))

    def test_four_counters_has_five_games(self):
        s = tree_statistics((4, True), self.moves, self.outcome)
        self.assertEqual(s["leaves"], 5)
        # The game is impartial, so the graph needs only the counts 0 to 4.
        self.assertEqual(reachable(4, lambda n: [n - k for k in (1, 2) if k <= n]), {0, 1, 2, 3, 4})

    def test_exact_values(self):
        # Fractions as outcomes are kept exact.
        value = solve_all((5, True), self.moves, lambda p: Fraction(-1 if p[1] else 1, 3), lambda p: p[1])
        self.assertEqual(value[(5, True)], Fraction(1, 3))


class TestCycleGuard(unittest.TestCase):
    def test_cycle_is_reported(self):
        moves = {"a": ["b"], "b": ["a", "c"], "c": []}
        with self.assertRaises(ValueError):
            solve_all("a", lambda p: moves[p], lambda p: 0, lambda p: p == "a")


if __name__ == "__main__":
    unittest.main()
