# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zonotope-reachability/. The authors are listed in prov/XHB5KP.jsonl.

import itertools
import math
import random

from ctlmat import expm, matvec
from zonotope_reachability import (
    box,
    contains_2d,
    hull_with_map,
    interval_hull,
    linear_map,
    minkowski_sum,
    norm_inf,
    reach,
    reduce_order,
    support,
    sup_norm,
    vertices_2d,
    zonotope,
)

# The example of the page.
A = [[-1.0, -4.0], [4.0, -1.0]]
Z0 = box(2, 0.1, [1.0, 0.0])
MU = 0.05
R = 0.05


def corner_points(z):
    """All points c + sum s_j g_j with s_j = +1 or -1. Z is their convex hull."""
    c, gens = z
    pts = []
    for signs in itertools.product((-1.0, 1.0), repeat=len(gens)):
        pts.append([c[i] + sum(s * g[i] for s, g in zip(signs, gens)) for i in range(len(c))])
    return pts


def random_zonotope(rng, n, p):
    return zonotope([rng.uniform(-1, 1) for _ in range(n)], [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)])


def unit_directions(k):
    return [[math.cos(2 * math.pi * i / k), math.sin(2 * math.pi * i / k)] for i in range(k)]


def test_example_numbers():
    phi = expm([[R * v for v in row] for row in A])
    assert abs(phi[0][0] - math.exp(-R) * math.cos(4 * R)) < 1e-14
    assert abs(phi[1][0] - math.exp(-R) * math.sin(4 * R)) < 1e-14
    assert norm_inf(A) == 5.0
    assert abs(sup_norm(Z0) - 1.1) < 1e-15
    qs = reach(A, Z0, MU, R, 20)
    assert [len(q[1]) for q in qs] == [7 + 2 * i for i in range(20)]
    lo, hi = interval_hull(qs[0])
    assert abs(lo[0] - 0.773102) < 1e-6 and abs(hi[0] - 1.159166) < 1e-6
    assert abs(lo[1] + 0.159166) < 1e-6 and abs(hi[1] - 0.348146) < 1e-6
    lo, hi = interval_hull(qs[19])
    assert abs(lo[0] + 0.430991) < 1e-6 and abs(hi[0] + 0.115371) < 1e-6


def test_support_function_matches_corners():
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(1, 3)
        z = random_zonotope(rng, n, rng.randint(0, 5))
        pts = corner_points(z)
        for _ in range(5):
            d = [rng.uniform(-1, 1) for _ in range(n)]
            best = max(sum(a * b for a, b in zip(d, p)) for p in pts)
            assert abs(support(z, d) - best) < 1e-12


def test_linear_map_and_sum_are_exact():
    rng = random.Random(2)
    for _ in range(50):
        z1 = random_zonotope(rng, 2, 3)
        z2 = random_zonotope(rng, 2, 2)
        m = [[rng.uniform(-2, 2) for _ in range(2)] for _ in range(2)]
        mz = linear_map(m, z1)
        s = minkowski_sum(z1, z2)
        for d in unit_directions(24):
            mtd = [m[0][0] * d[0] + m[1][0] * d[1], m[0][1] * d[0] + m[1][1] * d[1]]
            assert abs(support(mz, d) - support(z1, mtd)) < 1e-12
            assert abs(support(s, d) - support(z1, d) - support(z2, d)) < 1e-12


def test_contains_2d_is_exact_on_vertices():
    rng = random.Random(3)
    for _ in range(40):
        z = random_zonotope(rng, 2, rng.randint(1, 5))
        for v in vertices_2d(z):
            assert contains_2d(z, v)
        c = z[0]
        for v in vertices_2d(z):
            out = [c[0] + 1.001 * (v[0] - c[0]), c[1] + 1.001 * (v[1] - c[1])]
            assert not contains_2d(z, out, tol=1e-12)


def test_hull_contains_convex_hull():
    rng = random.Random(4)
    for _ in range(30):
        z = random_zonotope(rng, 2, rng.randint(1, 3))
        phi = [[rng.uniform(-1.5, 1.5) for _ in range(2)] for _ in range(2)]
        h = hull_with_map(z, phi)
        pz = linear_map(phi, z)
        for p in corner_points(z) + corner_points(pz):
            assert contains_2d(h, p)
        for _ in range(20):
            lam = rng.random()
            p = rng.choice(corner_points(z))
            q = rng.choice(corner_points(pz))
            assert contains_2d(h, [lam * a + (1 - lam) * b for a, b in zip(p, q)])


def test_reduction_contains_original():
    rng = random.Random(5)
    for _ in range(30):
        z = random_zonotope(rng, 2, rng.randint(3, 8))
        red = reduce_order(z, 3)
        assert len(red[1]) <= 3
        # Z is the convex hull of its corner points, and the reduced zonotope is
        # convex, so this proves containment.
        for p in corner_points(z):
            assert contains_2d(red, p)


def test_reduction_contains_original_in_3d_by_support():
    rng = random.Random(6)
    for _ in range(20):
        z = random_zonotope(rng, 3, 9)
        red = reduce_order(z, 4)
        assert len(red[1]) <= 4
        for _ in range(50):
            d = [rng.gauss(0, 1) for _ in range(3)]
            assert support(red, d) >= support(z, d) - 1e-12


def simulate_inside(a, z0, mu, r, steps, qs, rng, sub=10, trials=40, check=contains_2d):
    """RK4 runs with random piecewise constant inputs; x(t) must lie in Q_i for t in [i r, (i+1) r]."""
    n = len(a)
    h = r / sub

    def f(x, u):
        return [sum(a[i][j] * x[j] for j in range(n)) + u[i] for i in range(n)]

    c, gens = z0
    for _ in range(trials):
        coef = [rng.choice((-1.0, 1.0)) if rng.random() < 0.5 else rng.uniform(-1, 1) for _ in gens]
        x = [c[i] + sum(s * g[i] for s, g in zip(coef, gens)) for i in range(n)]
        for i in range(steps):
            for k in range(sub):
                assert check(qs[i], x), (i, k, x)
                u = [mu * rng.choice((-1.0, 1.0)) for _ in range(n)]
                k1 = f(x, u)
                k2 = f([xi + h / 2 * v for xi, v in zip(x, k1)], u)
                k3 = f([xi + h / 2 * v for xi, v in zip(x, k2)], u)
                k4 = f([xi + h * v for xi, v in zip(x, k3)], u)
                x = [xi + h / 6 * (p + 2 * q + 2 * s + t) for xi, p, q, s, t in zip(x, k1, k2, k3, k4)]
            assert check(qs[i], x)


def test_trajectories_stay_inside_example():
    rng = random.Random(7)
    qs = reach(A, Z0, MU, R, 20)
    simulate_inside(A, Z0, MU, R, 20, qs, rng)


def test_trajectories_stay_inside_with_reduction():
    rng = random.Random(8)
    qs = reach(A, Z0, MU, R, 20, max_gens=6)
    assert all(len(q[1]) <= 6 for q in qs)
    simulate_inside(A, Z0, MU, R, 20, qs, rng)


def test_trajectories_unstable_and_zero_matrix():
    rng = random.Random(9)
    a = [[0.5, 1.0], [0.0, 0.3]]
    z0 = zonotope([0.0, 1.0], [[0.2, 0.1], [0.0, 0.05]])
    qs = reach(a, z0, 0.1, 0.1, 15, max_gens=8)
    simulate_inside(a, z0, 0.1, 0.1, 15, qs, rng, trials=20)
    zero = [[0.0, 0.0], [0.0, 0.0]]
    qs = reach(zero, z0, 0.2, 0.1, 5)
    simulate_inside(zero, z0, 0.2, 0.1, 5, qs, rng, trials=10)


def test_trajectories_3d_by_support():
    """In 3D the test only checks support directions: a necessary condition."""
    rng = random.Random(10)
    a = [[-0.5, 2.0, 0.0], [-2.0, -0.5, 0.0], [0.0, 0.0, -1.0]]
    z0 = box(3, 0.05, [1.0, 0.0, 1.0])
    qs = reach(a, z0, 0.02, 0.05, 10, max_gens=9)
    dirs = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(30)]

    def check(q, x):
        return all(sum(di * xi for di, xi in zip(d, x)) <= support(q, d) + 1e-9 for d in dirs)

    simulate_inside(a, z0, 0.02, 0.05, 10, qs, rng, trials=10, check=check)


def test_no_input_contains_exact_flow():
    """With mu = 0, the exact image e^(tA) Z0 at sample times lies in the reach set."""
    qs = reach(A, Z0, 0.0, R, 20)
    for i in range(20):
        for frac in (0.0, 0.3, 0.7, 1.0):
            e = expm([[(i + frac) * R * v for v in row] for row in A])
            for p in corner_points(Z0):
                assert contains_2d(qs[i], matvec(e, p))


def test_smaller_step_is_tighter():
    """Halving r shrinks the first set; the extra width of Q_0 is about alpha, which is O(r^2)."""
    widths = []
    for r in (0.04, 0.02, 0.01):
        q0 = reach(A, Z0, 0.0, r, 1)[0]
        lo, hi = interval_hull(q0)
        hull = hull_with_map(Z0, expm([[r * v for v in row] for row in A]))
        hlo, hhi = interval_hull(hull)
        widths.append((hi[0] - lo[0]) - (hhi[0] - hlo[0]))
    assert widths[1] < 0.3 * widths[0] and widths[2] < 0.3 * widths[1]
