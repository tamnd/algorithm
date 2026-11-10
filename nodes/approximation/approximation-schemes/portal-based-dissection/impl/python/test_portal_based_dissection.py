# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/portal-based-dissection/. The authors are listed in prov/4X3G6D.jsonl.

import random
from fractions import Fraction
from math import dist, sqrt

from portal_based_dissection import (crossings, depth_count, interface_count, line_level, nearest_portal, perturb,
                                     portal_gap, quadtree_size, random_shift, snap_tour)


def optimal_tour(points):
    """Held-Karp: a shortest closed tour through the points."""
    n = len(points)
    if n <= 2:
        return list(range(n)), 2 * dist(points[0], points[-1])
    full = 1 << n
    inf = float("inf")
    cost = [[inf] * n for _ in range(full)]
    back = [[-1] * n for _ in range(full)]
    cost[1][0] = 0.0
    for mask in range(1, full, 2):
        for j in range(n):
            c = cost[mask][j]
            if c == inf:
                continue
            for k in range(1, n):
                if not mask >> k & 1:
                    nm = mask | 1 << k
                    v = c + dist(points[j], points[k])
                    if v < cost[nm][k]:
                        cost[nm][k], back[nm][k] = v, j
    best, last = min((cost[full - 1][j] + dist(points[j], points[0]), j) for j in range(1, n))
    tour, mask = [], full - 1
    while last != -1:
        tour.append(last)
        mask, last = mask ^ (1 << last), back[mask][last]
    return tour[::-1], best


def random_points(rng, n, size):
    pts = set()
    while len(pts) < n:
        pts.add((rng.randrange(size), rng.randrange(size)))
    return sorted(pts)


EXAMPLE = [(0, 1), (2, 6), (5, 7), (6, 2)]


def test_example() -> None:
    size = 8
    assert depth_count(size) == 4
    # with the shift a = 3, the line x = 5 is the middle line of the root square [-3, 13)
    assert [line_level(c, 3, size) for c in range(1, 8)] == [2, 4, 3, 4, 1, 4, 3]
    assert [line_level(c, 5, size) for c in range(1, 8)] == [3, 4, 1, 4, 3, 4, 2]
    tour, length = optimal_tour(EXAMPLE)
    assert tour == [0, 3, 2, 1] and abs(length - (sqrt(29) + sqrt(10) + sqrt(26) + sqrt(37))) < 1e-9
    xs = crossings(EXAMPLE[0], EXAMPLE[1])
    assert xs == [("x", 1, Fraction(11, 4)), ("x", 2, Fraction(21, 4)), ("y", 2, Fraction(7, 10)),
                  ("y", 3, Fraction(11, 10)), ("y", 4, Fraction(3, 2)), ("y", 5, Fraction(19, 10)),
                  ("y", 6, Fraction(23, 10))]
    expected = {1: (Fraction(574, 15), Fraction(89, 3)), 2: (Fraction(14), Fraction(147, 10)),
                4: (Fraction(107, 15), Fraction(139, 20)), 8: (Fraction(62, 15), Fraction(97, 30))}
    for m, (at_shift, mean) in expected.items():
        st = {}
        assert snap_tour(EXAMPLE, tour, size, m, (3, 5), st) == at_shift and st["crossings"] == 24
        total = sum(snap_tour(EXAMPLE, tour, size, m, (a, b)) for a in range(size) for b in range(size))
        assert total / size ** 2 == mean <= Fraction(depth_count(size), m) * 24
    assert quadtree_size(EXAMPLE, size, (3, 5)) == (5, 1)


def test_level_probabilities() -> None:
    for size in (4, 8, 16, 32):
        depth = depth_count(size)
        for c in range(1, size):
            counts = [0] * (depth + 1)
            for a in range(size):
                counts[line_level(c, a, size)] += 1
            assert counts[0] == 0 and sum(counts) == size
            for i in range(1, depth + 1):
                assert counts[i] <= max(1, 2 ** (i - 2))  # so Pr[level i] <= 2^(i-1) / L
                assert counts[i] * size <= 2 ** (i - 1) * size


def test_snap_is_bounded_by_the_gap() -> None:
    rng = random.Random(1998)
    for _ in range(200):
        size, m = rng.choice([(8, 2), (16, 4), (16, 2)])
        p, q = random_points(rng, 2, size)
        shift = random_shift(size, rng)
        st = {}
        snap_tour([p, q], [0, 1], size, m, shift, st)
        assert st["worst"] <= 1
        assert st["crossings"] == 2 * (abs(p[0] - q[0]) + abs(p[1] - q[1]))
        for axis, c, t in crossings(p, q):
            level = line_level(c, shift[0] if axis == "x" else shift[1], size)
            portal, d = nearest_portal(t, shift[1] if axis == "x" else shift[0], portal_gap(level, size, m))
            assert d <= portal_gap(level, size, m) / 2 and abs(t - portal) == d


def test_expected_portal_cost_against_opt() -> None:
    rng = random.Random(1997)
    for _ in range(12):
        size, m = rng.choice([(8, 2), (8, 4), (16, 4)])
        pts = random_points(rng, rng.randint(3, 7), size)
        tour, length = optimal_tour(pts)
        depth = depth_count(size)
        st = {}
        snap_tour(pts, tour, size, m, (0, 0), st)
        # the crossings of a tour number at most sqrt(2) times its length
        assert st["crossings"] <= sqrt(2) * length + 1e-9
        total = sum(snap_tour(pts, tour, size, m, (a, b)) for a in range(size) for b in range(size))
        mean = total / size ** 2
        assert mean <= Fraction(depth, m) * st["crossings"]
        assert float(mean) <= sqrt(2) * depth / m * length + 1e-9


def test_quadtree_size() -> None:
    rng = random.Random(1996)
    for _ in range(100):
        size = rng.choice([8, 16, 32])
        n = rng.randint(1, 12)
        pts = random_points(rng, n, size)
        nodes, depth = quadtree_size(pts, size, random_shift(size, rng))
        assert depth <= depth_count(size)
        assert nodes <= 1 + 2 * n * depth_count(size)


def test_interface_count() -> None:
    for m in (1, 2, 4, 8):
        for r in (1, 2, 3):
            assert interface_count(m, r) <= (m + 2) ** (4 * r)


def test_perturb() -> None:
    rng = random.Random(1995)
    for _ in range(20):
        n = rng.randint(2, 30)
        pts = [(rng.random() * 100, rng.random() * 100) for _ in range(n)]
        for eps in (1.0, 0.5, 0.25):
            cells, size = perturb(pts, eps)
            assert size & (size - 1) == 0 and len(cells) <= n
            assert all(0 <= c < size for p in cells for c in p)
            assert size <= 2 * (8 * n / eps + 1)
