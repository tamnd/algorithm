# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beam-search/. The authors are listed in prov/WJE1MW.jsonl.

import random
import unittest
from collections import deque

from beam_search import beam_search

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
    """4-connected grid with walls and unit costs; neighbors in the order E, W, S, N."""
    cells = {(x, y) for x in range(w) for y in range(hgt) if rng.random() >= wall}
    adj = {}
    for x, y in sorted(cells):
        adj[(x, y)] = [((x + dx, y + dy), 1) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                       if (x + dx, y + dy) in cells]
    return adj


def path_cost(test, adj, path):
    total = 0
    for u, v in zip(path, path[1:]):
        cs = [c for w, c in adj[u] if w == v]
        test.assertTrue(cs, f"{u} -> {v} is not an edge")
        total += min(cs)
    return total


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


# ---------------------------------------------------------------- the page example

PAGE = ["S.....",
        "...##.",
        "...#..",
        "..#.##",
        "#....G"]


def page_grid():
    cells = {(x, y) for y, row in enumerate(PAGE) for x, ch in enumerate(row) if ch != "#"}
    return {(x, y): [((x + dx, y + dy), 1) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                     if (x + dx, y + dy) in cells] for x, y in sorted(cells)}


class TestPageExample(unittest.TestCase):
    def run_width(self, k):
        adj = page_grid()
        goal = (5, 4)
        return beam_search((0, 0), lambda u: adj[u], lambda u: u == goal,
                           lambda u: abs(u[0] - 5) + abs(u[1] - 4), k)

    def test_page_grid_is_the_seeded_one(self):
        self.assertEqual(page_grid(), unit_grid(random.Random(804), 6, 5, 0.3))

    def test_width_one_fails(self):
        r = self.run_width(1)
        self.assertIsNone(r.path)
        self.assertEqual([x[0] for x in r.layers],
                         [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (4, 2)])

    def test_width_two_is_not_optimal(self):
        r = self.run_width(2)
        self.assertEqual(r.cost, 11)
        self.assertEqual(r.path[:4], [(0, 0), (1, 0), (2, 0), (2, 1)])

    def test_full_width_is_optimal(self):
        self.assertEqual(bfs(page_grid(), (0, 0))[(5, 4)], 9)
        self.assertEqual(self.run_width(None).cost, 9)
        self.assertEqual(self.run_width(30).cost, 9)

    def test_bad_width(self):
        with self.assertRaises(ValueError):
            beam_search(0, lambda u: [], lambda u: False, lambda u: 0, 0)


class TestRandom(unittest.TestCase):
    def test_grids(self):
        rng = random.Random(9)
        fails = worse = 0
        for _ in range(250):
            adj = unit_grid(rng, rng.randint(1, 9), rng.randint(1, 9), 0.3)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            dist = bfs(adj, s)
            h = lambda u, t=t: abs(u[0] - t[0]) + abs(u[1] - t[1])  # noqa: E731
            for k in (1, 2, 3, 5, None):
                r = beam_search(s, lambda u: adj[u], lambda u: u == t, h, k)
                if k is not None:
                    self.assertTrue(all(len(x) <= k for x in r.layers))
                if r.path is None:
                    if k is None:
                        self.assertNotIn(t, dist)  # full width fails only without a path
                    fails += t in dist
                    continue
                self.assertEqual((r.path[0], r.path[-1]), (s, t))
                self.assertEqual(path_cost(self, adj, r.path), r.cost)
                self.assertGreaterEqual(r.cost, dist[t])
                if k is None:
                    self.assertEqual(r.cost, dist[t])  # breadth-first search
                worse += r.cost > dist[t]
        self.assertGreater(fails, 0)
        self.assertGreater(worse, 0)

    def test_eight_puzzle(self):
        rng = random.Random(2024)
        for _ in range(10):
            s = GOAL8
            for _ in range(40):
                s = rng.choice(puzzle_successors(s))[0]
            for k in (1, 10, 100):
                r = beam_search(s, puzzle_successors, lambda u: u == GOAL8, puzzle_h, k)
                if r.path is not None:
                    self.assertEqual(r.path[-1], GOAL8)
                    self.assertEqual(len(r.path) - 1, r.cost)
                    self.assertTrue(all(b in [m for m, _ in puzzle_successors(a)]
                                        for a, b in zip(r.path, r.path[1:])))


if __name__ == "__main__":
    unittest.main()
