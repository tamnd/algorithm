# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/limited-discrepancy-search/. The authors are listed in prov/Y4C1CW.jsonl.

import itertools
import random
import unittest
from collections import deque

from limited_discrepancy_search import ilds, lds, lds_path

# A node of a complete tree is a tuple of child indices from the root; index 0 is the
# child the heuristic prefers, so the number of nonzero entries is the discrepancy count.


def tree(branching, depth):
    def children(node):
        return [] if len(node) == depth else [node + (i,) for i in range(branching)]
    return children


def discrepancies(leaf):
    return sum(1 for x in leaf if x != 0)


def never(node):
    return False


class TestBinaryTreeEnumeration(unittest.TestCase):
    def test_lds_iteration_k_visits_leaves_with_at_most_k(self):
        for d in range(0, 8):
            r = lds((), tree(2, d), never, d)
            all_leaves = list(itertools.product((0, 1), repeat=d))
            for k in range(d + 1):
                got = r.leaves[k]
                self.assertEqual(len(got), len(set(got)))  # each leaf once
                want = {x for x in all_leaves if discrepancies(x) <= k}
                self.assertEqual(set(got), want)

    def test_lds_repeats(self):
        d = 6
        r = lds((), tree(2, d), never, d)
        seen = {}
        for part in r.leaves:
            for x in part:
                seen[x] = seen.get(x, 0) + 1
        for x, times in seen.items():
            self.assertEqual(times, d - discrepancies(x) + 1)

    def test_ilds_iteration_k_visits_leaves_with_exactly_k(self):
        for d in range(0, 8):
            r = ilds((), tree(2, d), never, d)
            all_leaves = list(itertools.product((0, 1), repeat=d))
            for k in range(d + 1):
                got = r.leaves[k]
                self.assertEqual(len(got), len(set(got)))
                self.assertEqual(set(got), {x for x in all_leaves if discrepancies(x) == k})

    def test_ilds_node_count(self):
        for d in range(0, 12):
            r = ilds((), tree(2, d), never, d)
            self.assertEqual(r.visited, sum(2**j * (d - j + 1) for j in range(d + 1)))
            self.assertEqual(r.visited, 2 ** (d + 2) - d - 3)
            self.assertLess(r.visited, 2 * (2 ** (d + 1) - 1))  # under twice one full DFS

    def test_lds_node_count_is_larger(self):
        for d in range(1, 11):
            a = lds((), tree(2, d), never, d).visited
            b = ilds((), tree(2, d), never, d).visited
            self.assertGreater(a, b)

    def test_ternary_tree(self):
        d = 4
        r = lds((), tree(3, d), never, d)
        all_leaves = list(itertools.product((0, 1, 2), repeat=d))
        for k in range(d + 1):
            self.assertEqual(sorted(r.leaves[k]),
                             sorted(x for x in all_leaves if discrepancies(x) <= k))
        r = ilds((), tree(3, d), never, d)
        for k in range(d + 1):
            self.assertEqual(sorted(r.leaves[k]),
                             sorted(x for x in all_leaves if discrepancies(x) == k))

    def test_goal_found_in_its_iteration(self):
        d = 7
        for goal in itertools.product((0, 1), repeat=d):
            for search in (lds, ilds):
                r = search((), tree(2, d), lambda n, g=goal: n == g, d)
                self.assertEqual(r.goal_path[-1], goal)
                self.assertEqual(r.iteration, discrepancies(goal))
                self.assertEqual(len(r.goal_path), d + 1)


class TestPageExample(unittest.TestCase):
    def test_order_of_iteration_one_and_two(self):
        r = lds((), tree(2, 3), never, 3)
        self.assertEqual(r.leaves[0], [(0, 0, 0)])
        self.assertEqual(r.leaves[1], [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)])
        r = ilds((), tree(2, 3), never, 3)
        self.assertEqual(r.leaves[1], [(0, 0, 1), (0, 1, 0), (1, 0, 0)])
        self.assertEqual(r.leaves[2], [(0, 1, 1), (1, 0, 1), (1, 1, 0)])


# ---------------------------------------------------------------- lds_path on graphs


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


def unit_grid(rng, w, hgt, wall):
    cells = {(x, y) for x in range(w) for y in range(hgt) if rng.random() >= wall}
    return {(x, y): [((x + dx, y + dy), 1) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                     if (x + dx, y + dy) in cells] for x, y in sorted(cells)}


class TestPaths(unittest.TestCase):
    def test_grids(self):
        rng = random.Random(13)
        for _ in range(150):
            adj = unit_grid(rng, rng.randint(1, 4), rng.randint(1, 4), 0.25)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            dist = bfs(adj, s)
            r = lds_path(s, lambda u: adj[u], lambda u: u == t,
                         lambda u: abs(u[0] - t[0]) + abs(u[1] - t[1]), len(adj) - 1)
            if t not in dist:
                self.assertIsNone(r.goal_path)
                continue
            p = r.goal_path
            self.assertIsNotNone(p)  # complete when the limits allow every simple path
            self.assertEqual((p[0], p[-1]), (s, t))
            self.assertEqual(len(p), len(set(p)))
            for u, v in zip(p, p[1:]):
                self.assertIn(v, [w for w, _ in adj[u]])
            self.assertGreaterEqual(len(p) - 1, dist[t])


if __name__ == "__main__":
    unittest.main()
