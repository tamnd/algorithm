# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/futility-pruning/. The authors are listed in prov/9FWPSR.jsonl.

import random
import unittest

from futility_pruning import INF, MaterialGame, alphabeta, futility_search, small_margin_example


def negamax(g, n, depth):
    """Reference: plain negamax to a fixed depth, no pruning."""
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    return max(-negamax(g, c, depth - 1) for c in kids)


SAFE = {1: 2, 2: 4}  # the quiet swing of MaterialGame is 2


class TestFutility(unittest.TestCase):
    def test_small_margin_example(self):
        g = small_margin_example()
        self.assertEqual(alphabeta(g, "R", 1, -INF, INF), 5)
        self.assertEqual(futility_search(g, "R", 1, -INF, INF, {1: 1}), 3)
        self.assertEqual(futility_search(g, "R", 1, -INF, INF, {1: 5}), 5)

    def test_alphabeta_reference(self):
        for seed in range(500):
            g = MaterialGame(seed, b=3, height=5)
            self.assertEqual(alphabeta(g, (), 5, -INF, INF), negamax(g, (), 5))

    def test_safe_margins_keep_the_value(self):
        rng = random.Random(41)
        for seed in range(600):
            g = MaterialGame(1000 + seed, b=3, height=5)
            want = negamax(g, (), 5)
            self.assertEqual(futility_search(g, (), 5, -INF, INF, SAFE), want)
            a = rng.randint(-15, 15)
            b = a + rng.randint(1, 12)
            got = futility_search(g, (), 5, a, b, SAFE)
            if want <= a:
                self.assertTrue(want <= got <= a)
            elif want >= b:
                self.assertTrue(b <= got <= want)
            else:
                self.assertEqual(got, want)

    def test_measured_nodes_and_values(self):
        # The page states these numbers: 200 trees, seeds 30000 to 30199, b = 4,
        # height 6, search depth 6, capture probability 0.3, quiet swing 2.
        cases = [({}, 89977, 200), ({1: 2}, 71038, 200), ({1: 2, 2: 4}, 55380, 200),
                 ({1: 0}, 68352, 147), ({1: 1, 2: 2}, 49941, 169)]
        nodes = [[0] for _ in cases]
        same = [0] * len(cases)
        for seed in range(200):
            g = MaterialGame(30000 + seed, b=4, height=6)
            v = alphabeta(g, (), 6, -INF, INF)
            for i, (margins, _, _) in enumerate(cases):
                same[i] += futility_search(g, (), 6, -INF, INF, margins, nodes[i]) == v
        for i, (_, want_nodes, want_same) in enumerate(cases):
            self.assertEqual((nodes[i][0], same[i]), (want_nodes, want_same))


if __name__ == "__main__":
    unittest.main()
