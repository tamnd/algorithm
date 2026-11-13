# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aspiration-search/. The authors are listed in prov/K9327M.jsonl.

import math
import random
import unittest
from fractions import Fraction

from aspiration_search import INF, alpha_beta, aspiration, deepening_with_aspiration


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
        v = rng.randint(-30, 30)
        return Fraction(v, rng.randint(1, 6)) if frac else v
    b = rng.randint(1, 4) if irregular else 3
    return [random_tree(rng, depth - 1, frac, irregular) for _ in range(b)]


def fail_hard(t, alpha, beta):
    """Fail-hard alpha-beta (F2 of Knuth and Moore) on a nested-list tree in negamax form."""
    if not isinstance(t, list):
        return min(max(t, alpha), beta)
    m = alpha
    for c in t:
        m = max(m, -fail_hard(c, -beta, -m))
        if m >= beta:
            return beta
    return m


def incremental_game(seed, b, d):
    rng = random.Random(seed)
    w = [rng.randint(-5, 5) for _ in range(b)]

    def moves(pos):
        path, s = pos
        if len(path) == d:
            return []
        out = []
        for m in range(b):
            q = path + (m,)
            gain = w[m] + random.Random(f"{seed}:{q}").randint(-4, 4)
            out.append((m, (q, -(s + gain))))
        return out

    return moves, (lambda pos: pos[1])


class TestAspirationSearch(unittest.TestCase):
    def test_equals_negamax_for_any_guess_and_width(self):
        rng = random.Random(17)
        for trial in range(250):
            t = random_tree(rng, rng.randint(1, 5), trial % 2 == 1, trial % 3 != 0)
            want = negamax(t, 99, tree_moves, tree_eval)
            guesses = [want, want + 1, want - Fraction(1, 7), Fraction(rng.randint(-60, 60), rng.randint(1, 5)), 1000, -1000]
            for g in guesses:
                for delta in (Fraction(1, 100), 1, 5, 100):
                    log = []
                    self.assertEqual(aspiration(t, 99, g, delta, tree_moves, tree_eval, log), want)
                    self.assertTrue(all(a < b for a, b, _ in log))
                    # Searches: the first, the doublings that the distance needs, and up to two more.
                    dist = abs(g - want)
                    bound = 3 + (math.ceil(math.log2(dist / delta)) if dist > delta else 0)
                    self.assertLessEqual(len(log), bound)

    def test_value_on_the_edge_of_the_window(self):
        t = [[3, 17], [2, 12]]  # negamax value 3
        log = []
        self.assertEqual(aspiration(t, 9, 5, 2, tree_moves, tree_eval, log), 3)  # first window (3, 7)
        self.assertEqual([(a, b) for a, b, _ in log], [(3, 7), (-1, 3)])
        self.assertEqual(log[1][2], 3)  # the second search fails high at 3 = lo = hi

    def test_fail_hard_research_below_alpha_fails_high(self):
        # Knuth and Moore, Section 4, suggest the re-search F2(p, -inf, v) after a fail low at v.
        # With fail-hard F2 it returns its beta = v when the value is v: a fail high. Only the
        # bound from the first search shows that the value is v.
        t = [[3, 17], [2, 12]]
        self.assertEqual(fail_hard(t, 3, 7), 3)
        self.assertEqual(fail_hard(t, -INF, 3), 3)  # = beta: a fail high, though the value is 3

    def test_deepening_on_an_incremental_game(self):
        for seed in range(6):
            moves, ev = incremental_game(seed, 3, 6)
            root = ((), 0)
            vals = deepening_with_aspiration(root, 6, 2, moves, ev)
            self.assertEqual(vals, [negamax(root, d, moves, ev) for d in range(1, 7)])

    def test_random_windows_of_alpha_beta(self):
        rng = random.Random(9)
        for trial in range(300):
            t = random_tree(rng, rng.randint(1, 5), trial % 2 == 0, True)
            want = negamax(t, 99, tree_moves, tree_eval)
            a = Fraction(rng.randint(-40, 40), rng.randint(1, 3))
            b = a + Fraction(rng.randint(1, 30), rng.randint(1, 3))
            r = alpha_beta(t, 99, a, b, tree_moves, tree_eval)
            if r <= a:
                self.assertLessEqual(want, r)
            elif r >= b:
                self.assertGreaterEqual(want, r)
            else:
                self.assertEqual(r, want)


if __name__ == "__main__":
    unittest.main()
