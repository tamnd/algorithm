# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mtdf/. The authors are listed in prov/C2MWH2.jsonl.

import random
import unittest
from fractions import Fraction

from mtdf import INF, alpha_beta_with_memory, mtdf

GRAIN = Fraction(1, 60)  # every leaf p/q with 1 <= q <= 6 is a multiple of 1/60


def path_moves(p):
    path, t = p
    return [] if not isinstance(t, list) else [(i, (path + (i,), c)) for i, c in enumerate(t)]


def path_eval(p):
    return 0 if isinstance(p[1], list) else p[1]


def path_key(p):
    return p[0]


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


def ttt_eval_scaled(b):
    # A win scores more when it comes sooner: 10 + the number of empty squares.
    return -(10 + b.count(".")) if ttt_eval(b) else 0


class TestMTDf(unittest.TestCase):
    def test_equals_negamax_on_random_trees(self):
        rng = random.Random(21)
        for trial in range(400):
            frac = trial % 2 == 1
            t = random_tree(rng, rng.randint(0, 6), frac, trial % 3 != 0)
            root = ((), t)
            g = GRAIN if frac else 1
            for d in (99, rng.randint(0, 3)):
                want = negamax(root, d, path_moves, path_eval)
                for f in (want, want + 3, want - Fraction(5, 7), 0, 50, -50):
                    log = []
                    self.assertEqual(mtdf(root, d, f, path_moves, path_eval, path_key, g, log=log), want)
                    if f == want:
                        self.assertEqual(len(log), 2)  # one pass fails high, one fails low

    def test_any_grain_is_correct(self):
        rng = random.Random(22)
        for trial in range(200):
            t = random_tree(rng, rng.randint(1, 5), True, True)
            root = ((), t)
            want = negamax(root, 99, path_moves, path_eval)
            for g in (1, 5, Fraction(1, 1000)):
                self.assertEqual(mtdf(root, 99, 0, path_moves, path_eval, path_key, g), want)

    def test_memory_bounds_for_random_windows_with_a_shared_table(self):
        rng = random.Random(23)
        for trial in range(60):
            t = random_tree(rng, rng.randint(1, 5), trial % 2 == 0, True)
            root = ((), t)
            want = negamax(root, 99, path_moves, path_eval)
            table = {}
            for _ in range(15):
                a = Fraction(rng.randint(-40, 40), rng.randint(1, 3))
                b = a + Fraction(rng.randint(1, 30), rng.randint(1, 3))
                r = alpha_beta_with_memory(root, 99, a, b, path_moves, path_eval, path_key, table)
                if r <= a:
                    self.assertLessEqual(want, r)
                elif r >= b:
                    self.assertGreaterEqual(want, r)
                else:
                    self.assertEqual(r, want)
            # Every stored bound is a true bound.
            for (path, depth), (lo, hi) in table.items():
                sub = t
                for i in path:
                    sub = sub[i]
                v = negamax((path, sub), depth, path_moves, path_eval)
                self.assertTrue(lo <= v <= hi)

    def test_example_of_the_page(self):
        # MAX view: D = (3, 17), E = (19, 12), G = (2, 5), F = (15, 25); the leaves are at depth 3.
        t = [[[-3, -17], [-19, -12]], [[-2, -5], [-15, -25]]]
        log, seen = [], []
        ev = lambda p: (seen.append(p[1]), path_eval(p))[1]  # noqa: E731
        self.assertEqual(mtdf(((), t), 99, 0, path_moves, ev, path_key, 1, log=log), 17)
        self.assertEqual(log, [(0, 3), (4, 17), (18, 17)])  # fail high, fail high, fail low
        self.assertEqual(seen, [-3, -19, -17, -2, -5])  # the table keeps each leaf: no leaf twice
        log = []
        self.assertEqual(mtdf(((), t), 99, 17, path_moves, path_eval, path_key, 1, log=log), 17)
        self.assertEqual(log, [(17, 17), (18, 17)])

    def test_tictactoe_with_transpositions(self):
        # The board is the key, so the table merges transpositions.
        for ev in (ttt_eval, ttt_eval_scaled):
            want = negamax("." * 9, 9, ttt_moves, ev)
            self.assertEqual(mtdf("." * 9, 9, 0, ttt_moves, ev, lambda b: b), want)
        rng = random.Random(24)
        for _ in range(20):
            b = "." * 9
            for _ in range(rng.randint(1, 5)):
                kids = ttt_moves(b)
                if not kids:
                    break
                b = rng.choice(kids)[1]
            want = negamax(b, 9, ttt_moves, ttt_eval_scaled)
            self.assertEqual(mtdf(b, 9, rng.randint(-20, 20), ttt_moves, ttt_eval_scaled, lambda x: x), want)

    def test_iterative_deepening_with_one_table(self):
        # One table for all depths: entries are keyed by (position, depth).
        rng = random.Random(25)
        for _ in range(20):
            t = random_tree(rng, 6, False, True)
            root = ((), t)
            table = {}
            f = 0
            for d in range(1, 7):
                f = mtdf(root, d, f, path_moves, path_eval, path_key, 1, table)
                self.assertEqual(f, negamax(root, d, path_moves, path_eval))


if __name__ == "__main__":
    unittest.main()
