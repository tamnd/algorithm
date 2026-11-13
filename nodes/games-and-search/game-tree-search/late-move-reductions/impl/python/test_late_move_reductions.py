# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/late-move-reductions/. The authors are listed in prov/EJ7NFT.jsonl.

import unittest

from late_move_reductions import INF, MaterialGame, alphabeta, late_threat_example, lmr_search


def negamax(g, n, depth):
    """Reference: plain negamax to a fixed depth, no pruning."""
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    return max(-negamax(g, c, depth - 1) for c in kids)


class TestLateMoveReductions(unittest.TestCase):
    def test_late_threat_example(self):
        g = late_threat_example()
        self.assertEqual(negamax(g, "R", 2), 4)
        self.assertEqual(alphabeta(g, "R", 2, -INF, INF), 4)
        # The reduced search of m1 sees only the static score 0, fails low, and is not repeated.
        self.assertEqual(lmr_search(g, "R", 2, -INF, INF, full=1, r=1), 1)
        # With two full-depth moves, nothing is reduced.
        self.assertEqual(lmr_search(g, "R", 2, -INF, INF, full=2, r=1), 4)

    def test_alphabeta_reference(self):
        for seed in range(500):
            g = MaterialGame(seed, b=3, height=5)
            self.assertEqual(alphabeta(g, (), 5, -INF, INF), negamax(g, (), 5))

    def test_no_reduction_is_alphabeta(self):
        # With full >= b, no move is late, and LMR is plain alpha-beta, node for node.
        for seed in range(500):
            g = MaterialGame(2000 + seed, b=3, height=5)
            c1, c2 = [0], [0]
            self.assertEqual(lmr_search(g, (), 5, -INF, INF, 3, 1, c1), alphabeta(g, (), 5, -INF, INF, c2))
            self.assertEqual(c1, c2)

    def test_measured_nodes_and_values(self):
        # The page states these numbers: 200 trees, seeds 40000 to 40199, b = 4,
        # height 7, search depth 7, capture probability 0.3, quiet swing 2.
        cases = [((1, 1), 91300, 82), ((2, 1), 102556, 116), ((1, 2), 57430, 126), ((3, 1), 139334, 171)]
        plain = [0]
        nodes = [[0] for _ in cases]
        same = [0] * len(cases)
        for seed in range(200):
            g = MaterialGame(40000 + seed, b=4, height=7)
            v = alphabeta(g, (), 7, -INF, INF, plain)
            for i, ((full, r), _, _) in enumerate(cases):
                same[i] += lmr_search(g, (), 7, -INF, INF, full, r, nodes[i]) == v
        self.assertEqual(plain[0], 197970)
        for i, (_, want_nodes, want_same) in enumerate(cases):
            self.assertEqual((nodes[i][0], same[i]), (want_nodes, want_same))


if __name__ == "__main__":
    unittest.main()
