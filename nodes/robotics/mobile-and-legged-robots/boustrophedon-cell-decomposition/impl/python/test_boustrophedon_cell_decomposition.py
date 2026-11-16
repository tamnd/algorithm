# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boustrophedon-cell-decomposition/. The authors are listed in prov/E8C6B2.jsonl.

import math
import random
from fractions import Fraction

from boustrophedon_cell_decomposition import (
    cell_area,
    ceil_y,
    coverage_path,
    decompose,
    dfs_order,
    floor_y,
    lanes,
    locate,
    polygon_slice,
)

W, H = 20, 12


def hull(points):
    pts = sorted(set(points))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def shoelace(poly):
    m = len(poly)
    return abs(sum(poly[i][0] * poly[(i + 1) % m][1] - poly[(i + 1) % m][0] * poly[i][1] for i in range(m))) / 2


def random_obstacles(rng, k):
    """k disjoint convex polygons in general position inside the rectangle."""
    while True:
        discs, polys = [], []
        for _ in range(200):
            if len(polys) == k:
                break
            r = rng.uniform(0.6, 2.0)
            cx, cy = rng.uniform(r + 0.5, W - r - 0.5), rng.uniform(r + 0.5, H - r - 0.5)
            if any(math.hypot(cx - a, cy - b) < r + s + 0.3 for a, b, s in discs):
                continue
            pts = []
            for _ in range(rng.randint(3, 6)):
                t = rng.uniform(0, 2 * math.pi)
                pts.append((Fraction(round((cx + r * math.cos(t)) * 1000), 1000),
                            Fraction(round((cy + r * math.sin(t)) * 1000), 1000)))
            poly = hull(pts)
            xs = sorted(p[0] for p in poly)
            if len(poly) < 3 or xs[0] == xs[1] or xs[-1] == xs[-2]:
                continue
            discs.append((cx, cy, r))
            polys.append(poly)
        ends = [x for p in polys for x in (min(q[0] for q in p), max(q[0] for q in p))]
        if len(polys) == k and len(set(ends)) == len(ends):
            return polys


def inside(poly, x, y):
    s = polygon_slice(poly, x)
    return s is not None and s[0] <= y <= s[1]


def test_example_diamond():
    diamond = [(3, 3), (5, 1), (7, 3), (5, 5)]
    obstacles = [[(Fraction(a), Fraction(b)) for a, b in diamond]]
    cells, adj = decompose(10, 6, obstacles)
    assert len(cells) == 4
    assert [cell_area(c, obstacles, 6) for c in cells] == [18, 8, 8, 18]
    assert adj == {0: {1, 2}, 1: {0, 3}, 2: {0, 3}, 3: {1, 2}}
    assert dfs_order(adj) == [0, 1, 3, 2]
    assert sum(len(lanes(c, obstacles, 6, 1)) for c in cells) == 14
    # Lanes of the cell below the diamond: x = 3.5, 4.5, 5.5, 6.5, from y = 0 to the lower edge.
    assert lanes(cells[1], obstacles, 6, 1) == [(Fraction(7, 2), 0, Fraction(5, 2)), (Fraction(9, 2), 0, Fraction(3, 2)),
                                                (Fraction(11, 2), 0, Fraction(3, 2)), (Fraction(13, 2), 0, Fraction(5, 2))]


def test_cells_partition_the_free_space():
    rng = random.Random(41)
    for trial in range(12):
        k = rng.randint(0, 5)
        obstacles = random_obstacles(rng, k)
        cells, adj = decompose(W, H, obstacles)
        assert len(cells) == 1 + 3 * k
        free_area = W * H - sum(shoelace(p) for p in obstacles)
        assert sum(cell_area(c, obstacles, H) for c in cells) == free_area
        for _ in range(150):
            x = Fraction(rng.randrange(1, 10 ** 6 * W), 10 ** 6) + Fraction(1, 7 * 10 ** 7)
            y = Fraction(rng.randrange(1, 10 ** 6 * H), 10 ** 6) + Fraction(1, 11 * 10 ** 7)
            blocked = any(inside(p, x, y) for p in obstacles)
            assert len(locate(cells, obstacles, H, x, y)) == (0 if blocked else 1)


def test_adjacency_graph():
    rng = random.Random(42)
    for trial in range(12):
        k = rng.randint(1, 5)
        obstacles = random_obstacles(rng, k)
        cells, adj = decompose(W, H, obstacles)
        assert sum(len(v) for v in adj.values()) == 2 * 4 * k
        assert sorted(dfs_order(adj)) == list(range(len(cells)))
        for a in adj:
            for b in adj[a]:
                ca, cb = cells[a], cells[b]
                if ca.x1 != cb.x0:
                    ca, cb = cb, ca
                x = ca.x1
                assert x == cb.x0
                lo = max(floor_y(ca, obstacles, x), floor_y(cb, obstacles, x))
                hi = min(ceil_y(ca, obstacles, x, H), ceil_y(cb, obstacles, x, H))
                assert hi > lo


def test_lanes_cover_each_cell_within_half_a_width():
    rng = random.Random(43)
    for trial in range(8):
        obstacles = random_obstacles(rng, rng.randint(1, 4))
        cells, adj = decompose(W, H, obstacles)
        w = Fraction(rng.choice([1, 2, 3]), 2)
        path = coverage_path(cells, adj, obstacles, H, w)
        assert len(path) == sum(max(1, math.ceil((c.x1 - c.x0) / w)) for c in cells)
        for c in cells:
            xs = [ln[0] for ln in lanes(c, obstacles, H, w)]
            assert xs[0] - c.x0 <= w / 2 and c.x1 - xs[-1] <= w / 2
            assert all(b - a <= w for a, b in zip(xs, xs[1:]))
            for x, lo, hi in lanes(c, obstacles, H, w):
                assert lo < hi and not any(inside(p, x, (lo + hi) / 2) for p in obstacles)
        # Inside each cell, in visiting order, the lanes alternate up and down.
        i = 0
        for cid in dfs_order(adj):
            for j in range(len(lanes(cells[cid], obstacles, H, w))):
                (x0, y0), (x1, y1) = path[i]
                assert x0 == x1 and (y1 > y0) == (j % 2 == 0)
                i += 1
        assert i == len(path)
