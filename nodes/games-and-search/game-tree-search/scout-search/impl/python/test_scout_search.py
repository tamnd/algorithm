# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scout-search/. The authors are listed in prov/X5X0T8.jsonl.

import math
import random
import unittest
from fractions import Fraction

from scout_search import scout, scout_test

INF = math.inf


def tree_moves(t):
    return [] if not isinstance(t, list) else list(enumerate(t))


def tree_eval(t):
    return 0 if isinstance(t, list) else t


def path_moves(p):
    path, t = p
    return [] if not isinstance(t, list) else [(i, (path + (i,), c)) for i, c in enumerate(t)]


def negamax(pos, depth, moves, evaluate):
    kids = moves(pos)
    if depth == 0 or not kids:
        return evaluate(pos)
    return max(-negamax(c, depth - 1, moves, evaluate) for _, c in kids)


def alpha_beta_leaves(p, alpha, beta, seen):
    """Fail-soft alpha-beta on a (path, tree) position; appends the path of each evaluated leaf."""
    path, t = p
    if not isinstance(t, list):
        seen.append(path)
        return t
    m = -INF
    for _, c in path_moves(p):
        m = max(m, -alpha_beta_leaves(c, -beta, -max(m, alpha), seen))
        if m >= beta:
            break
    return m


def scout_leaves(t):
    seen = []

    def ev(p):
        seen.append(p[0])
        return p[1]

    return scout(((), t), 99, path_moves, ev), seen


def random_tree(rng, depth, frac, irregular):
    if depth == 0 or (irregular and rng.random() < 0.2):
        v = rng.randint(-20, 20)
        return Fraction(v, rng.randint(1, 6)) if frac else v
    b = rng.randint(1, 4) if irregular else 3
    return [random_tree(rng, depth - 1, frac, irregular) for _ in range(b)]


def uniform_tree(rng, b, d):
    if d == 0:
        return rng.randint(-20, 20)
    return [uniform_tree(rng, b, d - 1) for _ in range(b)]


def best_first(t):
    """The same tree with the children of every node sorted best first for the side to move."""
    if not isinstance(t, list):
        return t
    kids = [best_first(c) for c in t]
    kids.sort(key=lambda c: negamax(c, 99, tree_moves, tree_eval))
    return kids


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def ttt_moves(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return []
    p = "X" if b.count("X") == b.count("O") else "O"
    return [(i, b[:i] + p + b[i + 1 :]) for i in range(9) if b[i] == "."]


def ttt_eval(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return -1  # the side to move has lost
    return 0


class TestScout(unittest.TestCase):
    def test_equals_negamax_on_random_trees(self):
        rng = random.Random(3)
        for trial in range(500):
            t = random_tree(rng, rng.randint(0, 6), trial % 2 == 1, trial % 3 != 0)
            self.assertEqual(scout(t, 99, tree_moves, tree_eval), negamax(t, 99, tree_moves, tree_eval))
            d = rng.randint(0, 3)
            self.assertEqual(scout(t, d, tree_moves, tree_eval), negamax(t, d, tree_moves, tree_eval))

    def test_the_test_procedure(self):
        rng = random.Random(4)
        for trial in range(400):
            t = random_tree(rng, rng.randint(0, 5), trial % 2 == 0, True)
            n = negamax(t, 99, tree_moves, tree_eval)
            for v in (n, n - Fraction(1, 7), n + Fraction(1, 7), Fraction(rng.randint(-25, 25), rng.randint(1, 4))):
                self.assertEqual(scout_test(t, 99, v, True, tree_moves, tree_eval), n > v)
                self.assertEqual(scout_test(t, 99, v, False, tree_moves, tree_eval), n >= v)

    def test_example_of_the_page(self):
        # MAX view: D = (3, 17), E = (19, 12), G = (2, 5), F = (15, 25); the leaves are at depth 3.
        t = [[[-3, -17], [-19, -12]], [[-2, -5], [-15, -25]]]
        order = []
        v = scout(t, 99, tree_moves, lambda x: (order.append(x), tree_eval(x))[1])
        self.assertEqual(v, 17)
        self.assertEqual(order, [-3, -17, -17, -19, -2, -5])  # 17 is tested, then searched

    def test_best_first_order_gives_the_minimal_tree(self):
        rng = random.Random(5)
        for b, d in [(2, 3), (2, 4), (3, 3), (3, 4), (2, 6), (3, 5)]:
            for _ in range(4):
                t = best_first(uniform_tree(rng, b, d))
                v, seen = scout_leaves(t)
                self.assertEqual(v, negamax(t, 99, tree_moves, tree_eval))
                minimal = b ** ((d + 1) // 2) + b ** (d // 2) - 1
                self.assertEqual(len(seen), minimal)  # no leaf twice, and no more than the bound
                ab = []
                alpha_beta_leaves(((), t), -INF, INF, ab)
                self.assertEqual(sorted(ab), sorted(seen))

    def test_scout_and_alpha_beta_are_incomparable(self):
        # Binary trees of depth 4 found by a random search.
        t1 = [[[[-5, 5], [3, -4]], [[6, 5], [7, 9]]], [[[-8, 9], [-3, 9]], [[5, 6], [3, 0]]]]
        t2 = [[[[1, -9], [-4, 1]], [[-2, 1], [-1, -1]]], [[[0, 6], [4, -9]], [[0, -4], [0, -8]]]]
        for t, sc_only, ab_only in [(t1, {(1, 0, 0, 1)}, set()), (t2, set(), {(1, 0, 1, 0), (1, 0, 1, 1)})]:
            v, sc = scout_leaves(t)
            ab = []
            self.assertEqual(alpha_beta_leaves(((), t), -INF, INF, ab), v)
            self.assertEqual(set(sc) - set(ab), sc_only)
            self.assertEqual(set(ab) - set(sc), ab_only)

    def test_tictactoe(self):
        self.assertEqual(scout("." * 9, 9, ttt_moves, ttt_eval), 0)
        rng = random.Random(6)
        for _ in range(30):
            b = "." * 9
            for _ in range(rng.randint(1, 5)):
                kids = ttt_moves(b)
                if not kids:
                    break
                b = rng.choice(kids)[1]
            self.assertEqual(scout(b, 9, ttt_moves, ttt_eval), negamax(b, 9, ttt_moves, ttt_eval))


if __name__ == "__main__":
    unittest.main()
