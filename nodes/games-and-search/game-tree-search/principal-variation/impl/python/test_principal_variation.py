# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-variation/. The authors are listed in prov/Z9NCM4.jsonl.

import random
import unittest
from fractions import Fraction

from principal_variation import INF, follow, pv_search


def tree_moves(t):
    return [] if not isinstance(t, list) else list(enumerate(t))


def tree_eval(t):
    return 0 if isinstance(t, list) else t


def negamax(pos, depth, moves, evaluate):
    kids = moves(pos)
    if depth == 0 or not kids:
        return evaluate(pos)
    return max(-negamax(c, depth - 1, moves, evaluate) for _, c in kids)


def random_tree(rng, depth, frac, irregular):
    if depth == 0 or (irregular and rng.random() < 0.2):
        v = rng.randint(-20, 20)
        return Fraction(v, rng.randint(1, 6)) if frac else v
    b = rng.randint(1, 4) if irregular else 3
    return [random_tree(rng, depth - 1, frac, irregular) for _ in range(b)]


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def to_move(b):
    return "X" if b.count("X") == b.count("O") else "O"


def ttt_moves(b):
    if winner(b) or "." not in b:
        return []
    p = to_move(b)
    return [(i, b[:i] + p + b[i + 1 :]) for i in range(9) if b[i] == "."]


def ttt_eval(b):
    w = winner(b)
    return 0 if w is None else (1 if w == to_move(b) else -1)


class TestPrincipalVariation(unittest.TestCase):
    def check_line(self, root, depth, moves, evaluate):
        value, line = pv_search(root, depth, -INF, INF, moves, evaluate)
        self.assertEqual(value, negamax(root, depth, moves, evaluate))
        leaf = follow(root, line, moves)  # raises if a move is illegal
        # The line ends at a terminal position or at the depth limit.
        self.assertTrue(len(line) == depth or not moves(leaf))
        # The leaf value, for the side to move at the root, is the root value.
        sign = 1 if len(line) % 2 == 0 else -1
        self.assertEqual(sign * evaluate(leaf), value)
        # Each position on the line has the root value, from its own side.
        pos = root
        for k, mv in enumerate(line):
            self.assertEqual(negamax(pos, depth - k, moves, evaluate), (1 if k % 2 == 0 else -1) * value)
            pos = dict(moves(pos))[mv]
        return value, line

    def test_random_trees(self):
        rng = random.Random(7)
        for trial in range(400):
            t = random_tree(rng, rng.randint(0, 6), trial % 2 == 1, trial % 3 != 0)
            self.check_line(t, 99, tree_moves, tree_eval)
            self.check_line(t, rng.randint(0, 3), tree_moves, tree_eval)

    def test_tictactoe(self):
        value, line = self.check_line("." * 9, 9, ttt_moves, ttt_eval)
        self.assertEqual(value, 0)
        self.assertEqual(len(line), 9)  # a draw fills the board
        rng = random.Random(5)
        for _ in range(40):
            b = "." * 9
            for _ in range(rng.randint(1, 6)):
                kids = ttt_moves(b)
                if not kids:
                    break
                b = rng.choice(kids)[1]
            self.check_line(b, 9, ttt_moves, ttt_eval)

    def test_example_of_the_page(self):
        # MAX view [[3, 17], [2, 12]] in negamax form: the leaves are at depth 2, MAX to move there.
        t = [[3, 17], [2, 12]]
        value, line = pv_search(t, 2, -INF, INF, tree_moves, tree_eval)
        self.assertEqual((value, line), (3, [0, 0]))

    def test_follow_rejects_illegal_moves(self):
        with self.assertRaises(ValueError):
            follow([[1, 2], [3]], [1, 1], tree_moves)


if __name__ == "__main__":
    unittest.main()
