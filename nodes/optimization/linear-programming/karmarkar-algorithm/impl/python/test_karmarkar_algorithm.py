# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karmarkar-algorithm/. The authors are listed in prov/8T5Z9B.jsonl.

import itertools
import math
import random

from karmarkar_algorithm import karmarkar_algorithm, potential, project_out, step_bound

TOL = 1e-9


def canonical_instance(rng):
    """A random program in canonical form with optimal value 0 at a known point xs.

    The rows of A are orthogonal to e and to xs, so A e = 0 and A xs = 0. The cost is
    c = A^T u + v with v >= 0 and v = 0 on the support of xs: then c^T x = v^T x >= 0 on
    the feasible set, and c^T xs = 0."""
    n = rng.randint(3, 8)
    support = rng.sample(range(n), rng.randint(1, n - 1))
    xs = [rng.uniform(0.1, 1.0) if j in support else 0.0 for j in range(n)]
    t = sum(xs)
    xs = [v / t for v in xs]
    q1 = [1 / math.sqrt(n)] * n
    d = sum(a * b for a, b in zip(xs, q1))
    q2 = [a - d * b for a, b in zip(xs, q1)]
    s = math.sqrt(sum(a * a for a in q2))
    q2 = [a / s for a in q2]
    a = []
    for _ in range(rng.randint(0, n - 2)):
        row = [rng.uniform(-1, 1) for _ in range(n)]
        for q in (q1, q2):
            d = sum(u * w for u, w in zip(row, q))
            row = [u - d * w for u, w in zip(row, q)]
        a.append(row)
    u = [rng.uniform(-1, 1) for _ in a]
    off = [j for j in range(n) if j not in support]
    v = [0.0] * n
    for j in off:
        v[j] = rng.choice([0.0, rng.uniform(0.1, 1.0)])
    v[off[0]] = rng.uniform(0.1, 1.0)
    c = [sum(u[i] * a[i][j] for i in range(len(a))) + v[j] for j in range(n)]
    return a, c, xs


def solve(m, rhs):
    """Gaussian elimination with partial pivoting; None if the matrix is singular."""
    t = [list(r) + [x] for r, x in zip(m, rhs)]
    k = len(t)
    for col in range(k):
        p = max(range(col, k), key=lambda i: abs(t[i][col]))
        if abs(t[p][col]) < 1e-10:
            return None
        t[col], t[p] = t[p], t[col]
        for i in range(k):
            if i != col:
                f = t[i][col] / t[col][col]
                t[i] = [vi - f * vc for vi, vc in zip(t[i], t[col])]
    return [t[i][k] / t[i][i] for i in range(k)]


def vertex_minimum(a, c):
    """Brute force: the least c^T x over the basic feasible solutions of [A; e^T] x = [0; 1]."""
    n = len(c)
    rows = [list(r) for r in a] + [[1.0] * n]
    rhs = [0.0] * len(a) + [1.0]
    best = math.inf
    for cols in itertools.combinations(range(n), len(rows)):  # the rows are independent by construction
        z = solve([[row[j] for j in cols] for row in rows], rhs)
        if z is None or min(z) < -TOL:
            continue
        best = min(best, sum(c[j] * v for j, v in zip(cols, z)))
    return best


def test_example_trace() -> None:
    # minimize x2 subject to x1 + x2 - 2 x3 = 0, x1 + x2 + x3 = 1, x >= 0; the optimum is (2/3, 0, 1/3)
    res = karmarkar_algorithm([[1, 1, -2]], [0, 1, 0], eps=1e-3)
    assert res.status == "optimal"
    expected = [1 / 3, 0.26116, 0.19496, 0.14007, 0.09798]
    assert all(abs(u - v) < 1e-5 for u, v in zip(res.values, expected))
    assert abs(res.x[2] - 1 / 3) < TOL and abs(res.x[0] - 2 / 3) < 1e-3
    assert res.values[-1] <= 1e-3 * res.values[0]


def test_random_canonical_programs() -> None:
    rng = random.Random(31)
    eps = 1e-8
    for _ in range(500):
        a, c, xs = canonical_instance(rng)
        n = len(c)
        assert abs(vertex_minimum(a, c)) < 1e-9  # brute force agrees that the optimal value is 0
        res = karmarkar_algorithm(a, c, eps=eps)
        assert res.status == "optimal"
        assert res.iterations <= step_bound(n, eps)
        x = res.x
        assert min(x) > 0 and abs(sum(x) - 1) < TOL
        assert all(abs(sum(r * v for r, v in zip(row, x))) < 1e-9 for row in a)
        assert -1e-12 <= res.values[-1] <= eps * res.values[0]
        for f0, f1 in zip(res.potentials, res.potentials[1:]):
            assert f0 - f1 >= 0.125 - TOL  # the potential drops by at least 1/8 per step
        for k, v in enumerate(res.values):
            assert v <= res.values[0] * math.exp(-k / (8 * n)) * (1 + TOL)


def test_projective_map_keeps_potential_differences() -> None:
    rng = random.Random(37)
    for _ in range(200):
        a, c, _ = canonical_instance(rng)
        n = len(c)
        res = karmarkar_algorithm(a, c, eps=1e-2)
        x = res.x if res.iterations else [1 / n] * n
        cbar = [ci * xi for ci, xi in zip(c, x)]
        rows = [[aij * xj for aij, xj in zip(row, x)] for row in a] + [[1.0] * n]
        p = project_out(rows, cbar)
        norm = math.sqrt(sum(v * v for v in p))
        y = [1 / n - 0.25 / math.sqrt(n * (n - 1)) * v / norm for v in p]
        s = sum(u * v for u, v in zip(x, y))
        x2 = [u * v / s for u, v in zip(x, y)]
        assert abs((potential(c, x2) - potential(c, x)) - (potential(cbar, y) - potential(cbar, [1 / n] * n))) < 1e-9


def test_edge_cases() -> None:
    # c^T x = 1 on the whole set: the optimal value is not 0, so the input is not canonical
    res = karmarkar_algorithm([[1, 1, -2]], [1, 1, 1])
    assert res.status == "constant" and res.iterations == 0
    # the center is optimal already
    res = karmarkar_algorithm([[1, -1, 0]], [1, -1, 0])
    assert res.status == "optimal" and res.iterations == 0
    # no rows: minimize over the simplex, optimum at the vertex e_1
    res = karmarkar_algorithm([], [0, 1, 2, 3], eps=1e-6)
    assert res.status == "optimal" and res.x[0] > 1 - 1e-5
