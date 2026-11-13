# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxation-heuristic/. The authors are listed in prov/2WVNT9.jsonl.

import heapq
import random
import unittest

from relaxation_heuristic import (
    gaschnig,
    goal_board,
    grid_manhattan,
    grid_octile,
    jump_into_blank_moves,
    manhattan_distance,
    misplaced_tiles,
    puzzle_moves,
    relaxed_distances,
)

EPS = 1e-9


def random_grid(rng: random.Random, w: int, h: int, p: float) -> list[list[bool]]:
    """True means blocked."""
    return [[rng.random() < p for _ in range(w)] for _ in range(h)]


def grid_moves(grid, cell, eight: bool):
    """4- or 8-connected moves. A diagonal move needs both side cells free (no corner cutting)."""
    h, w = len(grid), len(grid[0])
    x, y = cell
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if eight:
        steps += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dx, dy in steps:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < w and 0 <= ny < h) or grid[ny][nx]:
            continue
        if dx and dy and (grid[y][nx] or grid[ny][x]):
            continue
        yield (nx, ny), (2 ** 0.5 if dx and dy else 1.0)


def dijkstra_to(grid, goal, eight):
    """Exact distances to goal (the moves are symmetric)."""
    dist = {goal: 0.0}
    pq = [(0.0, goal)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, c in grid_moves(grid, u, eight):
            if d + c < dist.get(v, float("inf")) - EPS:
                dist[v] = d + c
                heapq.heappush(pq, (d + c, v))
    return dist


class EightPuzzle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.goal = goal_board(3, 3)
        cls.dist = relaxed_distances([cls.goal], lambda b: puzzle_moves(b, 3, 3))

    def heuristics(self):
        g = self.goal
        return {
            "misplaced": lambda b: misplaced_tiles(b, g),
            "manhattan": lambda b: manhattan_distance(b, g, 3),
            "gaschnig": lambda b: gaschnig(b, g),
            "max": lambda b: max(manhattan_distance(b, g, 3), gaschnig(b, g)),
        }

    def test_reachable_count(self):
        self.assertEqual(len(self.dist), 181440)
        self.assertEqual(max(self.dist.values()), 31)

    def test_admissible_on_every_state(self):
        for name, h in self.heuristics().items():
            for b, d in self.dist.items():
                self.assertLessEqual(h(b), d, (name, b))
            self.assertEqual(h(self.goal), 0)

    def test_consistent_on_sampled_states(self):
        rng = random.Random(7)
        sample = rng.sample(sorted(self.dist), 15000)
        for name, h in self.heuristics().items():
            for b in sample:
                hb = h(b)
                for nb in puzzle_moves(b, 3, 3):
                    self.assertLessEqual(hb, 1 + h(nb), (name, b, nb))

    def test_dominance(self):
        g = self.goal
        gas_wins = man_wins = 0
        for b in self.dist:
            m, a, s = manhattan_distance(b, g, 3), misplaced_tiles(b, g), gaschnig(b, g)
            self.assertGreaterEqual(m, a)
            self.assertGreaterEqual(s, a)
            gas_wins += s > m
            man_wins += m > s
        self.assertEqual((gas_wins, man_wins), (304, 177591))

    def test_page_examples(self):
        g = self.goal
        b = (1, 2, 3, 5, 4, 6, 8, 7, 0)
        self.assertEqual((misplaced_tiles(b, g), manhattan_distance(b, g, 3), gaschnig(b, g), self.dist[b]), (4, 4, 6, 14))
        b = (5, 1, 3, 4, 0, 2, 7, 8, 6)
        self.assertEqual((misplaced_tiles(b, g), manhattan_distance(b, g, 3), gaschnig(b, g), self.dist[b]), (4, 6, 4, 12))


class ClosedFormsEqualRelaxedSearch(unittest.TestCase):
    """Each closed form is the exact cost of its relaxed problem."""

    def test_gaschnig_is_jump_distance(self):
        for rows, cols in ((2, 2), (2, 3), (2, 4)):
            g = goal_board(rows, cols)
            d = relaxed_distances([g], jump_into_blank_moves)
            n = rows * cols
            self.assertEqual(len(d), {4: 24, 6: 720, 8: 40320}[n])
            for b, v in d.items():
                self.assertEqual(gaschnig(b, g), v, b)

    def tile_space(self, rows, cols, adjacent_only):
        """Relaxed space: tiles move one at a time and may share squares."""
        n = rows * cols
        k = n - 1

        def moves(pos):
            for t in range(k):
                p = pos[t]
                if adjacent_only:
                    r, c = divmod(p, cols)
                    targets = [rr * cols + cc for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)) if 0 <= rr < rows and 0 <= cc < cols]
                else:
                    targets = [q for q in range(n) if q != p]
                for q in targets:
                    yield pos[:t] + (q,) + pos[t + 1:]

        goal_pos = tuple(range(k))
        return relaxed_distances([goal_pos], moves)

    def test_misplaced_and_manhattan_are_tile_space_distances(self):
        rows, cols = 2, 3
        g = goal_board(rows, cols)
        free = self.tile_space(rows, cols, adjacent_only=False)
        step = self.tile_space(rows, cols, adjacent_only=True)
        self.assertEqual(len(free), 6 ** 5)
        rng = random.Random(3)
        for _ in range(400):
            b = list(range(6))
            rng.shuffle(b)
            b = tuple(b)
            pos = tuple(b.index(t) for t in range(1, 6))
            self.assertEqual(misplaced_tiles(b, g), free[pos])
            self.assertEqual(manhattan_distance(b, g, cols), step[pos])


class Grids(unittest.TestCase):
    def test_manhattan_on_4_connected_grids(self):
        rng = random.Random(11)
        for _ in range(30):
            grid = random_grid(rng, 12, 9, 0.25)
            free = [(x, y) for y in range(9) for x in range(12) if not grid[y][x]]
            goal = rng.choice(free)
            dist = dijkstra_to(grid, goal, eight=False)
            for u, du in dist.items():
                hu = grid_manhattan(u, goal)
                self.assertLessEqual(hu, du + EPS)
                for v, c in grid_moves(grid, u, eight=False):
                    self.assertLessEqual(hu, c + grid_manhattan(v, goal) + EPS)

    def test_octile_on_8_connected_grids(self):
        rng = random.Random(12)
        for _ in range(30):
            grid = random_grid(rng, 12, 9, 0.25)
            free = [(x, y) for y in range(9) for x in range(12) if not grid[y][x]]
            goal = rng.choice(free)
            dist = dijkstra_to(grid, goal, eight=True)
            for u, du in dist.items():
                hu = grid_octile(u, goal)
                self.assertLessEqual(hu, du + EPS)
                for v, c in grid_moves(grid, u, eight=True):
                    self.assertLessEqual(hu, c + grid_octile(v, goal) + EPS)

    def test_octile_is_exact_without_obstacles(self):
        grid = [[False] * 8 for _ in range(6)]
        dist = dijkstra_to(grid, (0, 0), eight=True)
        for u, du in dist.items():
            self.assertAlmostEqual(grid_octile(u, (0, 0)), du)


if __name__ == "__main__":
    unittest.main()
