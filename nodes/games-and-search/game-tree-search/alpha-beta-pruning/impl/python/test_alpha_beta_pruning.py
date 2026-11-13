# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpha-beta-pruning/. The authors are listed in prov/AYQW86.jsonl.

import math
import random
import unittest
from fractions import Fraction

from alpha_beta_pruning import alpha_beta, alpha_beta_tree, minimax_leaves_to_negamax

INF = math.inf
PAGE_TREE = [[[3, 17], [19, 12]], [[2, 5], [15, 25]]]  # leaves are values for MAX


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


def random_tree(rng, depth, leaf, root=True):
    if depth == 0 or (not root and rng.random() < 0.3):
        return leaf(rng)
    return [random_tree(rng, depth - 1, leaf, False) for _ in range(rng.randint(1, 4))]


def int_leaf(rng):
    return rng.randint(-20, 20)


def frac_leaf(rng):
    return Fraction(rng.randint(-60, 60), rng.randint(1, 6))


def random_trees(seed, count):
    """Uniform and irregular trees with int and Fraction leaves, as negamax trees."""
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        leaf = int_leaf if rng.random() < 0.5 else frac_leaf
        if rng.random() < 0.5:
            b, d = rng.randint(2, 4), rng.randint(1, 5)
            tree = build_uniform([leaf(rng) for _ in range(b**d)], b, d)
        else:
            tree = random_tree(rng, rng.randint(0, 6), leaf)
        out.append((tree, rng))
    return out


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


def ttt_eval(b):
    w = ttt_winner(b)
    return 0 if w is None else (1 if w == ttt_to_move(b) else -1)


def negamax_ref(s):
    kids = ttt_children(s)
    if not kids:
        return ttt_eval(s)
    return max(-negamax_ref(c) for c in kids)


class TestAlphaBeta(unittest.TestCase):
    def test_page_example(self):
        t = minimax_leaves_to_negamax(PAGE_TREE)
        for fs in (True, False):
            seen = []
            self.assertEqual(alpha_beta_tree(t, fail_soft=fs, visited=seen), 17)
            # Leaves 3, 17, 19, 2, 5 are evaluated; 12, 15 and 25 are cut off.
            self.assertEqual(seen, [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 0, 1)])
        # C is the MIN node at path (1,). With the window (17, inf) for MAX it
        # returns 5 for MAX in the fail-soft form and the bound 17 in the fail-hard form.
        c = t[1]
        self.assertEqual(-alpha_beta_tree(c, -INF, -17, True), 5)
        self.assertEqual(-alpha_beta_tree(c, -INF, -17, False), 17)

    def test_root_value_equals_minimax(self):
        for tree, _ in random_trees(2024, 1500):
            for max_root in (True, False):
                v = minimax_ref(tree, max_root)
                nt = minimax_leaves_to_negamax(tree, max_root)
                want = v if max_root else -v
                for fs in (True, False):
                    self.assertEqual(alpha_beta_tree(nt, fail_soft=fs), want)

    def test_window_bounds_fail_hard_and_fail_soft(self):
        for tree, rng in random_trees(77, 800):
            v = minimax_ref(tree, True)
            nt = minimax_leaves_to_negamax(tree, True)
            for _ in range(6):
                a = Fraction(rng.randint(-25, 25), rng.randint(1, 3))
                b = a + Fraction(rng.randint(1, 30), rng.randint(1, 3))
                if rng.random() < 0.2:
                    a = -INF
                if rng.random() < 0.2:
                    b = INF
                hard = alpha_beta_tree(nt, a, b, fail_soft=False)
                soft = alpha_beta_tree(nt, a, b, fail_soft=True)
                for r in (hard, soft):
                    # Knuth and Moore: the three cases match.
                    self.assertEqual(v <= a, r <= a)
                    self.assertEqual(v >= b, r >= b)
                    if a < v < b:
                        self.assertEqual(r, v)
                # Fail-soft: the returned value is itself a bound.
                if soft <= a:
                    self.assertLessEqual(v, soft)
                if soft >= b:
                    self.assertGreaterEqual(v, soft)
                # The fail-soft bound is never weaker than the fail-hard one.
                if hard <= a:
                    self.assertLessEqual(soft, hard)
                if hard >= b:
                    self.assertGreaterEqual(soft, hard)

    def test_both_forms_visit_the_same_leaves(self):
        for tree, rng in random_trees(5, 400):
            nt = minimax_leaves_to_negamax(tree)
            a = rng.randint(-15, 5)
            b = a + rng.randint(1, 15)
            s1, s2 = [], []
            alpha_beta_tree(nt, a, b, True, s1)
            alpha_beta_tree(nt, a, b, False, s2)
            self.assertEqual(s1, s2)

    def test_never_more_leaves_than_minimax(self):
        rng = random.Random(9)
        for b in range(2, 5):
            for d in range(1, 6):
                for _ in range(10):
                    nt = build_uniform([rng.randint(-9, 9) for _ in range(b**d)], b, d)
                    seen = []
                    alpha_beta_tree(nt, visited=seen)
                    self.assertLessEqual(len(seen), b**d)
                    self.assertEqual(len(seen), len(set(seen)))

    def test_tictactoe(self):
        rng = random.Random(3)
        for _ in range(12):
            b = "." * 9
            for _ in range(rng.randint(2, 6)):
                kids = ttt_children(b)
                if not kids:
                    break
                b = rng.choice(kids)
            want = negamax_ref(b)
            for fs in (True, False):
                count = [0]
                self.assertEqual(alpha_beta(b, ttt_children, ttt_eval, fail_soft=fs, leaf_count=count), want)
        # From the empty board, in square order 0 to 8: the value is a draw, and
        # alpha-beta evaluates 7330 of the 255168 terminal positions that minimax visits.
        count = [0]
        self.assertEqual(alpha_beta("." * 9, ttt_children, ttt_eval, leaf_count=count), 0)
        self.assertEqual(count[0], 7330)

        def all_leaves(s):
            kids = ttt_children(s)
            return 1 if not kids else sum(all_leaves(c) for c in kids)

        self.assertEqual(all_leaves("." * 9), 255168)


if __name__ == "__main__":
    unittest.main()
