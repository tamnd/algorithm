# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ellipsoid-method/. The authors are listed in prov/S8AASR.jsonl.

import itertools
import math
import random

from ellipsoid_method import cut, feasible_point, iteration_bound, minimize, rows_oracle, shape

TOL = 1e-7


def det(m):
    """Determinant by Gaussian elimination with partial pivoting."""
    a = [list(r) for r in m]
    n, d = len(a), 1.0
    for col in range(n):
        p = max(range(col, n), key=lambda i: abs(a[i][col]))
        if a[p][col] == 0:
            return 0.0
        if p != col:
            a[col], a[p] = a[p], a[col]
            d = -d
        d *= a[col][col]
        for i in range(col + 1, n):
            f = a[i][col] / a[col][col]
            a[i] = [vi - f * vc for vi, vc in zip(a[i], a[col])]
    return d


def solve(m, v):
    a = [list(r) + [x] for r, x in zip(m, v)]
    n = len(a)
    for col in range(n):
        p = max(range(col, n), key=lambda i: abs(a[i][col]))
        a[col], a[p] = a[p], a[col]
        for i in range(n):
            if i != col:
                f = a[i][col] / a[col][col]
                a[i] = [vi - f * vc for vi, vc in zip(a[i], a[col])]
    return [a[i][n] / a[i][i] for i in range(n)]


def inside(z, x, P):
    d = [zi - xi for zi, xi in zip(z, x)]
    return sum(di * wi for di, wi in zip(d, solve(P, d))) <= 1 + 1e-6


def test_one_cut_volume_and_containment() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 5)
        x = [rng.uniform(-1, 1) for _ in range(n)]
        L = [[rng.uniform(-1, 1) if j <= i else 0.0 for j in range(n)] for i in range(n)]
        for i in range(n):
            L[i][i] = abs(L[i][i]) + 0.5
        P = [[sum(L[i][k] * L[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
        g = [rng.uniform(-1, 1) for _ in range(n)]
        x2, J2 = cut(x, L, g)
        P2 = shape(J2)
        ratio = math.sqrt(det(P2) / det(P))  # vol(E') / vol(E)
        if n == 1:
            assert abs(ratio - 0.5) < TOL
        else:
            exact = n / (n + 1) * (n * n / (n * n - 1)) ** ((n - 1) / 2)
            assert abs(ratio - exact) < 1e-9 and ratio <= math.exp(-1 / (2 * (n + 1))) + TOL
        for _ in range(20):  # points of the half-ellipsoid stay inside the new ellipsoid
            u = [rng.gauss(0, 1) for _ in range(n)]
            s = math.sqrt(sum(v * v for v in u))
            u = [v / s * rng.random() ** (1 / n) for v in u]
            z = [x[i] + sum(L[i][k] * u[k] for k in range(n)) for i in range(n)]
            if sum(gi * (zi - xi) for gi, zi, xi in zip(g, z, x)) <= 0:
                assert inside(z, x2, P2)


def random_polytope(rng, n, feasible):
    """Constraints a_i^T z <= a_i^T z0 + margin around a center z0 (feasible), or a pair that excludes all z."""
    z0 = [rng.uniform(-2, 2) for _ in range(n)]
    a, b = [], []
    for _ in range(rng.randint(n + 1, 2 * n + 3)):
        row = [rng.uniform(-1, 1) for _ in range(n)]
        a.append(row)
        b.append(sum(r * v for r, v in zip(row, z0)) + rng.uniform(0.05, 1.0))
    if not feasible:
        row = [rng.uniform(-1, 1) for _ in range(n)]
        t = sum(r * v for r, v in zip(row, z0))
        a += [row, [-r for r in row]]
        b += [t - 0.3, -t - 0.3]  # row^T z <= t - 0.3 and row^T z >= t + 0.3
    return a, b, z0


def test_feasibility_against_known_answers() -> None:
    rng = random.Random(11)
    statuses = set()
    for t in range(500):
        n = rng.randint(1, 4)
        feasible = t % 3 != 0
        a, b, z0 = random_polytope(rng, n, feasible)
        # if feasible, the ball of radius 0.05 / max |a_i| around z0 is inside; all lies in the ball of radius 10
        inner = 0.05 / max(math.sqrt(sum(r * r for r in row)) for row in a)
        res = feasible_point(rows_oracle(a, b), n, 10.0, inner, keep=t < 60)
        if feasible:
            assert res.status == "feasible", (a, b)
            assert all(sum(r * v for r, v in zip(row, res.x)) <= bi + TOL for row, bi in zip(a, b))
            assert res.iterations <= iteration_bound(n, 10.0, inner)
            for x, P in zip(res.centers, res.shapes):  # a feasible point stays in every ellipsoid
                assert inside(z0, x, P)
        else:
            assert res.status == "empty"
        statuses.add(res.status)
    assert statuses == {"feasible", "empty"}


def test_minimize_against_vertex_enumeration() -> None:
    rng = random.Random(23)
    for _ in range(60):
        n = 2
        a, b, _ = random_polytope(rng, n, True)
        a += [[1, 0], [-1, 0], [0, 1], [0, -1]]
        b += [4, 4, 4, 4]
        c = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        best = math.inf
        for i, j in itertools.combinations(range(len(a)), 2):
            dd = a[i][0] * a[j][1] - a[i][1] * a[j][0]
            if abs(dd) < 1e-12:
                continue
            z = [(b[i] * a[j][1] - a[i][1] * b[j]) / dd, (a[i][0] * b[j] - b[i] * a[j][0]) / dd]
            if all(r[0] * z[0] + r[1] * z[1] <= bb + 1e-9 for r, bb in zip(a, b)):
                best = min(best, c[0] * z[0] + c[1] * z[1])
        res = minimize(c, rows_oracle(a, b), n, 10.0, 200)
        assert res.status == "feasible"
        value = c[0] * res.x[0] + c[1] * res.x[1]
        assert best - 1e-9 <= value <= best + 1e-6, (value, best)  # stated tolerance after 200 cuts in the plane


def test_example_trace() -> None:
    # x1 >= 2, x2 >= 2, x1 + x2 <= 5 from the disk of radius 4 around 0
    a, b = [[-1, 0], [0, -1], [1, 1]], [-2, -2, 5]
    res = feasible_point(rows_oracle(a, b), 2, 4.0, 0.05, keep=True)
    assert res.status == "feasible" and res.iterations == 6
    assert all(sum(r * v for r, v in zip(row, res.x)) <= bi for row, bi in zip(a, b))
    assert abs(res.centers[1][0] - 4 / 3) < TOL and abs(res.centers[2][0] - 20 / 9) < TOL
    areas = [math.sqrt(det(P)) for P in res.shapes]
    for u, v in zip(areas, areas[1:]):
        assert abs(v / u - 2 / 3 * math.sqrt(4 / 3)) < 1e-9
