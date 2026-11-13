# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a-star-search/. The authors are listed in prov/6K9J0E.jsonl.

import heapq
import random
import unittest
from collections import deque
from fractions import Fraction

from a_star_search import a_star_search, effective_branching_factor

INF = 10**9  # h of a state that cannot reach the goal; larger than any C* here

# ---------------------------------------------------------------- oracles


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
    radj = {u: [] for u in adj}
    for u in adj:
        for v, c in adj[u]:
            radj[v].append((u, c))
    return radj


def bfs(adj, src):
    dist = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        for v, _ in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def random_digraph(rng, n, p, cmax):
    adj = {u: [] for u in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < p:
                adj[u].append((v, rng.randint(1, cmax)))
    return adj


def random_grid(rng, w, hgt, wall, cmax):
    """4-connected grid; entering cell v costs cost[v] in 1 .. cmax."""
    cells = [(x, y) for x in range(w) for y in range(hgt) if rng.random() >= wall]
    cost = {v: rng.randint(1, cmax) for v in cells}
    adj = {v: [] for v in cells}
    for x, y in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            m = (x + dx, y + dy)
            if m in cost:
                adj[(x, y)].append((m, cost[m]))
    return adj, cost


def run(adj, s, t, h, **kw):
    return a_star_search(s, lambda u: adj[u], lambda u: u == t, h, **kw)


def path_cost(adj, path):
    total = 0
    for u, v in zip(path, path[1:]):
        total += min(c for w, c in adj[u] if w == v)
    return total


def perfect(adj, t):
    hstar = dijkstra(reverse(adj), t)
    return lambda u: hstar.get(u, INF), hstar


# ---------------------------------------------------------------- the page example

POS = {"S": (0, 0), "A": (2, 0), "B": (0, 2), "C": (2, 2), "D": (4, 0), "E": (0, 4), "F": (-1, 0), "G": (4, 2)}
EDGES = [("S", "A", 2), ("S", "B", 3), ("A", "C", 4), ("A", "D", 3), ("B", "C", 2), ("B", "E", 2), ("C", "G", 2), ("D", "G", 3), ("S", "F", 1)]


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


# The counterexample of the page: admissible, not consistent at A -> B.
CE = {"S": [("A", 1), ("B", 3)], "A": [("B", 1)], "B": [("C", 1)], "C": [("G", 1)], "G": []}
CE_H = {"S": 0, "A": 3, "B": 0, "C": 0, "G": 0}


class TestPageExample(unittest.TestCase):
    def test_trace(self):
        r = run(page_graph(), "S", "G", manhattan)
        self.assertEqual(r.path, ["S", "B", "C", "G"])
        self.assertEqual(r.cost, 7)
        self.assertEqual(r.expanded, ["S", "A", "D", "B", "C"])
        self.assertEqual(r.popped_f, [6, 6, 7, 7, 7])
        self.assertEqual(r.reopenings, 0)

    def test_dijkstra_case(self):
        r = run(page_graph(), "S", "G", lambda u: 0)
        self.assertEqual(r.cost, 7)
        self.assertEqual(r.expanded, ["S", "F", "A", "B", "D", "C", "E"])

    def test_manhattan_is_consistent_here(self):
        for u, v, c in EDGES:
            self.assertLessEqual(abs(manhattan(u) - manhattan(v)), c)

    def test_start_is_goal(self):
        r = run(page_graph(), "G", "G", manhattan)
        self.assertEqual((r.path, r.cost, r.expansions), (["G"], 0, 0))

    def test_unreachable(self):
        adj = {0: [(1, 1)], 1: [], 2: []}
        r = run(adj, 0, 2, lambda u: 0)
        self.assertIsNone(r.path)
        self.assertEqual(r.expanded, [0, 1])


class TestInconsistentCounterexample(unittest.TestCase):
    def test_heuristic_is_admissible_not_consistent(self):
        hstar = dijkstra(reverse(CE), "G")
        self.assertEqual(hstar, {"G": 0, "C": 1, "B": 2, "A": 3, "S": 4})
        self.assertTrue(all(CE_H[u] <= hstar[u] for u in CE))
        self.assertGreater(CE_H["A"], 1 + CE_H["B"])

    def test_without_reopening_is_suboptimal(self):
        r = run(CE, "S", "G", CE_H.get, reopen=False)
        self.assertEqual((r.path, r.cost), (["S", "B", "C", "G"], 5))
        self.assertEqual(r.expanded, ["S", "B", "C", "A"])

    def test_with_reopening_is_optimal(self):
        r = run(CE, "S", "G", CE_H.get)
        self.assertEqual((r.path, r.cost), (["S", "A", "B", "C", "G"], 4))
        self.assertEqual(r.expanded, ["S", "B", "C", "A", "B", "C"])
        self.assertEqual(r.popped_f, [0, 3, 4, 4, 2, 3])
        self.assertEqual(r.reopenings, 2)

    def test_pathmax_on_the_counterexample(self):
        r = run(CE, "S", "G", CE_H.get, pathmax=True)
        self.assertEqual(r.cost, 4)
        self.assertEqual(r.popped_f, [0, 3, 4, 4, 4, 4])
        self.assertEqual(r.reopenings, 2)  # pathmax does not stop reopening
        r2 = run(CE, "S", "G", CE_H.get, pathmax=True, reopen=False)
        self.assertEqual(r2.cost, 5)  # nor does it make a closed list safe


class TestAgainstDijkstra(unittest.TestCase):
    def test_random_digraphs_consistent(self):
        rng = random.Random(2024)
        for _ in range(300):
            n = rng.randint(2, 25)
            adj = random_digraph(rng, n, rng.uniform(0.05, 0.4), 9)
            s, t = rng.randrange(n), rng.randrange(n)
            dist = dijkstra(adj, s)
            _, hstar = perfect(adj, t)
            for k in range(5):  # h_k = floor(k h* / 4) is consistent
                r = run(adj, s, t, lambda u: (k * hstar[u]) // 4 if u in hstar else INF)
                self.assertEqual(r.cost, dist.get(t))
                self.assertEqual(r.reopenings, 0)
                if r.path is not None:
                    self.assertEqual(path_cost(adj, r.path), r.cost)
                    self.assertEqual((r.path[0], r.path[-1]), (s, t))

    def test_random_grids(self):
        rng = random.Random(7)
        for _ in range(150):
            w, hg = rng.randint(1, 9), rng.randint(1, 9)
            adj, cost = random_grid(rng, w, hg, 0.25, 5)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            dist = dijkstra(adj, s)
            cmin = min(cost.values())
            r = run(adj, s, t, lambda u: cmin * (abs(u[0] - t[0]) + abs(u[1] - t[1])))
            self.assertEqual(r.cost, dist.get(t))
            self.assertEqual(r.reopenings, 0)

    def test_unit_grids_against_bfs(self):
        rng = random.Random(11)
        for _ in range(150):
            adj, cost = random_grid(rng, rng.randint(1, 10), rng.randint(1, 10), 0.3, 1)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            r = run(adj, s, t, lambda u: abs(u[0] - t[0]) + abs(u[1] - t[1]))
            self.assertEqual(r.cost, bfs(adj, s).get(t))

    def test_inconsistent_with_reopening_is_optimal(self):
        rng = random.Random(99)
        found_suboptimal = 0
        for _ in range(400):
            n = rng.randint(3, 15)
            adj = random_digraph(rng, n, rng.uniform(0.1, 0.5), 9)
            s, t = rng.randrange(n), rng.randrange(n)
            _, hstar = perfect(adj, t)
            hr = {u: (rng.randint(0, hstar[u]) if u in hstar else INF) for u in adj}
            want = dijkstra(adj, s).get(t)
            r = run(adj, s, t, hr.get)
            self.assertEqual(r.cost, want)
            rp = run(adj, s, t, hr.get, pathmax=True)
            self.assertEqual(rp.cost, want)
            self.assertEqual(rp.popped_f, sorted(rp.popped_f))  # pathmax: monotone f
            nr = run(adj, s, t, hr.get, reopen=False)
            if want is None:
                self.assertIsNone(nr.cost)
            else:
                self.assertGreaterEqual(nr.cost, want)
                found_suboptimal += nr.cost > want
        self.assertGreater(found_suboptimal, 0)


class TestDominance(unittest.TestCase):
    def test_surely_expanded_sets(self):
        """Consistent h: A* expands every n with g*(n) + h(n) < C* and none with > C*."""
        rng = random.Random(5)
        for _ in range(200):
            n = rng.randint(2, 25)
            adj = random_digraph(rng, n, rng.uniform(0.1, 0.4), 9)
            s, t = rng.randrange(n), rng.randrange(n)
            dist = dijkstra(adj, s)
            if t not in dist:
                continue
            cstar = dist[t]
            _, hstar = perfect(adj, t)
            prev = None
            for k in range(5):
                hk = {u: ((k * hstar[u]) // 4 if u in hstar else INF) for u in adj}
                ex = set(run(adj, s, t, hk.get).expanded)
                below = {u for u in dist if dist[u] + hk[u] < cstar}
                above = {u for u in dist if dist[u] + hk[u] > cstar}
                self.assertLessEqual(below, ex)
                self.assertFalse(ex & above)
                if prev is not None:
                    self.assertLessEqual(below, prev)  # h_k >= h_(k-1): fewer sure nodes
                prev = below

    def test_strict_dominance_gives_subset(self):
        """Admissible h2 > h1 off the goal: A*(h2) expands a subset of A*(h1)."""
        rng = random.Random(6)
        for _ in range(300):
            n = rng.randint(2, 20)
            adj = random_digraph(rng, n, rng.uniform(0.1, 0.5), 9)
            s, t = rng.randrange(n), rng.randrange(n)
            _, hstar = perfect(adj, t)
            if t not in dijkstra(adj, s):
                continue
            h1 = {u: (rng.randint(0, (hstar[u] - 1) // 2) if u in hstar and u != t else (0 if u == t else INF)) for u in adj}
            h2 = {u: (rng.randint(h1[u] + 1, hstar[u]) if u in hstar and u != t else h1[u]) for u in adj}
            e1 = set(run(adj, s, t, h1.get).expanded)
            e2 = set(run(adj, s, t, h2.get).expanded)
            self.assertLessEqual(e2, e1)

    def test_page_counts(self):
        """The counts of the page: h = 0, Manhattan, and the perfect h*."""
        adj = page_graph()
        hp, _ = perfect(adj, "G")
        counts = [run(adj, "S", "G", hf).expansions for hf in (lambda u: 0, manhattan, hp)]
        self.assertEqual(counts, [7, 5, 3])

    def test_non_strict_dominance_can_lose_on_ties(self):
        """The tie example of the dominance page: h2 >= h1, both consistent, h2 expands more."""
        adj = {"S": [("P", 1), ("X", 2)], "P": [("G", 3)], "X": [("G", 10)], "G": []}
        h1 = {"S": 3, "P": 2, "X": 2, "G": 0}
        h2 = {"S": 4, "P": 3, "X": 2, "G": 0}
        for h in (h1, h2):
            self.assertTrue(all(h[u] <= c + h[v] for u in adj for v, c in adj[u]))
        r1 = a_star_search("S", lambda u: adj[u], lambda u: u == "G", h1.get)
        r2 = a_star_search("S", lambda u: adj[u], lambda u: u == "G", h2.get)
        self.assertEqual((r1.cost, r1.expanded), (4, ["S", "P"]))
        self.assertEqual((r2.cost, r2.expanded), (4, ["S", "X", "P"]))

    def test_max_of_admissible_is_admissible_and_dominates(self):
        rng = random.Random(8)
        for _ in range(200):
            n = rng.randint(2, 15)
            adj = random_digraph(rng, n, 0.3, 9)
            s, t = rng.randrange(n), rng.randrange(n)
            _, hstar = perfect(adj, t)
            ha = {u: (rng.randint(0, hstar[u]) if u in hstar else INF) for u in adj}
            hb = {u: (rng.randint(0, hstar[u]) if u in hstar else INF) for u in adj}
            hm = {u: max(ha[u], hb[u]) for u in adj}
            self.assertTrue(all(hm[u] <= hstar[u] for u in hstar))
            self.assertEqual(run(adj, s, t, hm.get).cost, dijkstra(adj, s).get(t))


class TestEffectiveBranchingFactor(unittest.TestCase):
    @staticmethod
    def total(b, d):
        return sum(b**i for i in range(d + 1))

    def test_textbook_case(self):
        tol = Fraction(1, 10**6)
        b = effective_branching_factor(52, 5, tol)
        self.assertLess(self.total(b - tol, 5), 53)
        self.assertGreater(self.total(b + tol, 5), 53)
        self.assertEqual(round(float(b), 2), 1.92)

    def test_chain_gives_one(self):
        for d in range(1, 8):
            self.assertEqual(effective_branching_factor(d, d), 1)

    def test_uniform_trees(self):
        tol = Fraction(1, 10**9)
        for b in range(2, 6):
            for d in range(1, 7):
                n = sum(b**i for i in range(1, d + 1))
                self.assertLessEqual(abs(effective_branching_factor(n, d, tol) - b), tol)

    def test_bracket_on_random_inputs(self):
        rng = random.Random(3)
        tol = Fraction(1, 10**5)
        for _ in range(100):
            d = rng.randint(1, 12)
            n = rng.randint(d, 10**6)
            b = effective_branching_factor(n, d, tol)
            lo, hi = max(b - tol, Fraction(0)), b + tol
            self.assertLessEqual(self.total(lo, d), n + 1)
            self.assertGreaterEqual(self.total(hi, d), n + 1)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            effective_branching_factor(3, 5)
        with self.assertRaises(ValueError):
            effective_branching_factor(3, 0)


if __name__ == "__main__":
    unittest.main()
