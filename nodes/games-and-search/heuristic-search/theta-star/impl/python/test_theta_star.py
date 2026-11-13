# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/theta-star/. The authors are listed in prov/1ZY6ZC.jsonl.

import heapq
import math
import random
import unittest
from fractions import Fraction

from theta_star import NEIGHBOURS, Grid, dist, line_of_sight, theta_star

EPS = 1e-9


def exact_sight(grid, a, b):
    """Line of sight by exact rational traversal, written apart from the one in theta_star.

    The breakpoints are the parameters where the segment crosses a grid line.
    Between two breakpoints the segment stays in one open cell or on one open
    unit edge, so testing the midpoints and the breakpoints is enough.
    """
    (x0, y0), (x1, y1) = a, b
    ts = {Fraction(0), Fraction(1)}
    for k in range(min(x0, x1), max(x0, x1) + 1):
        if x1 != x0:
            ts.add(Fraction(k - x0, x1 - x0))
    for k in range(min(y0, y1), max(y0, y1) + 1):
        if y1 != y0:
            ts.add(Fraction(k - y0, y1 - y0))
    ts = sorted(ts)
    points = list(ts) + [(u + v) / 2 for u, v in zip(ts, ts[1:])]
    for t in points:
        px, py = x0 + t * (x1 - x0), y0 + t * (y1 - y0)
        if inside_obstacle(grid, px, py):
            return False
    return True


def inside_obstacle(grid, px, py):
    """True if the point is in the interior of the union of blocked cells."""
    fx, fy = math.floor(px), math.floor(py)
    xs = [fx - 1, fx] if px == fx else [fx]  # the cells whose closed square holds the point
    ys = [fy - 1, fy] if py == fy else [fy]
    return all(grid.blocked(i, j) for i in xs for j in ys)


def corners(grid):
    return [(x, y) for y in range(grid.h + 1) for x in range(grid.w + 1)]


def dijkstra(adj, s, t):
    d = {s: 0.0}
    pq = [(0.0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue
        if u == t:
            return du
        for v, c in adj(u):
            if du + c < d.get(v, math.inf):
                d[v] = du + c
                heapq.heappush(pq, (du + c, v))
    return None


def grid_length(grid, s, t):
    """Shortest path along the 8-connected corner graph (the path of A* on the grid)."""

    def adj(u):
        for dx, dy in NEIGHBOURS:
            v = (u[0] + dx, u[1] + dy)
            if grid.corner(*v) and line_of_sight(grid, u, v):
                yield v, dist(u, v)

    return dijkstra(adj, s, t)


def visibility_length(grid, s, t):
    """The true shortest length in the plane: Dijkstra on the visibility graph.

    A shortest path bends only at corners of the obstacle, so the nodes are s, t
    and the corners that touch a blocked cell. The sight test is the one of
    theta_star, which test_line_of_sight_matches_exact_traversal checks.
    """
    cs = [c for c in corners(grid) if any(grid.blocked(c[0] - i, c[1] - j) for i in (0, 1) for j in (0, 1))]
    cs = sorted(set(cs) | {s, t})
    seen = {}

    def adj(u):
        for v in cs:
            if v != u:
                key = (min(u, v), max(u, v))
                if key not in seen:
                    seen[key] = line_of_sight(grid, u, v)
                if seen[key]:
                    yield v, dist(u, v)

    return dijkstra(adj, s, t)


def random_grid(rng, w, h, density):
    return Grid(["".join("#" if rng.random() < density else "." for _ in range(w)) for _ in range(h)])


class Sight(unittest.TestCase):
    def test_line_of_sight_matches_exact_traversal(self):
        rng = random.Random(90)
        for _ in range(300):
            grid = random_grid(rng, rng.randint(1, 9), rng.randint(1, 9), rng.choice((0.1, 0.3, 0.5)))
            cs = corners(grid)
            for _ in range(20):
                a, b = rng.choice(cs), rng.choice(cs)
                if a == b:  # Theta* never tests a segment of length 0
                    continue
                self.assertEqual(line_of_sight(grid, a, b), exact_sight(grid, a, b), (grid.rows, a, b))

    def test_squeeze_and_shared_edges(self):
        grid = Grid(["#.", ".#"])
        self.assertTrue(line_of_sight(grid, (0, 2), (2, 0)))  # through the touching corner
        self.assertFalse(line_of_sight(grid, (0, 0), (2, 2)))
        walls = Grid(["##", ".."])
        self.assertFalse(line_of_sight(walls, (0, 0), (2, 0)))  # along the border of a blocked row
        self.assertTrue(line_of_sight(walls, (0, 1), (2, 1)))  # along the lower side of the walls


class Paths(unittest.TestCase):
    def check(self, grid, s, t):
        path, length = theta_star(grid, s, t)
        vis = visibility_length(grid, s, t)
        ref = grid_length(grid, s, t)
        self.assertEqual(path is None, ref is None)
        self.assertEqual(vis is None, ref is None)
        if path is None:
            return None
        self.assertEqual((path[0], path[-1]), (s, t))
        for a, b in zip(path, path[1:]):
            self.assertTrue(exact_sight(grid, a, b))
        self.assertAlmostEqual(sum(dist(a, b) for a, b in zip(path, path[1:])), length, delta=EPS)
        self.assertGreaterEqual(length, vis - EPS)  # no path in the plane is shorter than the optimum
        return length, ref, vis

    def test_random_grids(self):
        rng = random.Random(91)
        for _ in range(250):
            grid = random_grid(rng, rng.randint(1, 8), rng.randint(1, 8), rng.choice((0.0, 0.1, 0.2, 0.3, 0.4)))
            cs = corners(grid)
            for _ in range(2):
                result = self.check(grid, rng.choice(cs), rng.choice(cs))
                if result:
                    length, ref, _ = result
                    self.assertLessEqual(length, ref + EPS)

    def test_open_grid_is_a_straight_line(self):
        grid = Grid(["." * 7] * 5)
        path, length = theta_star(grid, (0, 0), (7, 3))
        self.assertEqual(path, [(0, 0), (7, 3)])
        self.assertAlmostEqual(length, math.hypot(7, 3))

    def test_page_example(self):
        """Shorter than the grid path, and longer than the optimum in the plane."""
        grid = Grid(PAGE_ROWS)
        path, length = theta_star(grid, (0, 0), (5, 2))
        self.assertEqual(path, PAGE_PATH)
        self.assertAlmostEqual(length, math.sqrt(17) + math.sqrt(2), places=9)
        self.assertAlmostEqual(grid_length(grid, (0, 0), (5, 2)), 3 + 2 * math.sqrt(2), places=9)
        self.assertAlmostEqual(visibility_length(grid, (0, 0), (5, 2)), math.sqrt(10) + math.sqrt(5), places=9)
        self.check(grid, (0, 0), (5, 2))

    def test_rejects_points_off_the_grid(self):
        with self.assertRaises(ValueError):
            theta_star(Grid([".."]), (0, 0), (3, 0))


PAGE_ROWS = ["....#", "#.#.."]
PAGE_PATH = [(0, 0), (4, 1), (5, 2)]


def experiment(seed, maps=40, w=10, h=10, density=0.2):
    """Sums of the lengths of Theta*, of grid A* and of the true optimum, and the count of maps
    where Theta* is strictly shorter than grid A*, equal, longer, and optimal."""
    rng = random.Random(seed)
    tot = [0.0, 0.0, 0.0]
    shorter = equal = longer = optimal = done = 0
    while done < maps:
        grid = random_grid(rng, w, h, density)
        cs = corners(grid)
        s, t = rng.choice(cs), rng.choice(cs)
        _, length = theta_star(grid, s, t)
        if length is None:
            continue
        ref, vis = grid_length(grid, s, t), visibility_length(grid, s, t)
        tot[0] += length
        tot[1] += ref
        tot[2] += vis
        shorter += length < ref - EPS
        equal += abs(length - ref) <= EPS
        longer += length > ref + EPS
        optimal += abs(length - vis) <= EPS
        done += 1
    return tuple(round(v, 3) for v in tot) + (shorter, equal, longer, optimal)


class Measured(unittest.TestCase):
    def test_experiment_numbers(self):
        """The numbers of the page: measurements, not guarantees."""
        self.assertEqual(experiment(9), EXPECTED)


EXPECTED = (233.111, 242.551, 232.779, 27, 13, 0, 38)

if __name__ == "__main__":
    unittest.main()
