# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jump-point-search/. The authors are listed in prov/RQYJH2.jsonl.

import heapq
import itertools
import random
import unittest

from jump_point_search import DIRECTIONS, Grid, expand, jump_point_search, octile, value


def grid_a_star(grid, start, goal):
    """Plain A* over all 8 moves, with the same corner rule. Return (cost pair or None, expansions)."""
    g = {start: (0, 0)}
    heap = [(octile(start, goal), 0, start)]
    closed = set()
    tie = 0
    while heap:
        _, _, u = heapq.heappop(heap)
        if u in closed:
            continue
        closed.add(u)
        if u == goal:
            return g[u], len(closed)
        a, b = g[u]
        for dx, dy in DIRECTIONS:
            if not grid.can_move(u[0], u[1], dx, dy):
                continue
            v = (u[0] + dx, u[1] + dy)
            new = (a, b + 1) if dx and dy else (a + 1, b)
            if v not in g or value(new) < value(g[v]):
                g[v] = new
                tie += 1
                heapq.heappush(heap, (value(new) + octile(v, goal), tie, v))
    return None, len(closed)


def random_grid(rng, w, h, density):
    return Grid(["".join("#" if rng.random() < density else "." for _ in range(w)) for _ in range(h)])


def free_cells(grid):
    return [(x, y) for y in range(grid.h) for x in range(grid.w) if grid.free(x, y)]


class Agreement(unittest.TestCase):
    def check(self, grid, s, t):
        path, cost, _ = jump_point_search(grid, s, t)
        ref, _ = grid_a_star(grid, s, t)
        self.assertEqual(cost, ref)
        if path is None:
            return
        cells = expand(path)
        self.assertEqual((cells[0], cells[-1]), (s, t))
        a = b = 0
        for (x0, y0), (x1, y1) in zip(cells, cells[1:]):
            dx, dy = x1 - x0, y1 - y0
            self.assertIn((dx, dy), DIRECTIONS)
            self.assertTrue(grid.can_move(x0, y0, dx, dy))
            if dx and dy:
                b += 1
            else:
                a += 1
        self.assertEqual((a, b), cost)

    def test_random_grids(self):
        rng = random.Random(80)
        for _ in range(400):
            w, h = rng.randint(1, 18), rng.randint(1, 18)
            grid = random_grid(rng, w, h, rng.choice((0.0, 0.1, 0.2, 0.3, 0.4)))
            cells = free_cells(grid)
            if not cells:
                continue
            for _ in range(3):
                self.check(grid, rng.choice(cells), rng.choice(cells))

    def test_rooms_and_corridors(self):
        """Long walls with gaps, where many paths have the same cost."""
        rng = random.Random(81)
        for _ in range(60):
            w, h = rng.randint(8, 30), rng.randint(8, 30)
            rows = [["."] * w for _ in range(h)]
            for _ in range(rng.randint(1, 4)):
                if rng.random() < 0.5:
                    x = rng.randrange(w)
                    for y in range(h):
                        rows[y][x] = "#"
                    for _ in range(rng.randint(1, 2)):
                        rows[rng.randrange(h)][x] = "."
                else:
                    y = rng.randrange(h)
                    for x in range(w):
                        rows[y][x] = "#"
                    for _ in range(rng.randint(1, 2)):
                        rows[y][rng.randrange(w)] = "."
            grid = Grid(["".join(r) for r in rows])
            cells = free_cells(grid)
            for _ in range(5):
                self.check(grid, rng.choice(cells), rng.choice(cells))

    def test_every_3_by_3_grid(self):
        for bits in itertools.product("#.", repeat=9):
            grid = Grid(["".join(bits[0:3]), "".join(bits[3:6]), "".join(bits[6:9])])
            cells = free_cells(grid)
            for s in cells:
                for t in cells:
                    self.check(grid, s, t)

    def test_page_example(self):
        grid = Grid(PAGE_ROWS)
        path, cost, expanded = jump_point_search(grid, (1, 3), (6, 3))
        self.assertEqual(path, PAGE_PATH)
        self.assertEqual(cost, PAGE_COST)
        self.assertEqual(expanded, PAGE_EXPANDED)
        self.assertEqual(grid_a_star(grid, (1, 3), (6, 3)), (PAGE_COST, PAGE_A_STAR_EXPANDED))

    def test_rejects_walls(self):
        with self.assertRaises(ValueError):
            jump_point_search(Grid(["#."]), (0, 0), (1, 0))


PAGE_ROWS = [
    "........",
    "........",
    "...#....",
    "...#....",
    "...#....",
    "........",
]
PAGE_PATH = [(1, 3), (2, 4), (2, 5), (4, 5), (6, 3)]
PAGE_COST = (3, 3)  # 3 + 3 sqrt(2)
PAGE_EXPANDED = 8
PAGE_A_STAR_EXPANDED = 16


def experiment(seed, maps=20, w=64, h=64, density=0.2):
    """Total expansions of JPS and of grid A* on random maps with reachable random pairs."""
    rng = random.Random(seed)
    jps = astar = done = 0
    while done < maps:
        grid = random_grid(rng, w, h, density)
        cells = free_cells(grid)
        s, t = rng.choice(cells), rng.choice(cells)
        cost, a = grid_a_star(grid, s, t)
        if cost is None:
            continue
        _, c2, j = jump_point_search(grid, s, t)
        assert c2 == cost
        jps += j
        astar += a
        done += 1
    return jps, astar


class Measured(unittest.TestCase):
    def test_experiment_numbers(self):
        """The numbers of the page: measurements, not guarantees."""
        self.assertEqual((experiment(8, density=0.05), experiment(8, density=0.2)), EXPECTED)


EXPECTED = ((878, 3455), (1246, 2430))

if __name__ == "__main__":
    unittest.main()
