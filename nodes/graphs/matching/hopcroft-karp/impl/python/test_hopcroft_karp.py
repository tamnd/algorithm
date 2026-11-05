# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-karp/. The authors are listed in prov/V8H9RQ.jsonl.

import math
import random
import unittest
from functools import lru_cache

from hopcroft_karp import hopcroft_karp


def brute_nu(n_left: int, n_right: int, edges: list[tuple[int, int]]) -> int:
    """Largest matching size by dynamic programming over subsets of the right side."""
    adj = [sorted({y for (x, y) in edges if x == i}) for i in range(n_left)]

    @lru_cache(maxsize=None)
    def best(i: int, used: int) -> int:
        if i == n_left:
            return 0
        res = best(i + 1, used)
        for y in adj[i]:
            if not used >> y & 1:
                res = max(res, 1 + best(i + 1, used | 1 << y))
        return res

    return best(0, 0)


def check_matching(tc, n_left, n_right, edges, res):
    es = set(edges)
    count = 0
    for x in range(n_left):
        y = res.mate_left[x]
        if y >= 0:
            count += 1
            tc.assertIn((x, y), es)
            tc.assertEqual(res.mate_right[y], x)
    for y in range(n_right):
        x = res.mate_right[y]
        if x >= 0:
            tc.assertEqual(res.mate_left[x], y)
    tc.assertEqual(count, res.size)


class TestHopcroftKarp(unittest.TestCase):
    def test_worked_example(self):
        # X = 1..4 as 0..3, Y = a..d as 0..3.
        edges = [(0, 0), (0, 1), (1, 0), (2, 1), (2, 2), (3, 2), (3, 3)]
        log = []
        res = hopcroft_karp(4, 4, edges, lambda p, d, paths: log.append((p, d, paths)))
        self.assertEqual(res.size, 4)
        self.assertEqual(res.mate_left, [1, 0, 2, 3])
        self.assertEqual(res.phases, 3)
        self.assertEqual(log[0], (1, 1, [[0, 0], [2, 1], [3, 2]]))
        self.assertEqual(log[1], (2, 4, [[1, 0, 0, 1, 2, 2, 3, 3]]))
        check_matching(self, 4, 4, edges, res)

    def test_empty_graph(self):
        res = hopcroft_karp(0, 0, [])
        self.assertEqual(res.size, 0)
        self.assertEqual(res.phases, 1)
        res = hopcroft_karp(3, 2, [])
        self.assertEqual((res.size, res.mate_left, res.mate_right), (0, [-1, -1, -1], [-1, -1]))

    def test_no_perfect_matching(self):
        # A, B, C adjacent to 1, 2; D to 3, 4; E to 4, 5.
        edges = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 2), (3, 3), (4, 3), (4, 4)]
        res = hopcroft_karp(5, 5, edges)
        self.assertEqual(res.size, 4)
        check_matching(self, 5, 5, edges, res)

    def test_complete_and_star(self):
        edges = [(x, y) for x in range(3) for y in range(5)]
        self.assertEqual(hopcroft_karp(3, 5, edges).size, 3)
        self.assertEqual(hopcroft_karp(5, 3, [(y, x) for x, y in edges]).size, 3)
        self.assertEqual(hopcroft_karp(1, 4, [(0, y) for y in range(4)]).size, 1)

    def test_even_cycle_and_parallel_edges(self):
        # C_6 as x0 y0 x1 y1 x2 y2.
        edges = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (0, 2), (0, 0)]
        res = hopcroft_karp(3, 3, edges)
        self.assertEqual(res.size, 3)

    def test_long_path_many_phases(self):
        # A path whose greedy first phase leaves one long augmenting path.
        k = 30
        edges = [(i, i) for i in range(k)] + [(i + 1, i) for i in range(k)] + [(0, k)]
        res = hopcroft_karp(k + 1, k + 1, edges)
        self.assertEqual(res.size, k + 1)
        check_matching(self, k + 1, k + 1, edges, res)

    def test_bad_edge(self):
        with self.assertRaises(ValueError):
            hopcroft_karp(1, 1, [(0, 1)])

    def test_random_against_brute_force(self):
        rng = random.Random(20260511)
        for _ in range(800):
            nl = rng.randint(0, 7)
            nr = rng.randint(0, 7)
            p = rng.random()
            edges = [(x, y) for x in range(nl) for y in range(nr) if rng.random() < p]
            rng.shuffle(edges)
            lengths = []
            res = hopcroft_karp(nl, nr, edges, lambda ph, d, paths: lengths.append(d))
            self.assertEqual(res.size, brute_nu(nl, nr, edges))
            check_matching(self, nl, nr, edges, res)
            # Shortest augmenting path lengths strictly increase from phase to phase.
            self.assertTrue(all(a < b for a, b in zip(lengths, lengths[1:])))
            self.assertLessEqual(res.phases - 1, 2 * math.sqrt(res.size) + 1)


if __name__ == "__main__":
    unittest.main()
