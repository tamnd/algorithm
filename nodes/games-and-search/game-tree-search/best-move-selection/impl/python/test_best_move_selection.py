# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-move-selection/. The authors are listed in prov/Y4MTQZ.jsonl.

import math
import random
import unittest

from best_move_selection import Counter, alphabeta, best_move, iterative_deepening, negamax

# A test node is (static value for the side to move, tuple of children).


def node_moves(n):
    return n[1]


def node_eval(n):
    return n[0]


def random_node(rng, depth, b_lo=1, b_hi=4, leaf_p=0.15, root=True):
    if depth == 0 or (not root and rng.random() < leaf_p):
        return (rng.randint(-9, 9), ())
    return (rng.randint(-9, 9), tuple(random_node(rng, depth - 1, b_lo, b_hi, leaf_p, False) for _ in range(rng.randint(b_lo, b_hi))))


def brute(n, depth):
    """Reference: depth-limited negamax written out directly."""
    if depth == 0 or not n[1]:
        return n[0]
    return max(-brute(c, depth - 1) for c in n[1])


def from_lists(t, max_to_move=True):
    """Nested lists with MAX-view leaves -> test nodes with side-to-move leaves."""
    if not isinstance(t, list):
        return (t if max_to_move else -t, ())
    return (0, tuple(from_lists(c, not max_to_move) for c in t))


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def ttt_winner(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def ttt_moves(b):
    if ttt_winner(b) or "." not in b:
        return []
    p = "X" if b.count("X") == b.count("O") else "O"
    return [b[:i] + p + b[i + 1 :] for i in range(9) if b[i] == "."]


def ttt_eval(b):
    return -1 if ttt_winner(b) else 0  # a finished board is lost for the side to move if there is a line


class TestBestMove(unittest.TestCase):
    def test_chosen_move_has_the_root_value(self):
        rng = random.Random(123)
        for _ in range(400):
            root = random_node(rng, rng.randint(1, 5))
            if not root[1]:
                continue
            d = rng.randint(1, 5)
            for ab in (False, True):
                m, v = best_move(root, d, node_moves, node_eval, use_alphabeta=ab)
                self.assertEqual(v, brute(root, d))
                self.assertEqual(-brute(root[1][m], d - 1), v)

    def test_ties_go_to_the_first_best_move_and_alphabeta_agrees(self):
        rng = random.Random(9)
        for _ in range(400):
            root = random_node(rng, rng.randint(1, 4), leaf_p=0.3)
            if not root[1]:
                continue
            d = rng.randint(1, 4)
            vals = [-brute(c, d - 1) for c in root[1]]
            first_best = vals.index(max(vals))
            self.assertEqual(best_move(root, d, node_moves, node_eval, use_alphabeta=False)[0], first_best)
            self.assertEqual(best_move(root, d, node_moves, node_eval, use_alphabeta=True)[0], first_best)

    def test_fail_soft_bounds(self):
        rng = random.Random(55)
        for _ in range(1500):
            n = random_node(rng, rng.randint(1, 4))
            d = rng.randint(1, 4)
            a, b = sorted(rng.sample(range(-12, 13), 2))
            v = alphabeta(n, d, a, b, node_moves, node_eval, Counter())
            true = brute(n, d)
            if v <= a:
                self.assertLessEqual(true, v)
            elif v >= b:
                self.assertGreaterEqual(true, v)
            else:
                self.assertEqual(true, v)

    def test_page_example(self):
        root = from_lists([[[3, 17], [2, 12]], [[15, 25], [2, 5]]])
        self.assertEqual(best_move(root, 3, node_moves, node_eval), (0, 12))
        # A tie: both moves have value 4; the first is chosen, whatever the search.
        tie = from_lists([[4, 9], [7, 4]])
        self.assertEqual(best_move(tie, 2, node_moves, node_eval, use_alphabeta=False), (0, 4))
        self.assertEqual(best_move(tie, 2, node_moves, node_eval, use_alphabeta=True), (0, 4))
        # With the second move tried first, it is chosen instead.
        self.assertEqual(best_move(tie, 2, node_moves, node_eval, first=1), (1, 4))

    def test_tictactoe_replies(self):
        corner = "X........"
        m, v = best_move(corner, 8, ttt_moves, ttt_eval)
        self.assertEqual(ttt_moves(corner)[m], "X...O....")  # only the centre reply draws
        self.assertEqual(v, 0)
        centre = "....X...."
        m, v = best_move(centre, 8, ttt_moves, ttt_eval)
        self.assertEqual(ttt_moves(centre)[m], "O...X....")
        self.assertEqual(v, 0)
        # X to move with a win at square 2.
        m, v = best_move("XX.OO....", 5, ttt_moves, ttt_eval)
        self.assertEqual((ttt_moves("XX.OO....")[m], v), ("XXXOO....", 1))


class TestIterativeDeepening(unittest.TestCase):
    def test_unlimited_budget_matches_fixed_depth(self):
        rng = random.Random(31)
        for _ in range(200):
            root = random_node(rng, 5, b_lo=2)
            m, v, d = iterative_deepening(root, 5, node_moves, node_eval)
            self.assertEqual(d, 5)
            self.assertEqual(v, brute(root, 5))
            self.assertEqual(-brute(root[1][m], 4), v)

    def test_budget_keeps_the_last_finished_iteration(self):
        rng = random.Random(8)
        for _ in range(200):
            root = random_node(rng, 6, b_lo=2)
            budget = rng.randint(1, 400)
            m, v, d = iterative_deepening(root, 6, node_moves, node_eval, budget)
            if d == 0:
                self.assertIsNone(m)
                continue
            # The answer is that of a complete search to depth d ...
            self.assertEqual(v, brute(root, d))
            self.assertEqual(-brute(root[1][m], d - 1), v)
            # ... and the iteration to depth d + 1 did not fit in the budget.
            if d < 6:
                c = Counter()
                first = None
                for k in range(1, d + 2):
                    first, _ = best_move(root, k, node_moves, node_eval, first, True, c)
                self.assertGreater(c.nodes, budget)

    def test_no_iteration_finishes(self):
        root = random_node(random.Random(1), 3, b_lo=2)
        self.assertEqual(iterative_deepening(root, 3, node_moves, node_eval, 1), (None, root[0], 0))


if __name__ == "__main__":
    unittest.main()
