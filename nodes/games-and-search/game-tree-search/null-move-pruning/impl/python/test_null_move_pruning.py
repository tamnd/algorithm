# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/null-move-pruning/. The authors are listed in prov/Q2C8WC.jsonl.

import random
import unittest

from null_move_pruning import INF, RandomGame, alphabeta, null_move_search, verified_search, zugzwang_example


def negamax(g, n, depth):
    """Reference: plain negamax to a fixed depth, no pruning."""
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    return max(-negamax(g, c, depth - 1) for c in kids)


class TestNullMove(unittest.TestCase):
    def test_zugzwang_example(self):
        g = zugzwang_example()
        self.assertEqual(negamax(g, "R", 4), 5)
        self.assertEqual(alphabeta(g, "R", 4, -INF, INF), 5)
        # The null move lets Black "pass" out of the zugzwang, so the line is cut off.
        self.assertEqual(null_move_search(g, "R", 4, -INF, INF, r=2), 1)
        # Verification sees that the reduced search does not fail high, and searches again.
        self.assertEqual(verified_search(g, "R", 4, -INF, INF, r=2), 5)

    def test_alphabeta_reference(self):
        for seed in range(500):
            g = RandomGame(seed, b=3, height=5)
            self.assertEqual(alphabeta(g, (), 5, -INF, INF), negamax(g, (), 5))

    def test_no_null_when_depth_too_small(self):
        # With r + 1 larger than the depth, the null move is never tried.
        for seed in range(500):
            g = RandomGame(700 + seed, b=3, height=4)
            self.assertEqual(null_move_search(g, (), 4, -INF, INF, r=4), alphabeta(g, (), 4, -INF, INF))

    def test_measured_nodes_and_values(self):
        # The page states these numbers: 200 trees, seeds 10000 to 10199,
        # b = 4, height 7, search depth 7, swing 4.
        plain_nodes, nmp_nodes, ver_nodes = [0], [0], [0]
        same_nmp = same_ver = 0
        for seed in range(200):
            g = RandomGame(10000 + seed, b=4, height=7)
            v = alphabeta(g, (), 7, -INF, INF, plain_nodes)
            same_nmp += null_move_search(g, (), 7, -INF, INF, 2, True, nmp_nodes) == v
            same_ver += verified_search(g, (), 7, -INF, INF, 3, True, True, ver_nodes) == v
        self.assertEqual((plain_nodes[0], nmp_nodes[0], ver_nodes[0]), (163755, 70499, 101630))
        self.assertEqual((same_nmp, same_ver), (173, 136))

if __name__ == "__main__":
    unittest.main()
