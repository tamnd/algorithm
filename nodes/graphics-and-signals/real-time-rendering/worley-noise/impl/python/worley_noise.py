# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/worley-noise/. The authors are listed in prov/KRW8CM.jsonl.

"""Worley noise (cellular noise) in 2D, after Worley 1996.

Space is cut into unit cells. Each cell holds a Poisson number of feature
points, with the mean `density`, placed uniformly in the cell. The count and
the places come from a generator seeded by the seed and the cell index, so
the same cell always holds the same points and no table is stored.

F_k(x) is the distance from x to the k-th nearest feature point. The search
visits the cells in square rings around the cell of x and stops when no cell
outside the rings can hold a point nearer than the current k-th distance.
This makes the result exact. The common shortcut of a 3 x 3 block is exact
only when the cells are never empty and F_k is small, which a Poisson count
does not promise.
"""

import random
from bisect import insort
from math import exp, floor, inf, sqrt

METRICS = {
    "euclidean": lambda dx, dy: sqrt(dx * dx + dy * dy),
    "manhattan": lambda dx, dy: abs(dx) + abs(dy),
    "chebyshev": lambda dx, dy: max(abs(dx), abs(dy)),
}


def poisson(rng, mean):
    """A Poisson sample by Knuth's product of uniforms (fine for a small mean)."""
    limit, k, prod = exp(-mean), 0, rng.random()
    while prod > limit:
        k += 1
        prod *= rng.random()
    return k


def cell_points(seed, i, j, density):
    """The feature points of cell (i, j). A string seed is hashed the same way on every run."""
    rng = random.Random(f"worley:{seed}:{i}:{j}")
    count = poisson(rng, density)
    return [(i + rng.random(), j + rng.random()) for _ in range(count)]


def ring(ci, cj, r):
    """The cells at Chebyshev distance exactly r from the cell (ci, cj)."""
    if r == 0:
        yield ci, cj
        return
    for a in range(-r, r + 1):
        yield ci + a, cj - r
        yield ci + a, cj + r
    for b in range(-r + 1, r):
        yield ci - r, cj + b
        yield ci + r, cj + b


def worley(x, y, k=2, seed=0, density=2.0, metric="euclidean", max_rings=10000):
    """Return [F_1, ..., F_k] at (x, y): the sorted distances to the k nearest points."""
    dist = METRICS[metric]
    ci, cj = floor(x), floor(y)
    fx, fy = x - ci, y - cj
    margin = min(fx, 1 - fx, fy, 1 - fy)  # @line L1
    best = []  # @line L2
    for r in range(max_rings):  # @line L3
        for (i, j) in ring(ci, cj, r):  # @line L4
            for (px, py) in cell_points(seed, i, j, density):  # @line L5
                d = dist(px - x, py - y)
                if len(best) < k or d < best[-1]:
                    insort(best, d)  # @line L6
                    del best[k:]
        if len(best) == k and best[-1] <= r + margin:  # @line L7
            return best  # @line L8
    raise RuntimeError("no k feature points found within max_rings")


class WorleyNoise:
    """Seeded 2D Worley noise. Calling it returns (F1, F2, ..., Fk)."""

    def __init__(self, seed=0, density=2.0, k=2, metric="euclidean"):
        self.seed, self.density, self.k, self.metric = seed, density, k, metric

    def __call__(self, x, y):
        return worley(x, y, self.k, self.seed, self.density, self.metric)

    def f2_minus_f1(self, x, y):
        f = self(x, y)
        return f[1] - f[0]

    def points(self, i, j):
        return cell_points(self.seed, i, j, self.density)


def nearest_brute_force(x, y, points, k, metric="euclidean"):
    """The k smallest distances from (x, y) to a list of points."""
    dist = METRICS[metric]
    return sorted(dist(px - x, py - y) for (px, py) in points)[:k]


def three_by_three(x, y, k=1, seed=0, density=2.0):
    """The common shortcut: search only the 3 x 3 block of cells. Not always exact."""
    ci, cj = floor(x), floor(y)
    pts = []
    for i in range(ci - 1, ci + 2):
        for j in range(cj - 1, cj + 2):
            pts.extend(cell_points(seed, i, j, density))
    out = nearest_brute_force(x, y, pts, k)
    return out + [inf] * (k - len(out))
