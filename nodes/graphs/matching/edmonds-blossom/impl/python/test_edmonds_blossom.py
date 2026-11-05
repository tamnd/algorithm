# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edmonds-blossom/. The authors are listed in prov/6F205G.jsonl.

import random
import unittest
from functools import lru_cache

from edmonds_blossom import edmonds_blossom


def brute_nu(n: int, edges: list[tuple[int, int]]) -> int:
    """Largest matching size by dynamic programming over vertex subsets."""
    adj = [0] * n
    for u, v in edges:
        if u != v:
            adj[u] |= 1 << v
            adj[v] |= 1 << u

    @lru_cache(maxsize=None)
    def best(mask: int) -> int:
        if mask == 0:
            return 0
        v = (mask & -mask).bit_length() - 1
        rest = mask & ~(1 << v)
        res = best(rest)
        cand = adj[v] & rest
        while cand:
            w = (cand & -cand).bit_length() - 1
            cand &= cand - 1
            res = max(res, 1 + best(rest & ~(1 << w)))
        return res

    return best((1 << n) - 1)


def run_checked(tc, n, edges):
    """Run with a callback that checks every reported path against the matching before it."""
    es = {(u, v) for u, v in edges} | {(v, u) for u, v in edges}
    mate = [-1] * n
    events = []

    def on_event(kind, data):
        events.append((kind, data))
        if kind != "augment":
            return
        path = list(data)
        tc.assertEqual(len(set(path)), len(path))
        tc.assertEqual(len(path) % 2, 0)
        tc.assertEqual(mate[path[0]], -1)
        tc.assertEqual(mate[path[-1]], -1)
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            tc.assertIn((a, b), es)
            tc.assertEqual(mate[a] == b, i % 2 == 1)
        for i in range(0, len(path), 2):
            mate[path[i]], mate[path[i + 1]] = path[i + 1], path[i]

    res = edmonds_blossom(n, edges, on_event)
    tc.assertEqual(res.mate, mate)
    count = 0
    for v in range(n):
        if res.mate[v] >= 0:
            tc.assertEqual(res.mate[res.mate[v]], v)
            tc.assertIn((v, res.mate[v]), es)
            count += 1
    tc.assertEqual(count, 2 * res.size)
    return res, events


def cycle(k):
    return [(i, (i + 1) % k) for i in range(k)]


PETERSEN = cycle(5) + [(i, i + 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)]


class TestEdmondsBlossom(unittest.TestCase):
    def test_worked_example(self):
        # a, c, r, t, d, b = 0, 1, 2, 3, 4, 5; edges ab, cb, ar, cd, rd, at.
        edges = [(0, 5), (1, 5), (0, 2), (1, 4), (2, 4), (0, 3)]
        res, events = run_checked(self, 6, edges)
        self.assertEqual(
            events,
            [
                ("augment", (0, 5)),
                ("augment", (1, 4)),
                ("blossom", (2, (0, 1, 2, 4, 5))),
                ("augment", (2, 4, 1, 5, 0, 3)),
            ],
        )
        self.assertEqual(res.size, 3)
        self.assertEqual(res.phases, 4)
        self.assertEqual(res.mate, [3, 5, 4, 0, 2, 1])

    def test_empty(self):
        self.assertEqual(edmonds_blossom(0, []), (0, [], 1))
        self.assertEqual(edmonds_blossom(4, []).size, 0)

    def test_odd_cycles(self):
        for k in (3, 5, 7, 9):
            res, _ = run_checked(self, k, cycle(k))
            self.assertEqual(res.size, k // 2)
            self.assertEqual(res.mate.count(-1), 1)

    def test_no_perfect_matching(self):
        # Star K_{1,3}, and two triangles joined at a cut vertex.
        self.assertEqual(run_checked(self, 4, [(0, 1), (0, 2), (0, 3)])[0].size, 1)
        bowtie = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)]
        self.assertEqual(run_checked(self, 5, bowtie)[0].size, 2)
        # Three triangles hanging off one vertex: removing it leaves 3 odd components.
        g = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (6, 7), (7, 8), (8, 6), (9, 0), (9, 3), (9, 6)]
        self.assertEqual(run_checked(self, 10, g)[0].size, 4)

    def test_petersen_and_complete(self):
        self.assertEqual(run_checked(self, 10, PETERSEN)[0].size, 5)
        k6 = [(u, v) for u in range(6) for v in range(u + 1, 6)]
        self.assertEqual(run_checked(self, 6, k6)[0].size, 3)

    def test_bipartite_and_loops(self):
        self.assertEqual(run_checked(self, 6, cycle(6))[0].size, 3)
        res = edmonds_blossom(3, [(0, 0), (0, 1), (0, 1), (2, 2)])
        self.assertEqual(res.size, 1)

    def test_nested_blossoms(self):
        # A triangle inside a 5-cycle-like structure with a long stem.
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 2), (3, 5), (4, 6), (5, 6), (6, 7), (1, 8), (8, 9)]
        res, _ = run_checked(self, 10, edges)
        self.assertEqual(res.size, brute_nu(10, edges))

    def test_bad_edge(self):
        with self.assertRaises(ValueError):
            edmonds_blossom(2, [(0, 2)])

    def test_random_against_brute_force(self):
        rng = random.Random(1965)
        for _ in range(700):
            n = rng.randint(0, 11)
            p = rng.random() * 0.7
            edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
            rng.shuffle(edges)
            edges = [(v, u) if rng.random() < 0.5 else (u, v) for u, v in edges]
            res, events = run_checked(self, n, edges)
            self.assertEqual(res.size, brute_nu(n, edges))
            self.assertEqual(res.phases, res.size + 1)


if __name__ == "__main__":
    unittest.main()
