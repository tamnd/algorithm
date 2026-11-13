# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-pathfinding-a-star/. The authors are listed in prov/XNV0WK.jsonl.

import random
import unittest
from collections import deque

from hierarchical_pathfinding_a_star import MOVES, SINGLE_LIMIT, HPAStar


def bfs_path(hpa, s, t):
    """A shortest grid path by breadth-first search on the whole grid, or None."""
    parent = {s: None}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        if u == t:
            path = [u]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            return path[::-1]
        for dx, dy in MOVES:
            v = (u[0] + dx, u[1] + dy)
            if v not in parent and hpa.free(*v):
                parent[v] = u
                queue.append(v)
    return None


def gap(hpa):
    """The largest distance from a position of an entrance to the nearest chosen transition."""
    worst = 0
    for run in hpa.entrances:
        chosen = [len(run) // 2] if len(run) < SINGLE_LIMIT else [0, len(run) - 1]
        worst = max(worst, max(min(abs(i - k) for k in chosen) for i in range(len(run))))
    return worst


def crossings(hpa, path):
    return sum(hpa.cluster(a) != hpa.cluster(b) for a, b in zip(path, path[1:]))


def random_rows(rng, w, h, density):
    return ["".join("#" if rng.random() < density else "." for _ in range(w)) for _ in range(h)]


def free_cells(hpa):
    return [(x, y) for y in range(hpa.h) for x in range(hpa.w) if hpa.free(x, y)]


class Paths(unittest.TestCase):
    def check(self, hpa, s, t):
        path, cost, _ = hpa.find_path(s, t)
        best = bfs_path(hpa, s, t)
        self.assertEqual(path is None, best is None)
        if path is None:
            return None
        self.assertEqual((path[0], path[-1]), (s, t))
        for a, b in zip(path, path[1:]):
            self.assertIn((b[0] - a[0], b[1] - a[1]), MOVES)
            self.assertTrue(hpa.free(*b))
        self.assertEqual(cost, len(path) - 1)
        opt = len(best) - 1
        self.assertGreaterEqual(cost, opt)
        self.assertLessEqual(cost, opt + 2 * gap(hpa) * crossings(hpa, best))  # the bound of the proof
        self.assertLessEqual(gap(hpa), max(SINGLE_LIMIT // 2 - 1, (hpa.c - 1) // 2))
        return cost, opt

    def test_random_grids(self):
        rng = random.Random(100)
        for _ in range(120):
            w, h = rng.randint(1, 30), rng.randint(1, 30)
            hpa = HPAStar(random_rows(rng, w, h, rng.choice((0.0, 0.1, 0.2, 0.3, 0.4))), rng.randint(2, 10))
            cells = free_cells(hpa)
            for _ in range(4):
                if cells:
                    self.check(hpa, rng.choice(cells), rng.choice(cells))

    def test_same_cluster_and_same_cell(self):
        hpa = HPAStar(["....", "....", "....", "...."], 4)
        self.assertEqual(hpa.find_path((1, 1), (1, 1))[:2], ([(1, 1)], 0))
        self.assertEqual(hpa.find_path((0, 0), (3, 0))[1], 3)

    def test_disconnected(self):
        hpa = HPAStar(["..#..", "..#..", "..#.."], 2)
        self.assertEqual(hpa.find_path((0, 0), (4, 2))[:2], (None, None))

    def test_page_example(self):
        hpa = HPAStar(PAGE_ROWS, 5)
        self.assertEqual(sorted(hpa.graph), PAGE_NODES)
        path, cost, expanded = hpa.find_path((0, 0), (9, 0))
        self.assertEqual(cost, PAGE_COST)
        self.assertEqual(len(bfs_path(hpa, (0, 0), (9, 0))) - 1, PAGE_OPT)
        self.assertEqual(path, PAGE_PATH)
        self.assertEqual(expanded, 4)
        self.assertEqual(cost, PAGE_OPT + 2 * gap(hpa) * 1)  # the bound of the proof is tight here

    def test_rejects_walls(self):
        with self.assertRaises(ValueError):
            HPAStar(["#."], 1).find_path((0, 0), (1, 0))


PAGE_ROWS = ["." * 10] * 10
PAGE_NODES = [(2, 4), (2, 5), (4, 2), (4, 7), (5, 2), (5, 7), (7, 4), (7, 5)]
PAGE_COST, PAGE_OPT = 13, 9
PAGE_PATH = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (9, 1), (9, 0)]


def experiment(seed, maps=10, w=60, h=60, density=0.2, queries=20):
    """Totals of the HPA* costs, the optimal costs, the abstract expansions and the abstract graph sizes."""
    rng = random.Random(seed)
    total = opt = expanded = nodes = 0
    for _ in range(maps):
        hpa = HPAStar(random_rows(rng, w, h, density), 10)
        nodes += len(hpa.graph)
        cells = free_cells(hpa)
        done = 0
        while done < queries:
            s, t = rng.choice(cells), rng.choice(cells)
            best = bfs_path(hpa, s, t)
            if best is None:
                continue
            _, cost, e = hpa.find_path(s, t)
            total += cost
            opt += len(best) - 1
            expanded += e
            done += 1
    return total, opt, expanded, nodes


class Measured(unittest.TestCase):
    def test_experiment_numbers(self):
        """The numbers of the page: measurements, not guarantees."""
        self.assertEqual(experiment(10), EXPECTED)


EXPECTED = (8193, 8005, 7176, 3276)

if __name__ == "__main__":
    unittest.main()
