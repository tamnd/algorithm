# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-expansion-a-star/. The authors are listed in prov/JA3VM9.jsonl.

import heapq
import random
import unittest
from collections import deque

from partial_expansion_a_star import partial_expansion_a_star

ALL = 10**9  # a cutoff so large that every child is stored: plain A*

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
    def test_table(self):
        adj = page_graph()
        want = {0: (7, 20, [6, 6, 7, 7, 7, 7]),
                1: (5, 14, [6, 6, 7, 7, 8, 7, 7]),
                ALL: (5, 14, [6, 6, 7, 8, 8, 7, 8, 7, 11, 7])}
        for C, row in want.items():
            r = partial_expansion_a_star("S", lambda u: adj[u], lambda u: u == "G", manhattan, C)
            self.assertEqual((r.path, r.cost), (["S", "B", "C", "G"], 7))
            self.assertEqual((r.expansions, r.generated, r.stored_f), row)

    def test_failure_and_trivial(self):
        adj = {0: [(1, 1)], 1: [(0, 1), (2, 2)], 2: [(1, 2)], 3: []}
        r = partial_expansion_a_star(0, lambda u: adj[u], lambda u: u == 3, lambda u: 0)
        self.assertIsNone(r.path)
        r = partial_expansion_a_star(3, lambda u: adj[u], lambda u: u == 3, lambda u: 0)
        self.assertEqual((r.path, r.cost), ([3], 0))


class TestOptimal(unittest.TestCase):
    def check(self, adj, s, t, h, C):
        r = partial_expansion_a_star(s, lambda u: adj[u], lambda u: u == t, h, C)
        dist = dijkstra(adj, s)
        if t not in dist:
            self.assertIsNone(r.path)
            return r
        check_path(self, adj, r.path, s, t, r.cost)
        self.assertEqual(r.cost, dist[t])
        if C == 0:
            self.assertLessEqual(max(r.stored_f), dist[t])  # no surplus node is stored
        return r

    def test_grids_consistent(self):
        rng = random.Random(18)
        for _ in range(200):
            adj = random_grid(rng, rng.randint(1, 9), rng.randint(1, 9), 0.25, 4)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            for C in (0, 1, 3, ALL):
                self.check(adj, s, t, lambda u: abs(u[0] - t[0]) + abs(u[1] - t[1]), C)

    def test_digraphs_admissible(self):
        rng = random.Random(19)
        for _ in range(300):
            n = rng.randint(2, 12)
            adj = random_digraph(rng, n, rng.uniform(0.1, 0.5), 6)
            t = rng.randrange(n)
            hs = dijkstra(reverse(adj), t)
            hv = [rng.randint(0, hs[u]) if u in hs else 100 for u in range(n)]
            s = rng.randrange(n)
            for C in (0, 2, ALL):
                self.check(adj, s, t, lambda u: hv[u], C)

    def test_eight_puzzle_stores_less(self):
        rng = random.Random(2024)
        stored = {0: 0, ALL: 0}
        expanded = {0: 0, ALL: 0}
        for _ in range(10):
            s = GOAL8
            for _ in range(40):
                s = rng.choice(puzzle_successors(s))[0]
            d = puzzle_bfs(s)
            for C in (0, ALL):
                r = partial_expansion_a_star(s, puzzle_successors, lambda u: u == GOAL8,
                                             puzzle_h, C)
                self.assertEqual(r.cost, d)
                stored[C] += len(r.stored_f)
                expanded[C] += r.expansions
        self.assertLess(stored[0], stored[ALL])  # fewer nodes stored
        self.assertGreater(expanded[0], expanded[ALL])  # more expansions


if __name__ == "__main__":
    unittest.main()
