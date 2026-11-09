# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barvinok-algorithm/. The authors are listed in prov/EFNZQ1.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from barvinok_algorithm import barvinok_count, decompose, shortest_vector, signed_cones


def brute_count(vertices):
    """Reference: test every integer point of the bounding box."""
    vs = [(F(x), F(y)) for x, y in vertices]
    m = len(vs)
    xs = [v[0] for v in vs]
    ys = [v[1] for v in vs]
    count = 0
    for x in range(math.floor(min(xs)), math.ceil(max(xs)) + 1):
        for y in range(math.floor(min(ys)), math.ceil(max(ys)) + 1):
            if all(
                (vs[(i + 1) % m][0] - vs[i][0]) * (y - vs[i][1]) - (vs[(i + 1) % m][1] - vs[i][1]) * (x - vs[i][0]) >= 0
                for i in range(m)
            ):
                count += 1
    return count


def lattice_points(vertices):
    vs = [(F(x), F(y)) for x, y in vertices]
    m = len(vs)
    xs = [v[0] for v in vs]
    ys = [v[1] for v in vs]
    for x in range(math.floor(min(xs)), math.ceil(max(xs)) + 1):
        for y in range(math.floor(min(ys)), math.ceil(max(ys)) + 1):
            if all(
                (vs[(i + 1) % m][0] - vs[i][0]) * (y - vs[i][1]) - (vs[(i + 1) % m][1] - vs[i][1]) * (x - vs[i][0]) >= 0
                for i in range(m)
            ):
                yield (x, y)


def hull(points):
    """Strictly convex hull in counterclockwise order (Andrew's monotone chain)."""
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


def random_polygon(rng, span, dens, k):
    while True:
        pts = [(F(rng.randint(-span * d, span * d), d), F(rng.randint(-span * e, span * e), e))
               for d, e in ((rng.choice(dens), rng.choice(dens)) for _ in range(k))]
        h = hull(pts)
        if len(h) >= 3:
            return h


def test_worked_example():
    tri = [(0, 0), (2, 0), (0, 1)]
    cones = signed_cones(tri)
    assert cones == [
        (1, (0, 0), (1, 0), (0, 1)),
        (1, (2, 0), (-2, 1), (-1, 0)),
        (1, (0, 1), (0, -1), (1, 0)),
        (1, (0, 1), (-1, 0), (2, -1)),
    ]
    assert barvinok_count(tri) == 4
    assert barvinok_count([(0, 0), (4, 0), (0, 3)]) == 11


def test_edges():
    assert barvinok_count([(0, 0), (1, 0), (1, 1), (0, 1)]) == 4
    assert barvinok_count([(F(1, 3), F(1, 3)), (F(2, 3), F(1, 3)), (F(1, 2), F(2, 3))]) == 0
    assert barvinok_count([(F(-1, 2), F(-1, 2)), (F(1, 2), F(-1, 2)), (0, F(1, 2))]) == 1
    with pytest.raises(ValueError):
        barvinok_count([(0, 0), (1, 1)])
    with pytest.raises(ValueError):
        barvinok_count([(0, 0), (0, 1), (1, 0)])  # clockwise
    with pytest.raises(ValueError):
        barvinok_count([(0, 0), (1, 0), (2, 0), (0, 1)])  # three collinear vertices


def test_large_polygons():
    for n in (10, 999, 10**9, 10**30):
        assert barvinok_count([(0, 0), (n, 0), (0, n)]) == (n + 1) * (n + 2) // 2
        assert barvinok_count([(0, 0), (n, 0), (n, n), (0, n)]) == (n + 1) ** 2
    # Pick's theorem: area + boundary / 2 + 1 for a lattice triangle
    a, b = 10**12, 10**12 + 7
    boundary = a + b + math.gcd(a, b)
    assert barvinok_count([(0, 0), (a, 0), (0, b)]) == a * b // 2 + boundary // 2 + 1


def test_shortest_vector():
    rng = random.Random(1)
    for _ in range(100):
        while True:
            u = (rng.randint(-30, 30), rng.randint(-30, 30))
            v = (rng.randint(-30, 30), rng.randint(-30, 30))
            if u[0] * v[1] - u[1] * v[0] != 0:
                break
        w = shortest_vector(u, v)
        best = min(
            (i * u[0] + j * v[0]) ** 2 + (i * u[1] + j * v[1]) ** 2
            for i in range(-40, 41)
            for j in range(-40, 41)
            if (i, j) != (0, 0)
        )
        assert w[0] ** 2 + w[1] ** 2 == best


def test_decompose_unimodular():
    rng = random.Random(2)
    for _ in range(300):
        p = (rng.randint(-50, 50), rng.randint(-50, 50))
        q = (rng.randint(-50, 50), rng.randint(-50, 50))
        if p[0] * q[1] - p[1] * q[0] == 0:
            continue
        for eps, a, b in decompose(p, q):
            assert eps in (1, -1)
            assert abs(a[0] * b[1] - a[1] * b[0]) == 1


def test_generating_function_identity():
    """The signed sum of the rational functions equals the sum of z^m over the lattice points."""
    rng = random.Random(3)
    for _ in range(60):
        poly = random_polygon(rng, 3, [1, 2, 3], rng.randint(3, 7))
        pts = list(lattice_points(poly))
        cones = signed_cones(poly)
        z = (F(rng.choice([2, 3, 5]), rng.choice([7, 11])), F(rng.choice([13, 17]), rng.choice([3, 4])))

        def mono(m):
            return z[0] ** m[0] * z[1] ** m[1]

        lhs = sum((mono(m) for m in pts), F(0))
        rhs = sum((eps * mono(u) / ((1 - mono(r)) * (1 - mono(s))) for eps, u, r, s in cones), F(0))
        assert lhs == rhs


def test_random_against_brute_force():
    rng = random.Random(20260611)
    for _ in range(600):
        span = rng.choice([2, 4, 6])
        dens = rng.choice([[1], [1, 2], [1, 2, 3, 5], [7, 9]])
        poly = random_polygon(rng, span, dens, rng.randint(3, 8))
        assert barvinok_count(poly) == brute_count(poly)
