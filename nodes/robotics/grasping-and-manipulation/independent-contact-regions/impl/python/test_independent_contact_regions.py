# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-contact-regions/. The authors are listed in prov/B0Z8Z4.jsonl.

# All checks are exact, in fractions.Fraction. The reference methods are
# written here again from the definitions: the friction cone as
# |tangential part| <= mu * normal part, and force closure as a strictly
# positive null vector of the 3 x 4 matrix of primitive wrenches with rank 3.

import random
from fractions import Fraction as F

from independent_contact_regions import (best_edge_pair, independent_regions,
                                         point_on_edge, region_program,
                                         simplex_max)

SQUARE = [(0, 0), (2, 0), (2, 2), (0, 2)]
TRIANGLE = [(0, 0), (4, 0), (1, 3)]


def frame(polygon, i):
    k = len(polygon)
    (ax, ay), (bx, by) = polygon[i], polygon[(i + 1) % k]
    d = (F(bx - ax), F(by - ay))
    return d, (-d[1], d[0])  # tangent and inward normal of a CCW polygon


def in_closed_cone(v, polygon, i, mu):
    d, n = frame(polygon, i)
    normal = v[0] * n[0] + v[1] * n[1]
    tangential = v[0] * d[0] + v[1] * d[1]
    return abs(tangential) <= mu * normal


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) -
            a[1] * (b[0] * c[2] - b[2] * c[0]) +
            a[2] * (b[0] * c[1] - b[1] * c[0]))


def force_closure(polygon, i, t1, j, t2, mu):
    # Planar wrench (m_z, f_x, f_y) with m_z = p_x f_y - p_y f_x.
    W = []
    for e, t in ((i, t1), (j, t2)):
        p = point_on_edge(polygon, e, t)
        d, n = frame(polygon, e)
        for s in (1, -1):
            f = (n[0] + s * mu * d[0], n[1] + s * mu * d[1])
            W.append((p[0] * f[1] - p[1] * f[0], f[0], f[1]))
    k = [(-1) ** c * det3(*[W[x] for x in range(4) if x != c])
         for c in range(4)]
    return all(v > 0 for v in k) or all(v < 0 for v in k)


def solve(M, rhs):
    # Gauss-Jordan elimination in exact arithmetic.
    n = len(M)
    A = [list(M[r]) + [rhs[r]] for r in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        A[c] = [v / A[c][c] for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [v - f * w for v, w in zip(A[r], A[c])]
    return [A[r][n] for r in range(n)]


def random_convex_polygon(rng):
    while True:
        pts = sorted(set((rng.randint(-6, 6), rng.randint(-6, 6))
                         for _ in range(8)))

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
        hull = lower[:-1] + upper[:-1]
        if len(hull) >= 4:
            return hull


def random_case(rng):
    poly = random_convex_polygon(rng)
    i, j = rng.sample(range(len(poly)), 2)
    mu = rng.choice([F(1, 4), F(1, 2), F(1), F(2)])
    return poly, i, j, mu


def grid_optimum(polygon, i, j, mu, N):
    # The largest smaller width of two grid intervals such that every pair of
    # grid points in them satisfies the closed cone condition.
    ok = [[False] * (N + 1) for _ in range(N + 1)]
    for a in range(N + 1):
        p1 = point_on_edge(polygon, i, F(a, N))
        for b in range(N + 1):
            p2 = point_on_edge(polygon, j, F(b, N))
            v = (p2[0] - p1[0], p2[1] - p1[1])
            ok[a][b] = (in_closed_cone(v, polygon, i, mu) and
                        in_closed_cone((-v[0], -v[1]), polygon, j, mu))
    best = None
    for s1 in range(N + 1):
        for u1 in range(s1, N + 1):
            for s2 in range(N + 1):
                for u2 in range(s2, N + 1):
                    w = F(min(u1 - s1, u2 - s2), N)
                    if best is not None and w <= best:
                        continue
                    if all(ok[a][b] for a in range(s1, u1 + 1)
                           for b in range(s2, u2 + 1)):
                        best = w
    return best


def test_square_opposite_sides():
    z, (s1, u1), (s2, u2) = independent_regions(SQUARE, 1, 3, F(1, 2))
    assert z == F(1, 2)
    assert u1 - s1 == F(1, 2) and u2 - s2 == F(1, 2)
    # Edge 1 goes up and edge 3 goes down: the heights must match.
    y1 = (point_on_edge(SQUARE, 1, s1)[1], point_on_edge(SQUARE, 1, u1)[1])
    y3 = (point_on_edge(SQUARE, 3, u2)[1], point_on_edge(SQUARE, 3, s2)[1])
    assert y1 == y3


def test_square_adjacent_sides():
    assert independent_regions(SQUARE, 0, 1, F(1, 2)) is None
    assert independent_regions(SQUARE, 0, 1, F(1)) is None  # only the corner
    z, r1, r2 = independent_regions(SQUARE, 0, 1, F(2))
    assert z == F(1, 2)


def test_triangle():
    assert best_edge_pair(TRIANGLE, F(1, 4)) is None
    z, i, j, r1, r2 = best_edge_pair(TRIANGLE, F(1))
    assert (z, i, j) == (F(2, 7), 0, 1)


def test_dual_certificate_proves_optimality():
    # For max c x, A x <= b, x >= 0: a y >= 0 with A^T y >= c and b y = z
    # proves that z is the optimum.
    rng = random.Random(1)
    found = 0
    for _ in range(12):
        poly, i, j, mu = random_case(rng)
        A, b, c = region_program(poly, i, j, mu)
        res = simplex_max(A, b, c)
        if res is None:
            continue
        found += 1
        z, x, basis = res
        m, n = len(A), len(c)
        assert len(basis) == m
        cols = [[A[r][k] if k < n else F(int(r == k - n)) for r in range(m)]
                for k in basis]
        cB = [F(c[k]) if k < n else F(0) for k in basis]
        y = solve(cols, cB)  # B^T y = c_B
        assert all(v >= 0 for v in y)
        for k in range(n):
            assert sum(A[r][k] * y[r] for r in range(m)) >= c[k]
        assert sum(b[r] * y[r] for r in range(m)) == z
        for r in range(m):
            assert sum(A[r][k] * x[k] for k in range(n)) <= b[r]
    assert found >= 4


def test_against_grid_brute_force():
    rng = random.Random(2)
    N = 10
    seen_none = seen_some = 0
    for _ in range(10):
        poly, i, j, mu = random_case(rng)
        res = independent_regions(poly, i, j, mu)
        g = grid_optimum(poly, i, j, mu, N)
        if res is None:
            seen_none += 1
            # No pair of grid points gives force closure.
            assert not any(force_closure(poly, i, F(a, N), j, F(b, N), mu)
                           for a in range(N + 1) for b in range(N + 1))
        else:
            seen_some += 1
            z = res[0]
            assert g is not None and z - F(2, N) < g <= z
    assert seen_none >= 1 and seen_some >= 3


def test_every_choice_in_the_regions_is_force_closure():
    rng = random.Random(3)
    checked = 0
    for _ in range(12):
        poly, i, j, mu = random_case(rng)
        res = independent_regions(poly, i, j, mu)
        if res is None:
            continue
        z, (s1, u1), (s2, u2) = res
        assert z > 0 and u1 - s1 >= z and u2 - s2 >= z
        for _ in range(40):
            t1 = s1 + (u1 - s1) * F(rng.randint(1, 999), 1000)
            t2 = s2 + (u2 - s2) * F(rng.randint(1, 999), 1000)
            assert force_closure(poly, i, t1, j, t2, mu)
        checked += 1
    assert checked >= 4
