# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/depth-limited-search/. The authors are listed in prov/T1ZWEX.jsonl.

import random
import unittest
from collections import deque

from depth_limited_search import CUTOFF, depth_limited_search

E = {"S": ["A", "G"], "A": ["B", "C"], "B": ["D"], "C": ["D", "G"], "D": ["G"], "G": []}


def run(goal, limit, edges=E, start="S", check_cycles=True):
    trace: list = []
    r = depth_limited_search(start, lambda s: edges[s], lambda s: s == goal, limit, check_cycles, trace)
    return r, trace


def oracle(n, edges, start, goals, limit):
    """BFS shortest distance to a goal and the length of the longest simple path, by brute force."""
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in edges[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    d = min((dist[g] for g in goals if g in dist), default=None)
    reachable = d is not None
    # does some simple path from start have more than `limit` actions?
    longer = False
    stack = [(start, frozenset([start]), 0)]
    while stack and not longer:
        u, seen, k = stack.pop()
        for v in edges[u]:
            if v not in seen:
                if k + 1 > limit:
                    longer = True
                    break
                stack.append((v, seen | {v}, k + 1))
    return d, reachable, longer


class TestPageExample(unittest.TestCase):
    def test_goal_d(self):
        for limit in (0, 1, 2):
            self.assertEqual(run("D", limit)[0], CUTOFF)
        r, trace = run("D", 3)
        self.assertEqual(r, ["S", "A", "B", "D"])
        self.assertEqual(len(trace), 4)

    def test_goal_missing(self):
        expected = [(CUTOFF, 1), (CUTOFF, 3), (CUTOFF, 5), (CUTOFF, 8), (None, 10)]
        for limit, (ans, tests) in enumerate(expected):
            r, trace = run("E", limit)
            self.assertEqual((r, len(trace)), (ans, tests))
        self.assertEqual(run("E", 3)[1], ["S", "A", "B", "D", "C", "D", "G", "G"])

    def test_not_shortest(self):
        self.assertEqual(run("G", 4)[0], ["S", "A", "B", "D", "G"])

    def test_two_cycle(self):
        edges = {"u": ["v"], "v": ["u"]}
        self.assertEqual(run("x", 0, edges, "u")[0], CUTOFF)
        for limit in range(1, 6):
            self.assertIsNone(run("x", limit, edges, "u")[0])
            self.assertEqual(run("x", limit, edges, "u", check_cycles=False)[0], CUTOFF)


class TestEdgeCases(unittest.TestCase):
    def test_start_is_goal(self):
        self.assertEqual(run("S", 0)[0], ["S"])

    def test_negative_limit(self):
        with self.assertRaises(ValueError):
            run("G", -1)

    def test_large_limit_chain(self):
        n = 3000
        r = depth_limited_search(0, lambda s: [s + 1] if s < n else [], lambda s: s == n, n)
        self.assertEqual(r, list(range(n + 1)))
        self.assertEqual(depth_limited_search(0, lambda s: [s + 1], lambda s: s == n, n - 1), CUTOFF)

    def test_infinite_space_stops(self):
        r = depth_limited_search(1, lambda s: [2 * s, 2 * s + 1], lambda s: s == 13, 3)
        self.assertEqual(r, [1, 3, 6, 13])


class TestRandom(unittest.TestCase):
    def test_against_oracle(self):
        rng = random.Random(1985)
        for trial in range(700):
            n = rng.randint(1, 8)
            edges = {u: [v for v in range(n) if rng.random() < 0.3] for u in range(n)}
            goals = {v for v in range(n) if rng.random() < 0.2}
            limit = rng.randint(0, 6)
            d, reachable, longer = oracle(n, edges, 0, goals, limit)
            r = depth_limited_search(0, lambda s: edges[s], lambda s: s in goals, limit)
            if d is not None and d <= limit:
                self.assertIsInstance(r, list, trial)
                self.assertEqual(r[0], 0)
                self.assertIn(r[-1], goals)
                self.assertLessEqual(len(r) - 1, limit)
                self.assertEqual(len(set(r)), len(r))
                for a, b in zip(r, r[1:]):
                    self.assertIn(b, edges[a])
            elif longer:
                self.assertEqual(r, CUTOFF, trial)
            else:
                self.assertFalse(reachable, trial)
                self.assertIsNone(r, trial)


if __name__ == "__main__":
    unittest.main()
