# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-tile-puzzle/. The authors are listed in prov/8BMZ6Z.jsonl.
import random
import unittest
from collections import Counter
from math import factorial

from sliding_tile_puzzle import (
    bfs_distances,
    goal,
    ida_star,
    linear_conflict,
    manhattan,
    neighbours,
    scramble,
)

# OEIS A089473: states of the 8-puzzle at each distance from the goal.
EIGHT_PUZZLE = [1, 2, 4, 8, 16, 20, 39, 62, 116, 152, 286, 396, 748, 1024, 1893, 2512, 4485,
                5638, 9529, 10878, 16993, 17110, 23952, 20224, 24047, 15578, 14560, 6274,
                3910, 760, 221, 2]


class TestSmallBoards(unittest.TestCase):
    def test_two_by_three(self):
        dist = bfs_distances(3, 2)
        self.assertEqual(len(dist), factorial(6) // 2)
        self.assertEqual(max(dist.values()), 21)
        far = [s for s, d in dist.items() if d == 21]
        self.assertEqual(far, [(4, 5, 0, 1, 2, 3)])

    def test_two_by_four(self):
        dist = bfs_distances(4, 2)
        self.assertEqual(len(dist), factorial(8) // 2)
        self.assertEqual(max(dist.values()), 36)


class TestEightPuzzle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dist = bfs_distances(3, 3)

    def test_state_count_and_layers(self):
        self.assertEqual(len(self.dist), 181440)
        counts = Counter(self.dist.values())
        self.assertEqual([counts[d] for d in range(32)], EIGHT_PUZZLE)

    def test_antipodes(self):
        far = sorted(s for s, d in self.dist.items() if d == 31)
        self.assertEqual(far, [(6, 4, 7, 8, 5, 0, 3, 2, 1), (8, 6, 7, 2, 5, 4, 3, 0, 1)])

    def test_heuristics_are_admissible(self):
        for s, d in self.dist.items():
            m = manhattan(s, 3, 3)
            lc = linear_conflict(s, 3, 3)
            self.assertLessEqual(m, lc)
            self.assertLessEqual(lc, d)
            self.assertEqual(m % 2, d % 2)
            self.assertEqual(lc % 2, d % 2)

    def test_manhattan_is_consistent(self):
        for s in list(self.dist)[:20000]:
            for t in neighbours(s, 3, 3):
                self.assertEqual(abs(manhattan(s, 3, 3) - manhattan(t, 3, 3)), 1)

    def test_ida_star_is_optimal(self):
        rnd = random.Random(4)
        states = rnd.sample(sorted(self.dist), 25)
        states += [s for s, d in self.dist.items() if d == 31]
        for s in states:
            for hfun in (manhattan, linear_conflict):
                path = ida_star(s, 3, 3, hfun)
                self.assertEqual(len(path) - 1, self.dist[s])
                self.assertEqual(path[-1], goal(3, 3))
                for a, b in zip(path, path[1:]):
                    self.assertIn(b, set(neighbours(a, 3, 3)))


class TestFifteenPuzzle(unittest.TestCase):
    def test_heuristics_agree_on_optimal_length(self):
        rnd = random.Random(9)
        for _ in range(4):
            s = scramble(4, 4, 60, rnd)
            p1 = ida_star(s, 4, 4, linear_conflict)
            p2 = ida_star(s, 4, 4, manhattan)
            self.assertEqual(len(p1), len(p2))
            self.assertEqual(p1[-1], goal(4, 4))
            self.assertLessEqual(linear_conflict(s, 4, 4), len(p1) - 1)


if __name__ == "__main__":
    unittest.main()
