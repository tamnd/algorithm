# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gonzalez-k-center/. The authors are listed in prov/FMYANK.jsonl.

import itertools
import random
from fractions import Fraction as F

from gonzalez_k_center import gonzalez_k_center


def line(a, b):
    return abs(a - b)


def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def radius(points, centers, dist):
    return max(min(dist(p, points[c]) for c in centers) for p in points)


def brute_opt(points, k, dist):
    """Least radius over all center sets of size min(k, n)."""
    n = len(points)
    return min(radius(points, cs, dist) for cs in itertools.combinations(range(n), min(k, n)))


def random_graph_metric(rng, n):
    """Shortest-path metric of a random complete graph with integer weights."""
    d = [[0 if i == j else rng.randint(1, 20) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i):
            d[i][j] = d[j][i]
    for m in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][m] + d[m][j] < d[i][j]:
                    d[i][j] = d[i][m] + d[m][j]
    return d


def check(points, k, dist, first=0):
    centers, r = gonzalez_k_center(points, k, dist, first)
    assert 1 <= len(centers) <= k
    assert len(set(centers)) == len(centers)
    assert centers[0] == first
    assert r == radius(points, centers, dist)
    opt = brute_opt(points, k, dist)
    assert opt <= r <= 2 * opt
    if len(centers) == k and r > 0:
        far = max(range(len(points)), key=lambda v: min(dist(points[v], points[c]) for c in centers))
        group = centers + [far]
        for a, b in itertools.combinations(group, 2):
            assert dist(points[a], points[b]) >= r
    return centers, r, opt


def test_page_example():
    pts = [0, 1, 2, 10, 11, 12]
    centers, r = gonzalez_k_center(pts, 2, line)
    assert centers == [0, 5]
    assert r == 2
    assert brute_opt(pts, 2, line) == 1


def test_page_example_2d():
    pts = [(0, 0), (1, 0), (0, 1), (6, 0), (7, 1), (3, 4)]
    assert gonzalez_k_center(pts, 3, manhattan) == ([0, 4, 5], 2)
    assert brute_opt(pts, 3, manhattan) == 2
    assert gonzalez_k_center(pts, 2, manhattan) == ([0, 4], 7)
    assert brute_opt(pts, 2, manhattan) == 6


def test_tight_k1():
    pts = [-1, 0, 1]
    centers, r = gonzalez_k_center(pts, 1, line, first=0)
    assert centers == [0] and r == 2
    assert brute_opt(pts, 1, line) == 1


def test_tight_family_each_k():
    for k in range(1, 6):
        pts = [-1, 0, 1] + [100 * j for j in range(1, k)]
        centers, r = gonzalez_k_center(pts, k, line, first=0)
        assert r == 2
        assert brute_opt(pts, k, line) == 1


def test_random_manhattan():
    rng = random.Random(20251110)
    for _ in range(300):
        n = rng.randint(1, 8)
        pts = [(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(n)]
        k = rng.randint(1, n)
        check(pts, k, manhattan, rng.randrange(n))


def test_random_fractions_on_line():
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(1, 8)
        pts = [F(rng.randint(-30, 30), rng.randint(1, 6)) for _ in range(n)]
        k = rng.randint(1, n)
        check(pts, k, line, rng.randrange(n))


def test_random_graph_metrics():
    rng = random.Random(12345)
    for _ in range(200):
        n = rng.randint(2, 8)
        d = random_graph_metric(rng, n)
        k = rng.randint(1, n)
        check(list(range(n)), k, lambda a, b: d[a][b], rng.randrange(n))


def test_k_at_least_n():
    pts = [(0, 0), (3, 1), (5, 5)]
    centers, r = gonzalez_k_center(pts, 5, manhattan)
    assert sorted(centers) == [0, 1, 2] and r == 0


def test_duplicates_stop_early():
    pts = [4, 4, 4]
    centers, r = gonzalez_k_center(pts, 3, line)
    assert centers == [0] and r == 0


def test_bad_input():
    for args in (([], 1), ([1], 0)):
        try:
            gonzalez_k_center(args[0], args[1], line)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
