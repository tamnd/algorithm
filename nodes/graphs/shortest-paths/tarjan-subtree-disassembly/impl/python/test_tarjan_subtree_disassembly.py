# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-subtree-disassembly/. The authors are listed in prov/8J5TGF.jsonl.

import random
import unittest

from tarjan_subtree_disassembly import tarjan_subtree_disassembly

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
    """Independent oracle: n - 1 passes, then one more to see a reachable negative cycle."""
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


def cycle_weight(adj, cycle):
    """Least weight of the closed walk through the listed vertices, using the cheapest parallel arc."""
    total = 0
    for i, a in enumerate(cycle):
        b = cycle[(i + 1) % len(cycle)]
        total += min(w for x, w in adj[a] if x == b)
    return total


def reachable(adj, s):
    seen, stack = {s}, [s]
    while stack:
        u = stack.pop()
        for v, _ in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


class TestSubtreeDisassembly(unittest.TestCase):
    def test_clrs_example(self):
        dist, parent, cycle = tarjan_subtree_disassembly(build(5, named(CLRS_22_4)), 0)
        self.assertIsNone(cycle)
        self.assertEqual(dist, [0, 2, 4, 7, -2])
        self.assertEqual([NAMES[p] if p is not None else None for p in parent], [None, "x", "y", "s", "t"])

    def test_negative_cycle_example(self):
        edges = [e if e[:2] != ("x", "t") else ("x", "t", -6) for e in CLRS_22_4]
        dist, parent, cycle = tarjan_subtree_disassembly(build(5, named(edges)), 0)
        self.assertIsNone(dist)
        self.assertEqual([NAMES[c] for c in cycle], ["x", "t"])

    def test_self_loop(self):
        _, _, cycle = tarjan_subtree_disassembly(build(2, [(0, 1, 1), (1, 1, -1)]), 0)
        self.assertEqual(cycle, [1])
        _, _, cycle = tarjan_subtree_disassembly(build(1, [(0, 0, -2)]), 0)
        self.assertEqual(cycle, [0])

    def test_unreachable_negative_cycle_and_vertices(self):
        edges = named(CLRS_22_4) + [(5, 6, -1), (6, 5, -1), (5, 0, 1)]
        dist, parent, cycle = tarjan_subtree_disassembly(build(8, edges), 0)
        self.assertIsNone(cycle)
        self.assertEqual(dist, [0, 2, 4, 7, -2, None, None, None])
        self.assertEqual(parent[5:], [None, None, None])

    def test_single_vertex_and_zero_cycle(self):
        self.assertEqual(tarjan_subtree_disassembly([[]], 0), ([0], [None], None))
        dist, parent, cycle = tarjan_subtree_disassembly(build(3, [(0, 1, 1), (1, 2, 0), (2, 1, 0)]), 0)
        self.assertEqual((dist, parent, cycle), ([0, 1, 1], [None, 0, 1], None))

    def test_random_against_bellman_ford(self):
        rng = random.Random(1981)
        negative = 0
        for _ in range(800):
            n = rng.randint(1, 8)
            m = rng.randint(0, 3 * n)
            low = rng.choice([0, -2, -5])
            edges = [(rng.randrange(n), rng.randrange(n), rng.randint(low, 9)) for _ in range(m)]
            s = rng.randrange(n)
            adj = build(n, edges)
            expected = bellman_ford(n, edges, s)
            dist, parent, cycle = tarjan_subtree_disassembly(adj, s)
            if expected is None:
                negative += 1
                self.assertIsNotNone(cycle)
                self.assertEqual(len(set(cycle)), len(cycle))
                self.assertLess(cycle_weight(adj, cycle), 0)
                self.assertIn(cycle[0], reachable(adj, s))
            else:
                self.assertIsNone(cycle)
                self.assertEqual(dist, expected)
                for v in range(n):
                    if v != s and dist[v] is not None:
                        u = parent[v]
                        self.assertTrue(any(x == v and dist[u] + w == dist[v] for x, w in adj[u]))
        self.assertGreater(negative, 50)


if __name__ == "__main__":
    unittest.main()
