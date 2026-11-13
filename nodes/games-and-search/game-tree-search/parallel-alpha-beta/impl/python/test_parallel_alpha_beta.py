# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-alpha-beta/. The authors are listed in prov/8BYDFQ.jsonl.

import random
import unittest

from parallel_alpha_beta import INF, RandomGame, alphabeta, simulate


def negamax(g, n, depth):
    """Reference: plain negamax to a fixed depth, no pruning."""
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    return max(-negamax(g, c, depth - 1) for c in kids)


class TestParallelAlphaBeta(unittest.TestCase):
    def test_alphabeta_reference(self):
        for seed in range(500):
            g = RandomGame(seed, b=3, height=5)
            self.assertEqual(alphabeta(g, (), 5, -INF, INF), negamax(g, (), 5))

    def test_same_value_as_sequential(self):
        rng = random.Random(61)
        for seed in range(500):
            b, h = rng.randint(2, 4), rng.randint(1, 5)
            g = RandomGame(1000 + seed, b=b, height=h)
            want = alphabeta(g, (), h, -INF, INF)
            for p in (1, 2, 4, 8):
                for wait in (True, False):
                    self.assertEqual(simulate(g, (), h, p, wait, min_split=rng.randint(1, 3))[0], want)

    def test_one_processor_is_sequential(self):
        # With one processor the stack order runs the children in order, and each
        # child reads the up-to-date window, so the search is sequential alpha-beta.
        for seed in range(200):
            g = RandomGame(3000 + seed, b=3, height=5)
            c = [0]
            v = alphabeta(g, (), 5, -INF, INF, c)
            self.assertEqual(simulate(g, (), 5, 1), (v, c[0], c[0]))

    def test_measured_overhead_and_speedup(self):
        # The page states these numbers: 100 trees, seeds 50000 to 50099, b = 4,
        # height 6, depth 6, swing 9, min_split 2, Young Brothers Wait.
        seq = 0
        got = {p: [0, 0] for p in (1, 2, 4, 8)}
        for seed in range(100):
            g = RandomGame(50000 + seed, b=4, height=6)
            c = [0]
            alphabeta(g, (), 6, -INF, INF, c)
            seq += c[0]
            for p in got:
                _, nodes, steps = simulate(g, (), 6, p)
                got[p][0] += nodes
                got[p][1] += steps
        self.assertEqual(seq, 38839)
        self.assertEqual(got, {1: [38839, 38839], 2: [42250, 23288], 4: [44381, 13972], 8: [44951, 10370]})


if __name__ == "__main__":
    unittest.main()
