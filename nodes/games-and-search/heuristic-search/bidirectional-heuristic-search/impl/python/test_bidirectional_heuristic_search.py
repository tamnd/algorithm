# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bidirectional-heuristic-search/. The authors are listed in prov/C7VG9R.jsonl.

import heapq
import random
import unittest
from collections import deque
from fractions import Fraction

from bidirectional_heuristic_search import mm_search

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


def check_path(test, adj, path, s, t, cost):
    test.assertEqual((path[0], path[-1]), (s, t))
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


def puzzle_h_to(target):
    where = {v: i for i, v in enumerate(target)}

    def h(s):
        return sum(abs(i // 3 - where[v] // 3) + abs(i % 3 - where[v] % 3)
                   for i, v in enumerate(s) if v)
    return h


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


def manhattan(u, t="G"):
    return abs(POS[u][0] - POS[t][0]) + abs(POS[u][1] - POS[t][1])


class TestPageExample(unittest.TestCase):
    def test_trace(self):
        adj = page_graph()
        for eps in (0, 1):
            r = mm_search("S", "G", lambda u: adj[u], lambda u: adj[u], manhattan,
                          lambda u: manhattan(u, "S"), eps)
            self.assertEqual((r.path, r.cost), (["S", "B", "C", "G"], 7))
            self.assertEqual((r.expanded_f, r.gs_f), (["S", "A"], [0, 2]))
            self.assertEqual((r.expanded_b, r.gs_b), (["G", "C"], [0, 2]))

    def test_failure_and_trivial(self):
        adj = {0: [(1, 1)], 1: [(0, 1)], 2: [(3, 1)], 3: []}
        rev = reverse(adj)
        r = mm_search(0, 3, lambda u: adj[u], lambda u: rev[u], lambda u: 0, lambda u: 0, 1)
        self.assertIsNone(r.path)
        r = mm_search(2, 2, lambda u: adj[u], lambda u: rev[u], lambda u: 0, lambda u: 0, 1)
        self.assertEqual((r.path, r.cost), ([2], 0))


class TestOptimal(unittest.TestCase):
    def check(self, adj, s, t, hf, hb, eps):
        rev = reverse(adj)
        r = mm_search(s, t, lambda u: adj[u], lambda u: rev[u], hf, hb, eps)
        dist = dijkstra(adj, s)
        if t not in dist:
            self.assertIsNone(r.path)
            return r
        best = dist[t]
        check_path(self, adj, r.path, s, t, r.cost)
        self.assertEqual(r.cost, best)
        # meet in the middle: no expansion has g > C*/2 or f > C*
        for n, g in zip(r.expanded_f, r.gs_f):
            self.assertLessEqual(2 * g, best)
            self.assertLessEqual(g + hf(n), best)
        for n, g in zip(r.expanded_b, r.gs_b):
            self.assertLessEqual(2 * g, best)
            self.assertLessEqual(g + hb(n), best)
        return r

    def test_grids_consistent(self):
        rng = random.Random(22)
        for _ in range(200):
            adj = random_grid(rng, rng.randint(1, 9), rng.randint(1, 9), 0.25, 4)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            for eps in (0, 1):
                self.check(adj, s, t, lambda u: abs(u[0] - t[0]) + abs(u[1] - t[1]),
                           lambda u: abs(u[0] - s[0]) + abs(u[1] - s[1]), eps)

    def test_digraphs_admissible(self):
        rng = random.Random(23)
        for _ in range(400):
            n = rng.randint(2, 12)
            adj = random_digraph(rng, n, rng.uniform(0.1, 0.5), 6)
            s, t = rng.randrange(n), rng.randrange(n)
            to_t = dijkstra(reverse(adj), t)
            from_s = dijkstra(adj, s)
            hf = [rng.randint(0, to_t[u]) if u in to_t else 100 for u in range(n)]
            hb = [rng.randint(0, from_s[u]) if u in from_s else 100 for u in range(n)]
            for eps in (0, 1):
                self.check(adj, s, t, lambda u: hf[u], lambda u: hb[u], eps)

    def test_fraction_costs_blind(self):
        rng = random.Random(24)
        for _ in range(100):
            n = rng.randint(2, 10)
            adj = {u: [(v, Fraction(c, 3)) for v, c in nb]
                   for u, nb in random_digraph(rng, n, 0.3, 9).items()}
            self.check(adj, 0, n - 1, lambda u: 0, lambda u: 0, Fraction(1, 3))

    def test_eight_puzzle(self):
        rng = random.Random(2024)
        for _ in range(6):
            s = GOAL8
            for _ in range(40):
                s = rng.choice(puzzle_successors(s))[0]
            r = mm_search(s, GOAL8, puzzle_successors, puzzle_successors,
                          puzzle_h_to(GOAL8), puzzle_h_to(s), 1)
            self.assertEqual(r.cost, puzzle_bfs(s))
            self.assertTrue(all(2 * g <= r.cost for g in r.gs_f + r.gs_b))


if __name__ == "__main__":
    unittest.main()
