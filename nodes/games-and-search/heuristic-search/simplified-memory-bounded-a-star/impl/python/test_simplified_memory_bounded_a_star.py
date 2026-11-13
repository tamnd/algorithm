# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplified-memory-bounded-a-star/. The authors are listed in prov/S5JTNJ.jsonl.

import heapq
import random
import unittest
from collections import deque

from simplified_memory_bounded_a_star import sma_star

INF = float("inf")

# ---------------------------------------------------------------- oracles and generators


def dijkstra(adj, src):
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


def limited_cost(adj, s, t, k):
    """Independent oracle: least cost of a path from s to t with at most k actions.

    Bellman-Ford rounds. With positive costs a cheapest walk of at most k actions
    has no cycle, so this is also the least cost of a simple path.
    """
    best = {s: 0}
    out = 0 if s == t else INF
    for _ in range(k):
        nxt = dict(best)
        for u, d in best.items():
            for v, c in adj[u]:
                if d + c < nxt.get(v, INF):
                    nxt[v] = d + c
        best = nxt
        out = min(out, best.get(t, INF))
    return out


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
        want = {2: (None, None), 3: (None, None), 4: (7, 10, 7), 5: (7, 9, 5),
                6: (7, 9, 4), 8: (7, 9, 2)}
        for M, row in want.items():
            r = sma_star("S", lambda u: adj[u], lambda u: u == "G", manhattan, M)
            self.assertLessEqual(r.peak, M)
            if row[0] is None:
                self.assertIsNone(r.path)
                self.assertEqual(limited_cost(adj, "S", "G", M - 1), INF)
            else:
                self.assertEqual((r.cost, r.steps, r.deletions), row)
                self.assertEqual(r.path, ["S", "B", "C", "G"])

    def test_bad_memory(self):
        with self.assertRaises(ValueError):
            sma_star(0, lambda u: [], lambda u: True, lambda u: 0, 1)


class TestLimitedOptimal(unittest.TestCase):
    def check(self, adj, s, t, h, M):
        r = sma_star(s, lambda u: adj[u], lambda u: u == t, h, M)
        want = limited_cost(adj, s, t, M - 1)
        self.assertLessEqual(r.peak, M)
        if want == INF:
            self.assertIsNone(r.path)
        else:
            check_path(self, adj, r.path, s, t, r.cost)
            self.assertEqual(r.cost, want)
        return r

    def test_digraphs(self):
        rng = random.Random(12)
        for _ in range(250):
            n = rng.randint(2, 8)
            adj = random_digraph(rng, n, rng.uniform(0.15, 0.5), 6)
            t = rng.randrange(n)
            hs = dijkstra(reverse(adj), t)
            hv = [rng.randint(0, hs[u]) if u in hs else 100 for u in range(n)]
            s = rng.randrange(n)
            for M in (2, 3, 4, 6, 9):
                self.check(adj, s, t, lambda u: hv[u], M)

    def test_grids(self):
        rng = random.Random(14)
        for _ in range(100):
            adj = random_grid(rng, rng.randint(1, 4), rng.randint(1, 4), 0.25, 4)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            dist = dijkstra(adj, s)
            for M in (3, 5, 8, len(adj) + 1):
                r = self.check(adj, s, t, lambda u: abs(u[0] - t[0]) + abs(u[1] - t[1]), M)
                if M == len(adj) + 1 and t in dist:
                    self.assertEqual(r.cost, dist[t])  # memory enough for any simple path

    def test_eight_puzzle(self):
        rng = random.Random(2024)
        for _ in range(4):
            s = GOAL8
            for _ in range(30):
                s = rng.choice(puzzle_successors(s))[0]
            d = puzzle_bfs(s)
            for M in (d + 1, 2 * d + 2, 100):
                r = sma_star(s, puzzle_successors, lambda u: u == GOAL8, puzzle_h, M)
                self.assertEqual(r.cost, d)
                self.assertLessEqual(r.peak, M)
            if d >= 2:
                r = sma_star(s, puzzle_successors, lambda u: u == GOAL8, puzzle_h, d)
                self.assertIsNone(r.path)  # d actions need d + 1 nodes


if __name__ == "__main__":
    unittest.main()
