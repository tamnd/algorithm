# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sss-star/. The authors are listed in prov/QXZG5Q.jsonl.

import random
import unittest
from fractions import Fraction

from sss_star import INF, sss_star


def path_moves(p):
    path, t = p
    return [] if not isinstance(t, list) else [(i, (path + (i,), c)) for i, c in enumerate(t)]


def path_eval(p):
    return 0 if isinstance(p[1], list) else p[1]


def negamax(pos, depth, moves, evaluate):
    kids = moves(pos)
    if depth == 0 or not kids:
        return evaluate(pos)
    return max(-negamax(c, depth - 1, moves, evaluate) for _, c in kids)


def alpha_beta(pos, depth, a, b, seen):
    """Fail-soft negamax alpha-beta, left to right, with a cutoff at g >= b."""
    kids = path_moves(pos)
    if depth == 0 or not kids:
        seen.append(pos[0])
        return path_eval(pos)
    g = -INF
    for _, c in kids:
        g = max(g, -alpha_beta(c, depth - 1, -b, -max(g, a), seen))
        if g >= b:
            break
    return g


def mt_sss(pos, top):
    """MTD with the first guess above every value: null-window searches with memory."""
    table, seen = {}, []

    def abwm(p, a, b):
        lo, hi = table.get(p[0], (-INF, INF))
        if lo >= b or lo == hi:
            return lo
        if hi <= a:
            return hi
        a, b = max(a, lo), min(b, hi)
        kids = path_moves(p)
        if not kids:
            seen.append(p[0])
            g = path_eval(p)
            table[p[0]] = (g, g)
            return g
        g, x = -INF, a
        for _, c in kids:
            if g >= b:
                break
            g = max(g, -abwm(c, -b, -x))
            x = max(x, g)
        table[p[0]] = (lo, g) if g <= a else (g, g) if g < b else (g, hi)
        return g

    g, lower, upper = top, -INF, INF
    while lower < upper:
        beta = max(g, lower + 1)
        g = abwm(pos, beta - 1, beta)
        if g < beta:
            upper = g
        else:
            lower = g
    return g, seen


def random_tree(rng, depth, irregular, frac=False, spread=20):
    if depth == 0 or (irregular and rng.random() < 0.2):
        v = rng.randint(-spread, spread)
        return Fraction(v, rng.randint(1, 6)) if frac else v
    b = rng.randint(1, 4) if irregular else 3
    return [random_tree(rng, depth - 1, irregular, frac, spread) for _ in range(b)]


def uniform_tree(rng, b, d):
    if d == 0:
        return rng.randint(-1000, 1000)
    return [uniform_tree(rng, b, d - 1) for _ in range(b)]


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
            return -(10 + b.count("."))  # the side to move has lost; sooner is worse
    return 0


class TestSSSStar(unittest.TestCase):
    def test_equals_negamax_on_random_trees(self):
        rng = random.Random(31)
        for trial in range(600):
            t = random_tree(rng, rng.randint(0, 6), trial % 3 != 0, trial % 2 == 1)
            root = ((), t)
            for d in (99, rng.randint(0, 3)):
                want = negamax(root, d, path_moves, path_eval)
                seen = []
                self.assertEqual(sss_star(root, d, path_moves, path_eval, seen), want)
                self.assertEqual(len(seen), len(set(seen)))  # no leaf twice

    def test_never_a_leaf_that_alpha_beta_skips(self):
        # Small spreads give many ties; ties in OPEN go to the leftmost state.
        rng = random.Random(32)
        fewer = 0
        for trial in range(1500):
            spread = (2, 5, 20)[trial % 3]
            t = random_tree(rng, rng.randint(1, 6), trial % 2 == 0, trial % 5 == 0, spread)
            root = ((), t)
            s, a = [], []
            v = sss_star(root, 99, path_moves, path_eval, s)
            self.assertEqual(v, alpha_beta(root, 99, -INF, INF, a))
            self.assertLessEqual(set(s), set(a))
            fewer += len(s) < len(a)
        self.assertGreater(fewer, 100)  # and often strictly fewer

    def test_example_of_the_page(self):
        # MAX view: D = (19, 8), E = (23, 11), G = (25, 22), F = (30, 26).
        t = [[[-19, -8], [-23, -11]], [[-25, -22], [-30, -26]]]
        s, a, stats = [], [], {}
        self.assertEqual(sss_star(((), t), 99, path_moves, path_eval, s, stats), 25)
        self.assertEqual(s, [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0)])  # 19, 8, 25, 22, 30
        self.assertEqual(alpha_beta(((), t), 99, -INF, INF, a), 25)
        self.assertEqual(a, [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 0, 1), (1, 1, 0)])  # also 23
        self.assertEqual(stats["open"], 4)

    def test_same_leaves_in_the_same_order_as_mtd_from_the_top(self):
        rng = random.Random(33)
        for trial in range(800):
            spread = (3, 20)[trial % 2]
            t = random_tree(rng, rng.randint(0, 6), trial % 3 != 0, False, spread)
            s = []
            v = sss_star(((), t), 99, path_moves, path_eval, s)
            g, m = mt_sss(((), t), spread + 1)
            self.assertEqual((g, m), (v, s))

    def test_open_holds_at_most_one_max_solution_tree(self):
        # On a uniform tree, OPEN never holds more than b^ceil(d/2) states.
        rng = random.Random(34)
        for b, d in ((2, 7), (3, 5), (4, 4), (5, 3)):
            for _ in range(15):
                stats = {}
                sss_star(((), uniform_tree(rng, b, d)), 99, path_moves, path_eval, stats=stats)
                self.assertLessEqual(stats["open"], b ** ((d + 1) // 2))

    def test_tictactoe(self):
        for start in (".........", "X........", "....X....", "X...O...."):
            want = negamax(start, 9, ttt_moves, ttt_eval)
            self.assertEqual(sss_star(start, 9, ttt_moves, ttt_eval), want)
        self.assertEqual(sss_star("." * 9, 3, ttt_moves, ttt_eval), negamax("." * 9, 3, ttt_moves, ttt_eval))


if __name__ == "__main__":
    unittest.main()
