# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/negamax/. The authors are listed in prov/XN376A.jsonl.

import random
import unittest
from fractions import Fraction

from negamax import minimax_leaves_to_negamax, negamax, negamax_tree

PAGE_TREE = [[[3, 17], [2, 12]], [[15, 25], [2, 5]]]  # leaves are values for MAX


def minimax_ref(tree, max_to_move=True):
    """Reference: plain two-sided minimax on MAX-view leaves."""
    if not isinstance(tree, list):
        return tree
    vals = [minimax_ref(c, not max_to_move) for c in tree]
    return max(vals) if max_to_move else min(vals)


def build_uniform(leaves, b, d):
    if d == 0:
        return leaves[0]
    k = len(leaves) // b
    return [build_uniform(leaves[i * k : (i + 1) * k], b, d - 1) for i in range(b)]


def levelwise(leaves, b, d, max_root=True):
    """Brute force without recursion: reduce the leaf row from the bottom level up."""
    row = list(leaves)
    for depth in range(d - 1, -1, -1):
        f = max if (depth % 2 == 0) == max_root else min
        row = [f(row[i : i + b]) for i in range(0, len(row), b)]
    return row[0]


def random_tree(rng, depth, root=True):
    if depth == 0 or (not root and rng.random() < 0.3):
        return rng.randint(-50, 50)
    return [random_tree(rng, depth - 1, False) for _ in range(rng.randint(1, 4))]


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def ttt_winner(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def ttt_to_move(b):
    return "X" if b.count("X") == b.count("O") else "O"


def ttt_children(b):
    if ttt_winner(b) or "." not in b:
        return []
    p = ttt_to_move(b)
    return [b[:i] + p + b[i + 1 :] for i in range(9) if b[i] == "."]


def ttt_side_to_move_eval(b):
    w = ttt_winner(b)
    return 0 if w is None else (1 if w == ttt_to_move(b) else -1)


def ttt_x_eval(b):
    w = ttt_winner(b)
    return 1 if w == "X" else -1 if w == "O" else 0


class TestNegamax(unittest.TestCase):
    def test_page_example(self):
        t = minimax_leaves_to_negamax(PAGE_TREE)
        # The leaves are at depth 3, where MIN would move, so each one is negated.
        self.assertEqual(t, [[[-3, -17], [-2, -12]], [[-15, -25], [-2, -5]]])
        self.assertEqual(negamax_tree(t), 12)

    def test_uniform_trees_match_minimax_and_brute_force(self):
        rng = random.Random(4242)
        for b in range(2, 5):
            for d in range(1, 7):
                if b**d > 5000:
                    continue
                for _ in range(15):
                    leaves = [rng.randint(-30, 30) for _ in range(b**d)]
                    tree = build_uniform(leaves, b, d)
                    for max_root in (True, False):
                        count = [0]
                        v = negamax_tree(minimax_leaves_to_negamax(tree, max_root), count)
                        mm = minimax_ref(tree, max_root)
                        brute = levelwise(leaves, b, d, max_root)
                        self.assertEqual(mm, brute)
                        self.assertEqual(v, mm if max_root else -mm)
                        self.assertEqual(count[0], b**d)

    def test_irregular_trees_match_minimax(self):
        rng = random.Random(31337)
        for _ in range(2000):
            tree = random_tree(rng, rng.randint(0, 6))
            max_root = rng.random() < 0.5
            v = negamax_tree(minimax_leaves_to_negamax(tree, max_root))
            mm = minimax_ref(tree, max_root)
            self.assertEqual(v, mm if max_root else -mm)

    def test_fractions_stay_exact(self):
        rng = random.Random(5)
        for _ in range(200):
            tree = random_tree(rng, 4)
            ftree = minimax_leaves_to_negamax(tree)

            def to_frac(t):
                return [to_frac(c) for c in t] if isinstance(t, list) else Fraction(t, 7)

            v = negamax_tree(to_frac(ftree))
            self.assertIsInstance(v, Fraction)
            self.assertEqual(v, Fraction(minimax_ref(tree), 7))

    def test_tictactoe_positions_match_minimax(self):
        rng = random.Random(11)
        for _ in range(25):
            b = "." * 9
            for _ in range(rng.randint(3, 6)):
                kids = ttt_children(b)
                if not kids:
                    break
                b = rng.choice(kids)
            x_to_move = ttt_to_move(b) == "X"
            v = negamax(b, ttt_children, ttt_side_to_move_eval)

            def mm(s, xmax):
                kids = ttt_children(s)
                if not kids:
                    return ttt_x_eval(s)
                vals = [mm(c, not xmax) for c in kids]
                return max(vals) if xmax else min(vals)

            m = mm(b, x_to_move)
            self.assertEqual(v, m if x_to_move else -m)

    def test_fixed_side_evaluation_is_a_bug(self):
        # Pitfall: if the leaves hold values for X (not for the side to move),
        # negamax returns a wrong value. X to move wins at once with square 2.
        b = "XX.OO...."
        self.assertEqual(negamax(b, ttt_children, ttt_side_to_move_eval), 1)
        self.assertEqual(negamax(b, ttt_children, ttt_x_eval), -1)


if __name__ == "__main__":
    unittest.main()
