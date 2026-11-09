# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-feasibility-problem/. The authors are listed in prov/H1CESA.jsonl.

import math
import random
from fractions import Fraction
from itertools import combinations

from convex_feasibility_problem import cyclic_projections, distance, project

TOL = 1e-9


def test_projections():
    assert project(("halfspace", [1.0, 1.0], 2.0), [2.0, 2.0]) == [1.0, 1.0]
    assert project(("halfspace", [1.0, 1.0], 2.0), [0.0, 0.0]) == [0.0, 0.0]
    assert project(("hyperplane", [0.0, 2.0], 2.0), [3.0, 5.0]) == [3.0, 1.0]
    assert project(("ball", [0.0, 0.0], 1.0), [3.0, 4.0]) == [0.6, 0.8]
    assert project(("box", [0.0, 0.0], [1.0, 1.0]), [2.0, -1.0]) == [1.0, 0.0]


def test_example_disk_and_halfplane():
    # unit disk and x1 + x2 >= 1.2, from (2, 2)
    sets = [("ball", [0.0, 0.0], 1.0), ("halfspace", [-1.0, -1.0], -1.2)]
    x = cyclic_projections(sets, [2.0, 2.0], tol=TOL)
    assert x is not None
    assert all(distance(s, x) <= TOL for s in sets)


def test_two_lines_rate():
    th = math.radians(10)
    sets = [("hyperplane", [0.0, 1.0], 0.0), ("hyperplane", [-math.sin(th), math.cos(th)], 0.0)]
    trace = []
    cyclic_projections(sets, [math.cos(th), math.sin(th)], tol=1e-300, max_cycles=600, trace=trace)
    norms = [math.hypot(*p) for p in trace]
    for k in range(1, 100):
        assert abs(norms[k] / norms[k - 1] - math.cos(th) ** 2) < 1e-12
    first = next(k for k, r in enumerate(norms) if r <= 1e-6)
    assert first == 452


def random_planted(rng, n, m):
    z = [rng.uniform(-3, 3) for _ in range(n)]
    sets = []
    for _ in range(m):
        a = [rng.uniform(-1, 1) for _ in range(n)]
        sets.append(("halfspace", a, sum(ai * zi for ai, zi in zip(a, z)) + rng.uniform(0, 1)))
    c = [zi + rng.uniform(-1, 1) for zi in z]
    sets.append(("ball", c, math.dist(c, z) + rng.uniform(0.1, 1)))
    sets.append(("box", [zi - rng.uniform(0.1, 2) for zi in z], [zi + rng.uniform(0.1, 2) for zi in z]))
    return z, sets


def test_planted_and_fejer():
    rng = random.Random(11)
    for _ in range(40):
        n = rng.randint(1, 4)
        z, sets = random_planted(rng, n, rng.randint(1, 6))
        trace = []
        x = cyclic_projections(sets, [rng.uniform(-20, 20) for _ in range(n)], tol=1e-7, max_cycles=20000, trace=trace)
        assert x is not None
        assert all(distance(s, x) <= 1e-7 for s in sets)
        d = [math.dist(p, z) for p in trace]
        assert all(d[k + 1] <= d[k] + 1e-9 for k in range(len(d) - 1))


def test_infeasible_balls():
    sets = [("ball", [0.0, 0.0], 1.0), ("ball", [3.0, 0.0], 1.0)]
    assert cyclic_projections(sets, [5.0, 5.0], max_cycles=2000) is None


# Exact 2D reference: the largest t such that some x in R^2 satisfies
# a_i . x + t <= b_i for all i, with unit normals a_i. The constraints
# include a box, so the LP is bounded and its optimum is at a vertex.
UNIT = [(Fraction(3, 5), Fraction(4, 5)), (Fraction(5, 13), Fraction(12, 13)), (Fraction(8, 17), Fraction(15, 17)), (Fraction(1), Fraction(0))]


def unit_normals():
    out = set()
    for p, q in UNIT:
        for u, v in ((p, q), (q, p)):
            for su in (1, -1):
                for sv in (1, -1):
                    out.add((su * u, sv * v))
    return sorted(out)


def solve3(M, r):
    n = 3
    a = [row[:] + [r[i]] for i, row in enumerate(M)]
    for col in range(n):
        piv = next((i for i in range(col, n) if a[i][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        for i in range(n):
            if i != col and a[i][col] != 0:
                f = a[i][col] / a[col][col]
                a[i] = [x - f * y for x, y in zip(a[i], a[col])]
    return [a[i][n] / a[i][i] for i in range(n)]


def best_margin(cons):
    best = None
    for tri in combinations(cons, 3):
        z = solve3([[a[0], a[1], Fraction(1)] for a, _ in tri], [b for _, b in tri])
        if z is None:
            continue
        if all(a[0] * z[0] + a[1] * z[1] + z[2] <= b for a, b in cons):
            best = z[2] if best is None else max(best, z[2])
    return best


def test_against_exact_2d_reference():
    rng = random.Random(5)
    normals = unit_normals()
    box = [((Fraction(1), Fraction(0)), Fraction(5)), ((Fraction(-1), Fraction(0)), Fraction(5)), ((Fraction(0), Fraction(1)), Fraction(5)), ((Fraction(0), Fraction(-1)), Fraction(5))]
    checked = {"feasible": 0, "infeasible": 0}
    for _ in range(80):
        cons = box + [(rng.choice(normals), Fraction(rng.randint(-12, 12), 4)) for _ in range(rng.randint(2, 4))]
        t = best_margin(cons)
        sets = [("halfspace", [float(a[0]), float(a[1])], float(b)) for a, b in cons]
        x = cyclic_projections(sets, [rng.uniform(-8, 8), rng.uniform(-8, 8)], tol=TOL, max_cycles=800)
        if t >= Fraction(1, 20):
            assert x is not None
            assert all(float(a[0]) * x[0] + float(a[1]) * x[1] <= float(b) + 1e-8 for a, b in cons)
            checked["feasible"] += 1
        elif t <= -Fraction(1, 20):
            assert x is None
            checked["infeasible"] += 1
    assert checked["feasible"] >= 5 and checked["infeasible"] >= 5
