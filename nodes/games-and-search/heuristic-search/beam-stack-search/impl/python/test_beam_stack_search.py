# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beam-stack-search/. The authors are listed in prov/2Y0M90.jsonl.

import random
import unittest
from collections import deque

from beam_stack_search import beam_stack_search

# ---------------------------------------------------------------- oracles and generators


def bfs(adj, src):
    """Independent oracle: number of actions on a shortest path from src."""
    dist = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        for v, _ in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def unit_grid(rng, w, hgt, wall):
    cells = {(x, y) for x in range(w) for y in range(hgt) if rng.random() >= wall}
    adj = {}
    for x, y in sorted(cells):
        adj[(x, y)] = [((x + dx, y + dy), 1) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                       if (x + dx, y + dy) in cells]
    return adj


def random_unit_graph(rng, n, p):
    adj = {u: [] for u in range(n)}
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append((v, 1))
                adj[v].append((u, 1))
    return adj


def check_path(test, adj, path, s, t):
    test.assertEqual((path[0], path[-1]), (s, t))
    for u, v in zip(path, path[1:]):
        test.assertIn(v, [w for w, _ in adj[u]])


GOAL8 = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def puzzle_successors(s):
    i = s.index(0)
    r, c = divmod(i, 3)
    out = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= r + dr < 3 and 0 <= c + dc < 3:
            j = (r + dr) * 3 + c + dc
            t = list(s)
            t[i], t[j] = t[j], t[i]
            out.append((tuple(t), 1))
    return out


def puzzle_h(s):
    return sum(abs(i // 3 - (v - 1) // 3) + abs(i % 3 - (v - 1) % 3) for i, v in enumerate(s) if v)


class TestPageExample(unittest.TestCase):
    START = (0, 2, 6, 8, 3, 5, 1, 7, 4)  # the 8-puzzle of the page, 18 moves from the goal

    def test_table(self):
        want = {1: ([22, 18], 144, 10, 50), 2: ([22, 18], 149, 10, 53),
                5: ([36, 32, 22, 18], 481, 17, 131), 20: ([18], 201, 0, 201),
                100: ([18], 857, 0, 857)}
        for k, row in want.items():
            r = beam_stack_search(self.START, puzzle_successors, lambda u: u == GOAL8, puzzle_h, k)
            self.assertEqual(([c for c, _ in r.solutions], r.expanded, r.backtracks,
                              r.peak_stored), row)
            self.assertEqual(r.cost, 18)
            self.assertEqual(len(r.path) - 1, 18)

    def test_seeded_start(self):
        rng = random.Random(2024)
        s = GOAL8
        for _ in range(60):
            s = rng.choice(puzzle_successors(s))[0]
        self.assertEqual(s, self.START)

    def test_small_cases(self):
        r = beam_stack_search(0, lambda u: [(1, 1)], lambda u: u == 0, lambda u: 0, 1)
        self.assertEqual((r.path, r.cost), ([0], 0))
        adj = {0: [(1, 1)], 1: [(0, 1)], 2: []}
        r = beam_stack_search(0, lambda u: adj[u], lambda u: u == 2, lambda u: 0, 1)
        self.assertIsNone(r.path)
        with self.assertRaises(ValueError):
            beam_stack_search(0, lambda u: [], lambda u: False, lambda u: 0, 0)


class TestOptimal(unittest.TestCase):
    def run_case(self, adj, s, t, h, k):
        r = beam_stack_search(s, lambda u: adj[u], lambda u: u == t, h, k)
        dist = bfs(adj, s)
        if t not in dist:
            self.assertIsNone(r.path)
            return r
        check_path(self, adj, r.path, s, t)
        self.assertEqual(r.cost, dist[t])
        self.assertEqual(len(r.path) - 1, r.cost)
        costs = [c for c, _ in r.solutions]
        self.assertEqual(costs, sorted(set(costs), reverse=True))  # each solution is better
        return r

    def test_grids(self):
        rng = random.Random(21)
        for _ in range(120):
            adj = unit_grid(rng, rng.randint(1, 8), rng.randint(1, 8), 0.3)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            for k in (1, 2, 4):
                self.run_case(adj, s, t, lambda u: abs(u[0] - t[0]) + abs(u[1] - t[1]), k)

    def test_graphs_with_a_weak_heuristic(self):
        rng = random.Random(4)
        for _ in range(300):
            n = rng.randint(2, 14)
            adj = random_unit_graph(rng, n, rng.uniform(0.15, 0.5))
            t = rng.randrange(n)
            ht = bfs(adj, t)
            hv = [ht.get(u, 0) // 2 for u in range(n)]  # consistent: half the exact distance
            for k in (1, 2):
                self.run_case(adj, rng.randrange(n), t, lambda u: hv[u], k)

    def test_eight_puzzle(self):
        rng = random.Random(7)
        total_backtracks = 0
        for _ in range(6):
            s = GOAL8
            for _ in range(40):
                s = rng.choice(puzzle_successors(s))[0]
            d = bfs_puzzle(s)
            for k in (1, 3, 10):
                r = beam_stack_search(s, puzzle_successors, lambda u: u == GOAL8, puzzle_h, k)
                self.assertEqual(r.cost, d)
                self.assertEqual(r.path[-1], GOAL8)
                total_backtracks += r.backtracks
        self.assertGreater(total_backtracks, 0)


def bfs_puzzle(s):
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        if u == GOAL8:
            return dist[u]
        for v, _ in puzzle_successors(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)


if __name__ == "__main__":
    unittest.main()
