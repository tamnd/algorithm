# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-variation-search/. The authors are listed in prov/HEBCKY.jsonl.

import random
import unittest
from fractions import Fraction

from principal_variation_search import INF, pvs

GRAIN = Fraction(1, 60)  # every leaf p/q with 1 <= q <= 6 is a multiple of 1/60


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


def alpha_beta(pos, depth, alpha, beta, moves, evaluate):
    kids = moves(pos)
    if depth == 0 or not kids:
        return evaluate(pos)
    m = -INF
    for _, c in kids:
        m = max(m, -alpha_beta(c, depth - 1, -beta, -max(m, alpha), moves, evaluate))
        if m >= beta:
            break
    return m


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
    if not isinstance(t, list):
        return t
    kids = [best_first(c) for c in t]
    kids.sort(key=lambda c: negamax(c, 99, tree_moves, tree_eval))
    return kids


def leaves_of(search, t, *args):
    seen = []

    def ev(p):
        seen.append(p[0])
        return p[1]

    v = search(((), t), 99, -INF, INF, path_moves, ev, *args)
    return v, seen


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


class TestPrincipalVariationSearch(unittest.TestCase):
    def test_equals_negamax_on_random_trees(self):
        rng = random.Random(11)
        for trial in range(500):
            frac = trial % 2 == 1
            t = random_tree(rng, rng.randint(0, 6), frac, trial % 3 != 0)
            g = GRAIN if frac else 1
            for d in (99, rng.randint(0, 3)):
                want = negamax(t, d, tree_moves, tree_eval)
                self.assertEqual(pvs(t, d, -INF, INF, tree_moves, tree_eval, g), want)

    def test_any_grain_is_correct(self):
        # A grain that is too coarse costs work but not correctness.
        rng = random.Random(12)
        for trial in range(300):
            t = random_tree(rng, rng.randint(1, 5), True, True)
            want = negamax(t, 99, tree_moves, tree_eval)
            for g in (1, 7, Fraction(1, 1000)):
                self.assertEqual(pvs(t, 99, -INF, INF, tree_moves, tree_eval, g), want)

    def test_bounds_for_random_windows(self):
        rng = random.Random(13)
        for trial in range(400):
            t = random_tree(rng, rng.randint(1, 5), trial % 2 == 0, True)
            want = negamax(t, 99, tree_moves, tree_eval)
            a = Fraction(rng.randint(-40, 40), rng.randint(1, 3))
            b = a + Fraction(rng.randint(1, 30), rng.randint(1, 3))
            r = pvs(t, 99, a, b, tree_moves, tree_eval, GRAIN)
            if r <= a:
                self.assertLessEqual(want, r)
            elif r >= b:
                self.assertGreaterEqual(want, r)
            else:
                self.assertEqual(r, want)

    def test_best_first_order_matches_alpha_beta(self):
        rng = random.Random(14)
        for b, d in [(2, 3), (2, 4), (3, 3), (3, 4), (2, 6), (3, 5)]:
            for _ in range(4):
                t = best_first(uniform_tree(rng, b, d))
                stats = [0, 0]
                v, seen = leaves_of(pvs, t, 1, stats)
                v2, seen2 = leaves_of(alpha_beta, t)
                self.assertEqual(v, v2)
                self.assertEqual(stats[1], 0)  # no re-search when the first move is best
                self.assertEqual(seen, seen2)  # the same leaves, in the same order
                self.assertEqual(len(seen), b ** ((d + 1) // 2) + b ** (d // 2) - 1)

    def test_example_of_the_page(self):
        # MAX view: B = (D, E), C = (G, F); D = (3, 17), E = (19, 12), G = (2, 5), F = (15, 25).
        t = [[[-3, -17], [-19, -12]], [[-2, -5], [-15, -25]]]
        stats = [0, 0]
        order = []
        v = pvs(t, 99, -INF, INF, tree_moves, lambda x: (order.append(x), tree_eval(x))[1], 1, stats)
        self.assertEqual(v, 17)
        self.assertEqual(order, [-3, -17, -19, -2, -5])
        # Swap D and E: the null-window test of D fails high, and D is searched again.
        t2 = [[[-19, -12], [-3, -17]], [[-2, -5], [-15, -25]]]
        stats2 = [0, 0]
        order2 = []
        v2 = pvs(t2, 99, -INF, INF, tree_moves, lambda x: (order2.append(x), tree_eval(x))[1], 1, stats2)
        self.assertEqual(v2, 17)
        self.assertEqual(stats2[1], 1)
        self.assertEqual(order2, [-19, -12, -3, -17, -3, -17, -2, -5])

    def test_tictactoe(self):
        self.assertEqual(pvs("." * 9, 9, -INF, INF, ttt_moves, ttt_eval), 0)
        rng = random.Random(15)
        for _ in range(30):
            b = "." * 9
            for _ in range(rng.randint(1, 5)):
                kids = ttt_moves(b)
                if not kids:
                    break
                b = rng.choice(kids)[1]
            self.assertEqual(pvs(b, 9, -INF, INF, ttt_moves, ttt_eval), negamax(b, 9, ttt_moves, ttt_eval))


if __name__ == "__main__":
    unittest.main()
