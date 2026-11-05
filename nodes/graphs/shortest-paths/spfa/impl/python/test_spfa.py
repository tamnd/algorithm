# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spfa/. The authors are listed in prov/W784DG.jsonl.

import random
import unittest

from spfa import spfa

NAMES = "stxyz"
CLRS_22_4 = [
    ("s", "t", 6), ("s", "y", 7), ("t", "x", 5), ("t", "y", 8), ("t", "z", -4),
    ("x", "t", -2), ("y", "x", -3), ("y", "z", 9), ("z", "s", 2), ("z", "x", 7),
]


def build(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def named(edges):
    return [(NAMES.index(a), NAMES.index(b), w) for a, b, w in edges]


def bellman_ford(n, edges, s):
    """Independent oracle: n - 1 full passes, then one more to find a reachable negative cycle."""
    dist = [None] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] is not None and (dist[v] is None or dist[u] + w < dist[v]):
                dist[v] = dist[u] + w
    for u, v, w in edges:
        if dist[u] is not None and (dist[v] is None or dist[u] + w < dist[v]):
            return None
    return dist


def check_tree(adj, s, dist, parent):
    """Each parent arc is tight and every reachable vertex leads back to s."""
    n = len(adj)
    for v in range(n):
        if v == s or dist[v] is None:
            continue
        u = parent[v]
        assert u is not None
        assert any(x == v and dist[u] + w == dist[v] for x, w in adj[u])
        seen, x = 0, v
        while x != s:
            x = parent[x]
            seen += 1
            assert seen <= n


class TestSPFA(unittest.TestCase):
    def test_clrs_example(self):
        adj = build(5, named(CLRS_22_4))
        dist, parent = spfa(adj, 0)
        self.assertEqual(dist, [0, 2, 4, 7, -2])
        self.assertEqual([NAMES[p] if p is not None else None for p in parent], [None, "x", "y", "s", "t"])

    def test_negative_cycle_reachable(self):
        edges = [e if e[:2] != ("x", "t") else ("x", "t", -6) for e in CLRS_22_4]
        self.assertIsNone(spfa(build(5, named(edges)), 0))

    def test_negative_self_loop(self):
        self.assertIsNone(spfa(build(1, [(0, 0, -1)]), 0))
        self.assertIsNone(spfa(build(3, [(0, 1, 1), (1, 2, 1), (2, 2, -1)]), 0))

    def test_negative_cycle_not_reachable(self):
        edges = named(CLRS_22_4) + [(5, 6, -1), (6, 5, -1), (5, 0, 1)]
        dist, parent = spfa(build(7, edges), 0)
        self.assertEqual(dist, [0, 2, 4, 7, -2, None, None])
        self.assertIsNone(parent[5])

    def test_unreachable_and_single(self):
        self.assertEqual(spfa([[]], 0), ([0], [None]))
        dist, parent = spfa(build(4, [(0, 1, 3), (2, 3, -5)]), 0)
        self.assertEqual(dist, [0, 3, None, None])
        self.assertEqual(parent, [None, 0, None, None])

    def test_zero_cycle(self):
        dist, parent = spfa(build(3, [(0, 1, 1), (1, 2, 0), (2, 1, 0)]), 0)
        self.assertEqual(dist, [0, 1, 1])
        self.assertEqual(parent, [None, 0, 1])

    def test_random_against_bellman_ford(self):
        rng = random.Random(1956)
        negative = 0
        for _ in range(800):
            n = rng.randint(1, 8)
            m = rng.randint(0, 3 * n)
            low = rng.choice([0, -2, -5])
            edges = [(rng.randrange(n), rng.randrange(n), rng.randint(low, 9)) for _ in range(m)]
            s = rng.randrange(n)
            adj = build(n, edges)
            expected = bellman_ford(n, edges, s)
            got = spfa(adj, s)
            if expected is None:
                negative += 1
                self.assertIsNone(got)
            else:
                self.assertIsNotNone(got)
                dist, parent = got
                self.assertEqual(dist, expected)
                check_tree(adj, s, dist, parent)
        self.assertGreater(negative, 50)


if __name__ == "__main__":
    unittest.main()
