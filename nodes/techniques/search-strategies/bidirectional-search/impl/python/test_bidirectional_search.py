# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bidirectional-search/. The authors are listed in prov/921J83.jsonl.

import random
import unittest
from collections import deque

from bidirectional_search import bidirectional_search


def preds(edges):
    r: dict = {v: [] for v in edges}
    for u in edges:
        for v in edges[u]:
            r[v].append(u)
    return r


def bfs_distance(edges, s, t):
    """Independent oracle: one-way breadth-first search."""
    d = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in edges[u]:
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d.get(t)


class TestPageExample(unittest.TestCase):
    E = {"S": ["A", "C"], "A": ["B"], "B": ["D"], "C": ["D"], "D": ["G"], "G": []}

    def test_shortest_path(self):
        r = preds(self.E)
        trace: list = []
        p = bidirectional_search("S", "G", lambda s: self.E[s], lambda s: r[s], trace)
        self.assertEqual(p, ["S", "C", "D", "G"])
        self.assertEqual(trace, [("f", 1), ("b", 1), ("b", 1)])

    def test_tree_counts(self):
        self.assertEqual(sum(10**i for i in range(1, 7)), 1111110)
        self.assertEqual(2 * sum(10**i for i in range(1, 4)), 2220)


class TestEdgeCases(unittest.TestCase):
    def test_same_state(self):
        self.assertEqual(bidirectional_search(1, 1, lambda s: [], lambda s: []), [1])

    def test_unreachable(self):
        e = {0: [1], 1: [0], 2: [3], 3: []}
        r = preds(e)
        self.assertIsNone(bidirectional_search(0, 3, lambda s: e[s], lambda s: r[s]))

    def test_direct_edge(self):
        e = {0: [1], 1: []}
        r = preds(e)
        self.assertEqual(bidirectional_search(0, 1, lambda s: e[s], lambda s: r[s]), [0, 1])

    def test_infinite_line(self):
        p = bidirectional_search(0, 40, lambda s: [s - 1, s + 1], lambda s: [s - 1, s + 1])
        self.assertEqual(p, list(range(41)))

    def test_grid(self):
        def nb(c):
            x, y = c
            return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        p = bidirectional_search((0, 0), (5, -3), nb, nb)
        self.assertEqual(len(p) - 1, 8)
        for a, b in zip(p, p[1:]):
            self.assertIn(b, nb(a))


class TestRandom(unittest.TestCase):
    def test_against_bfs(self):
        rng = random.Random(1971)
        for trial in range(1000):
            n = rng.randint(1, 10)
            e = {u: [v for v in range(n) if v != u and rng.random() < 0.25] for u in range(n)}
            r = preds(e)
            s, t = rng.randrange(n), rng.randrange(n)
            d = bfs_distance(e, s, t)
            p = bidirectional_search(s, t, lambda x: e[x], lambda x: r[x])
            if d is None:
                self.assertIsNone(p, trial)
            else:
                self.assertEqual(len(p) - 1, d, trial)
                self.assertEqual((p[0], p[-1]), (s, t))
                for a, b in zip(p, p[1:]):
                    self.assertIn(b, e[a])


if __name__ == "__main__":
    unittest.main()
