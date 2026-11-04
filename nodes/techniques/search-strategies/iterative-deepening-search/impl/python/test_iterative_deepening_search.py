# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-deepening-search/. The authors are listed in prov/76CY83.jsonl.

import random
import unittest
from collections import deque

from iterative_deepening_search import CUTOFF, iterative_deepening_search

E = {"S": ["A", "G"], "A": ["B", "C"], "B": ["D"], "C": ["D", "G"], "D": ["G"], "G": []}


def run(goal, edges=E, start="S", max_depth=None):
    trace: list = []
    r = iterative_deepening_search(start, lambda s: edges[s], lambda s: s == goal, max_depth, trace)
    return r, trace


def bfs_distance(edges, start, goals):
    """Independent oracle: the fewest actions from start to a goal, or None."""
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        if u in goals:
            return dist[u]
        for v in edges[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return None


class TestPageExample(unittest.TestCase):
    def test_goal_d(self):
        r, trace = run("D")
        self.assertEqual(r, ["S", "A", "B", "D"])
        self.assertEqual(trace, ["S", "S", "A", "G", "S", "A", "B", "C", "G", "S", "A", "B", "D"])

    def test_goal_g_shallowest(self):
        r, trace = run("G")
        self.assertEqual(r, ["S", "G"])
        self.assertEqual(len(trace), 4)

    def test_missing_goal(self):
        r, trace = run("E")
        self.assertIsNone(r)
        self.assertEqual(len(trace), 27)

    def test_counts_table(self):
        def n_ids(b, d):
            return sum((d + 1 - i) * b**i for i in range(1, d + 1))

        def n_bfs(b, d):
            return sum(b**i for i in range(1, d + 1))

        self.assertEqual((n_ids(10, 5), n_bfs(10, 5)), (123450, 111110))
        self.assertEqual((n_ids(2, 10), n_bfs(2, 10)), (4072, 2046))
        self.assertEqual((n_ids(3, 8), n_bfs(3, 8)), (14748, 9840))
        self.assertEqual(n_ids(10, 10), 12345679000)
        for b in range(2, 12):
            for d in range(1, 12):
                self.assertLess(n_ids(b, d) * (b - 1), b * n_bfs(b, d))

    def test_uniform_tree_generated(self):
        # tree of branching 3, goal is the last node of depth 4; count generated nodes
        b, d = 3, 4
        last = tuple([b - 1] * d)
        trace: list = []
        iterative_deepening_search((), lambda s: [s + (i,) for i in range(b)] if len(s) < 10 else [],
                                   lambda s: s == last, trace=trace)
        generated = len(trace) - (d + 1)  # every run also tests the root
        self.assertEqual(generated, sum((d + 1 - i) * b**i for i in range(1, d + 1)))


class TestEdgeCases(unittest.TestCase):
    def test_start_is_goal(self):
        self.assertEqual(run("S")[0], ["S"])

    def test_cycle_no_goal_stops(self):
        edges = {"u": ["v"], "v": ["u", "w"], "w": ["u"]}
        self.assertIsNone(run("x", edges, "u")[0])

    def test_infinite_no_goal_with_max_depth(self):
        r = iterative_deepening_search(0, lambda s: [s + 1], lambda s: False, max_depth=20)
        self.assertEqual(r, CUTOFF)

    def test_infinite_space_with_goal(self):
        r = iterative_deepening_search(1, lambda s: [s + 1, 2 * s], lambda s: s == 37)
        self.assertEqual(len(r) - 1, 7)
        self.assertEqual(r[-1], 37)


class TestRandom(unittest.TestCase):
    def test_against_bfs(self):
        rng = random.Random(76)
        for trial in range(800):
            n = rng.randint(1, 9)
            edges = {u: [v for v in range(n) if rng.random() < 0.3] for u in range(n)}
            goals = {v for v in range(n) if rng.random() < 0.2}
            d = bfs_distance(edges, 0, goals)
            r = iterative_deepening_search(0, lambda s: edges[s], lambda s: s in goals)
            if d is None:
                self.assertIsNone(r, trial)
            else:
                self.assertEqual(len(r) - 1, d, trial)
                self.assertEqual(r[0], 0)
                self.assertIn(r[-1], goals)
                for a, b in zip(r, r[1:]):
                    self.assertIn(b, edges[a])


if __name__ == "__main__":
    unittest.main()
