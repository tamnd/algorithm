# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/young-brothers-wait/. The authors are listed in prov/QFBJRN.jsonl.

import random
import unittest

from young_brothers_wait import (INF, PerfectOrder, RandomGame, alphabeta, critical_nodes, negamax,
                                 simulate)


class TestYoungBrothersWait(unittest.TestCase):
    def test_same_root_value_with_and_without_the_rule(self):
        rng = random.Random(71)
        for seed in range(300):
            b, h = rng.randint(2, 4), rng.randint(1, 5)
            g = RandomGame(2000 + seed, b=b, height=h)
            want = negamax(g, (), h)
            self.assertEqual(alphabeta(g, (), h, -INF, INF), want)
            for p in (1, 2, 4, 8):
                for wait in (True, False):
                    self.assertEqual(simulate(g, (), h, p, wait, rng.randint(1, 3))[0], want)

    def test_perfect_order_has_no_overhead(self):
        # With the best move first everywhere, the rule visits exactly the
        # minimal tree of Knuth and Moore for every P. Without it, it does not.
        for b, h, n in ((2, 4, 30), (3, 5, 30), (4, 6, 30)):
            for seed in range(n):
                g = PerfectOrder(RandomGame(70000 + seed, b, h), h)
                c = [0]
                v = alphabeta(g, (), h, -INF, INF, c)
                self.assertEqual(c[0], critical_nodes(b, h))
                for p in (1, 2, 4, 8):
                    got, nodes, _ = simulate(g, (), h, p)
                    self.assertEqual((got, nodes), (v, c[0]))

    def test_perfect_order_measured(self):
        # The page states these numbers: 20 perfectly ordered trees, seeds
        # 80000 to 80019, b = 4, height 6, depth 6, min_split 2.
        ybw = {p: [0, 0] for p in (1, 2, 4, 8)}
        nowait = {p: [0, 0] for p in (1, 2, 4, 8)}
        for seed in range(20):
            g = PerfectOrder(RandomGame(80000 + seed, 4, 6), 6)
            for p in ybw:
                for table, wait in ((ybw, True), (nowait, False)):
                    _, nodes, steps = simulate(g, (), 6, p, wait)
                    table[p][0] += nodes
                    table[p][1] += steps
        self.assertEqual(critical_nodes(4, 6), 268)
        self.assertEqual(ybw, {1: [5360, 5360], 2: [5360, 3200], 4: [5360, 1840], 8: [5360, 1420]})
        self.assertEqual(nowait, {1: [5360, 5360], 2: [8619, 4339], 4: [13887, 3494], 8: [18681, 2374]})

    def test_random_order_measured(self):
        # The page states these numbers: 100 trees, seeds 50000 to 50099, b = 4,
        # height 6, depth 6, moves ordered by their static score.
        seq = 0
        ybw = {p: [0, 0] for p in (2, 4, 8)}
        nowait = {p: [0, 0] for p in (2, 4, 8)}
        for seed in range(100):
            g = RandomGame(50000 + seed, b=4, height=6)
            c = [0]
            alphabeta(g, (), 6, -INF, INF, c)
            seq += c[0]
            for p in ybw:
                for table, wait in ((ybw, True), (nowait, False)):
                    _, nodes, steps = simulate(g, (), 6, p, wait)
                    table[p][0] += nodes
                    table[p][1] += steps
        self.assertEqual(seq, 38839)
        self.assertEqual(ybw, {2: [42250, 23288], 4: [44381, 13972], 8: [44951, 10370]})
        self.assertEqual(nowait, {2: [60282, 30239], 4: [107363, 27003], 8: [157021, 19919]})


if __name__ == "__main__":
    unittest.main()
