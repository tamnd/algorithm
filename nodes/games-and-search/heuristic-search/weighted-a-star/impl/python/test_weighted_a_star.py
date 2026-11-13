# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-a-star/. The authors are listed in prov/887HFH.jsonl.

import heapq
import random
import unittest
from collections import deque
from fractions import Fraction

from weighted_a_star import weighted_a_star

WEIGHTS = (1, Fraction(5, 4), Fraction(3, 2), 2, 3, 5)

# ---------------------------------------------------------------- oracles and generators


def dijkstra(adj, src):
    """Independent oracle: exact distances from src on a nonnegative graph."""
    dist = {src: 0}
    pq = [(0, src)]
    done = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        for v, c in adj[u]:
            if v not in dist or d + c < dist[v]:
                dist[v] = d + c
                heapq.heappush(pq, (d + c, v))
    return dist


def reverse(adj):
    r = {u: [] for u in adj}
    for u in adj:
        for v, c in adj[u]:
            r[v].append((u, c))
    return r


def random_grid(rng, w, hgt, wall, cmax):
    """4-connected grid with walls; entering a cell costs 1 to cmax."""
    cells = [(x, y) for x in range(w) for y in range(hgt) if rng.random() >= wall]
    cost = {v: rng.randint(1, cmax) for v in cells}
    adj = {v: [] for v in cells}
    for x, y in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            m = (x + dx, y + dy)
            if m in cost:
                adj[(x, y)].append((m, cost[m]))
    return adj


def random_digraph(rng, n, p, cmax):
    adj = {u: [] for u in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < p:
                adj[u].append((v, rng.randint(1, cmax)))
    return adj


def check_path(test, adj, path, s, cost):
    test.assertEqual(path[0], s)
    total = 0
    for u, v in zip(path, path[1:]):
        cs = [c for w, c in adj[u] if w == v]
        test.assertTrue(cs, f"{u} -> {v} is not an edge")
        total += min(cs)
    test.assertEqual(total, cost)


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


def puzzle_bfs(s):
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


# ---------------------------------------------------------------- the page example

POS = {"S": (0, 0), "A": (2, 0), "B": (0, 2), "C": (2, 2),
       "D": (4, 0), "E": (0, 4), "F": (-1, 0), "G": (4, 2)}
EDGES = [("S", "A", 2), ("S", "B", 3), ("A", "C", 4), ("A", "D", 3), ("B", "C", 2),
         ("B", "E", 2), ("C", "G", 2), ("D", "G", 3), ("S", "F", 1)]


def page_graph():
    adj = {v: [] for v in POS}
    for u, v, c in EDGES:
        adj[u].append((v, c))
        adj[v].append((u, c))
    for v in adj:
        adj[v].sort()
    return adj


def manhattan(u):
    return abs(POS[u][0] - 4) + abs(POS[u][1] - 2)


class TestPageExample(unittest.TestCase):
    def test_trace(self):
        adj = page_graph()
        succ, goal = (lambda u: adj[u]), (lambda u: u == "G")
        r = weighted_a_star("S", succ, goal, manhattan, 1)
        self.assertEqual((r.path, r.cost), (["S", "B", "C", "G"], 7))
        self.assertEqual(r.expanded, ["S", "A", "D", "B", "C"])
        for w in (Fraction(5, 4), Fraction(3, 2), 2, 3, 5):
            r = weighted_a_star("S", succ, goal, manhattan, w)
            self.assertEqual((r.path, r.cost), (["S", "A", "D", "G"], 8))
            self.assertEqual(r.expanded, ["S", "A", "D"])

    def test_bad_weight(self):
        with self.assertRaises(ValueError):
            weighted_a_star(0, lambda u: [], lambda u: True, lambda u: 0, Fraction(1, 2))


class TestBound(unittest.TestCase):
    def test_grids_consistent(self):
        rng = random.Random(3)
        for _ in range(120):
            adj = random_grid(rng, rng.randint(1, 10), rng.randint(1, 10), 0.25, 5)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            dist = dijkstra(adj, s)
            for w in WEIGHTS:
                for reopen in (True, False):
                    r = weighted_a_star(s, lambda u: adj[u], lambda u: u == t,
                                        lambda u: abs(u[0] - t[0]) + abs(u[1] - t[1]), w, reopen)
                    if t not in dist:
                        self.assertIsNone(r.path)
                        continue
                    check_path(self, adj, r.path, s, r.cost)
                    self.assertEqual(r.path[-1], t)
                    self.assertLessEqual(r.cost, w * dist[t])
                    if w == 1:
                        self.assertEqual(r.cost, dist[t])
                    if not reopen:
                        self.assertEqual(r.reopenings, 0)

    def test_digraphs_admissible_with_reopening(self):
        rng = random.Random(8)
        reopened = 0
        for _ in range(300):
            n = rng.randint(2, 16)
            adj = random_digraph(rng, n, rng.uniform(0.1, 0.4), 9)
            t = rng.randrange(n)
            hstar = dijkstra(reverse(adj), t)
            hv = [rng.randint(0, hstar[u]) if u in hstar else rng.randint(0, 50) for u in range(n)]
            s = rng.randrange(n)
            dist = dijkstra(adj, s)
            for w in WEIGHTS:
                r = weighted_a_star(s, lambda u: adj[u], lambda u: u == t, lambda u: hv[u], w)
                reopened += r.reopenings
                if t not in dist:
                    self.assertIsNone(r.path)
                    continue
                check_path(self, adj, r.path, s, r.cost)
                self.assertLessEqual(r.cost, w * dist[t])
        self.assertGreater(reopened, 0)  # the random h is often not consistent

    def test_eight_puzzle(self):
        rng = random.Random(2024)
        for _ in range(6):
            s = GOAL8
            for _ in range(40):
                s = rng.choice(puzzle_successors(s))[0]
            d = puzzle_bfs(s)
            for w in (1, Fraction(3, 2), 2, 5):
                r = weighted_a_star(s, puzzle_successors, lambda u: u == GOAL8, puzzle_h, w)
                self.assertEqual(r.path[-1], GOAL8)
                self.assertLessEqual(r.cost, w * d)
                if w == 1:
                    self.assertEqual(r.cost, d)


if __name__ == "__main__":
    unittest.main()
