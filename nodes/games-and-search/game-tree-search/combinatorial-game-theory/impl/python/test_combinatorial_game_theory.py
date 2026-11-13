# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combinatorial-game-theory/. The authors are listed in prov/JY9MWF.jsonl.

import random
import unittest

from combinatorial_game_theory import (
    DOWN,
    HALF,
    MINUS_ONE,
    ONE,
    PLUS_MINUS_ONE,
    QUARTER,
    STAR,
    TWO,
    UP,
    ZERO,
    Game,
    board,
    domineering,
    eq,
    fuzzy,
    ge,
    integer,
    lt,
    nimber,
    outcome,
)


class TestOutcomeClasses(unittest.TestCase):
    def test_basic_values(self):
        self.assertEqual(outcome(ZERO), "P")
        self.assertEqual(outcome(STAR), "N")
        self.assertEqual(outcome(ONE), "L")
        self.assertEqual(outcome(MINUS_ONE), "R")
        self.assertEqual(outcome(HALF), "L")
        self.assertEqual(outcome(UP), "L")
        self.assertEqual(outcome(PLUS_MINUS_ONE), "N")

    def test_sums_by_brute_force(self):
        self.assertEqual(outcome(STAR + STAR), "P")  # * + * = 0
        self.assertEqual(outcome(ONE + MINUS_ONE), "P")  # 1 - 1 = 0
        self.assertEqual(outcome(HALF + HALF + MINUS_ONE), "P")  # 1/2 + 1/2 = 1
        self.assertEqual(outcome(QUARTER + QUARTER - HALF), "P")
        self.assertEqual(outcome(UP + DOWN), "P")
        self.assertEqual(outcome(UP + STAR), "N")  # up-star is fuzzy with 0
        self.assertEqual(outcome(UP + UP + STAR), "L")  # double-up-star is positive
        self.assertEqual(outcome(PLUS_MINUS_ONE + PLUS_MINUS_ONE), "P")
        self.assertEqual(outcome(ONE + STAR), "L")

    def test_order(self):
        self.assertTrue(lt(ZERO, UP))
        self.assertTrue(lt(UP, QUARTER))
        self.assertTrue(lt(QUARTER, HALF))
        self.assertTrue(lt(HALF, ONE))
        self.assertTrue(fuzzy(UP, STAR))
        self.assertTrue(fuzzy(STAR, ZERO))
        self.assertTrue(fuzzy(PLUS_MINUS_ONE, ZERO))
        self.assertTrue(fuzzy(PLUS_MINUS_ONE, HALF))
        self.assertTrue(lt(PLUS_MINUS_ONE, TWO))

    def test_simplicity(self):
        self.assertTrue(eq(Game({MINUS_ONE}, {ONE}), ZERO))
        self.assertTrue(eq(Game({ZERO}, {TWO}), ONE))
        self.assertTrue(eq(Game({ONE}, {TWO}), ONE + HALF))
        self.assertTrue(eq(Game({STAR}, {STAR}), ZERO))
        self.assertTrue(eq(Game({ZERO, STAR}, {ZERO}), UP + STAR))

    def test_nimbers_add_by_xor(self):
        for a in range(4):
            for b in range(4):
                self.assertTrue(eq(nimber(a) + nimber(b), nimber(a ^ b)))
        rng = random.Random(3)
        for _ in range(5):
            a, b = rng.randint(4, 5), rng.randint(0, 2)
            self.assertTrue(eq(nimber(a) + nimber(b), nimber(a ^ b)))

    def test_values_born_by_day_two(self):
        from itertools import combinations

        day1 = [ZERO, STAR, ONE, MINUS_ONE]
        subsets = [s for r in range(5) for s in combinations(day1, r)]
        values = []
        for left in subsets:
            for right in subsets:
                g = Game(left, right)
                if not any(eq(g, h) for h in values):
                    values.append(g)
        self.assertEqual(len(values), 22)

    def test_integers(self):
        for a in range(-3, 4):
            for b in range(-3, 4):
                self.assertTrue(eq(integer(a) + integer(b), integer(a + b)))
                self.assertEqual(ge(integer(a), integer(b)), a >= b)


class TestDomineering(unittest.TestCase):
    def test_small_boards(self):
        self.assertTrue(eq(domineering(board(2, 1)), ONE))
        self.assertTrue(eq(domineering(board(1, 2)), MINUS_ONE))
        self.assertTrue(eq(domineering(board(3, 1)), ONE))
        self.assertTrue(eq(domineering(board(4, 1)), TWO))
        self.assertTrue(eq(domineering(board(2, 2)), PLUS_MINUS_ONE))
        # +-1 plus 1 is {2 | 0}: whoever moves first wins
        self.assertEqual(outcome(domineering(board(2, 2)) + domineering(board(2, 1))), "N")
        self.assertEqual(outcome(domineering(board(2, 2)) + TWO), "L")

    def test_sum_outcome_matches_disjoint_board(self):
        # two separate regions played as one board
        two_by_two = board(2, 2)
        strip = frozenset((r, 5) for r in range(4))
        self.assertEqual(
            outcome(domineering(two_by_two | strip)),
            outcome(domineering(two_by_two) + domineering(strip)),
        )
        self.assertEqual(outcome(domineering(two_by_two | strip)), "L")


if __name__ == "__main__":
    unittest.main()
