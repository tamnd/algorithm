# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kabsch-algorithm/. The authors are listed in prov/P934Z2.jsonl.

import math
import random

from kabsch_algorithm import det3, jacobi_eigen_sym3, kabsch_algorithm, rmsd_after

TOL = 1e-6  # in angstrom; an RMSD near 0 is the square root of a rounding error near 1e-14


def rotation_from_quaternion(q):
    w, x, y, z = q
    return [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]]


def random_rotation(rng):
    q = [rng.gauss(0, 1) for _ in range(4)]
    n = math.sqrt(sum(c * c for c in q))
    return rotation_from_quaternion([c / n for c in q])


def random_points(rng, n, spread=10.0):
    return [tuple(rng.uniform(-spread, spread) for _ in range(3)) for _ in range(n)]


def transform(rot, t, pts):
    return [tuple(sum(rot[r][c] * p[c] for c in range(3)) + t[r] for r in range(3)) for p in pts]


def best_rmsd_for_rotation(rot, xs, ys):
    """RMSD of R x + t to y with the optimal t for this R (centroid matching)."""
    n = len(xs)
    xbar = [sum(p[k] for p in xs) / n for k in range(3)]
    ybar = [sum(p[k] for p in ys) / n for k in range(3)]
    rx = [sum(rot[r][c] * xbar[c] for c in range(3)) for r in range(3)]
    t = tuple(ybar[r] - rx[r] for r in range(3))
    return rmsd_after(rot, t, xs, ys)


def quaternion_oracle_rmsd(xs, ys):
    """Independent oracle: Horn's 4 x 4 matrix, top eigenvalue by repeated squaring."""
    n = len(xs)
    xbar = [sum(p[k] for p in xs) / n for k in range(3)]
    ybar = [sum(p[k] for p in ys) / n for k in range(3)]
    a = [[p[k] - xbar[k] for k in range(3)] for p in xs]
    b = [[p[k] - ybar[k] for k in range(3)] for p in ys]
    s = [[sum(ai[r] * bi[c] for ai, bi in zip(a, b)) for c in range(3)] for r in range(3)]
    sxx, sxy, sxz = s[0]
    syx, syy, syz = s[1]
    szx, szy, szz = s[2]
    nm = [[sxx + syy + szz, syz - szy, szx - sxz, sxy - syx],
          [syz - szy, sxx - syy - szz, sxy + syx, szx + sxz],
          [szx - sxz, sxy + syx, -sxx + syy - szz, syz + szy],
          [sxy - syx, szx + sxz, syz + szy, -sxx - syy + szz]]
    ga = sum(c * c for p in a for c in p)
    gb = sum(c * c for p in b for c in p)
    shift = ga + gb + 1.0
    m = [[nm[i][j] + (shift if i == j else 0.0) for j in range(4)] for i in range(4)]
    for _ in range(60):
        m = [[sum(m[i][k] * m[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        big = max(abs(c) for row in m for c in row)
        m = [[c / big for c in row] for row in m]
    j = max(range(4), key=lambda c: sum(m[r][c] ** 2 for r in range(4)))
    q = [m[r][j] for r in range(4)]
    norm = math.sqrt(sum(c * c for c in q))
    q = [c / norm for c in q]
    lam = sum(q[i] * nm[i][j2] * q[j2] for i in range(4) for j2 in range(4))
    return math.sqrt(max(ga + gb - 2 * lam, 0.0) / n)


def check_rotation(rot):
    assert abs(det3(rot) - 1.0) < 1e-9
    for i in range(3):
        for j in range(3):
            dot = sum(rot[k][i] * rot[k][j] for k in range(3))
            assert abs(dot - (1.0 if i == j else 0.0)) < 1e-9


def test_example_of_the_page() -> None:
    xs = [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 4.0)]
    rz = [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    ys = transform(rz, (1.0, 2.0, 3.0), xs)
    rot, t, r = kabsch_algorithm(xs, ys)
    assert r < 1e-9
    for i in range(3):
        for j in range(3):
            assert abs(rot[i][j] - rz[i][j]) < 1e-9
    assert all(abs(t[k] - (1.0, 2.0, 3.0)[k]) < 1e-9 for k in range(3))


def test_mirror_image_needs_the_reflection_fix() -> None:
    xs = [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 4.0)]
    ys = [(p[0], p[1], -p[2]) for p in xs]
    rot, t, r = kabsch_algorithm(xs, ys)
    check_rotation(rot)
    # For a mirror image E = 4 c3, where c3 is the smallest eigenvalue of C = sum a_i a_i^T.
    n = len(xs)
    xbar = [sum(p[k] for p in xs) / n for k in range(3)]
    a = [[p[k] - xbar[k] for k in range(3)] for p in xs]
    c = [[sum(ai[r] * ai[s] for ai in a) for s in range(3)] for r in range(3)]
    c3 = jacobi_eigen_sym3(c)[0][2]
    assert abs(r - math.sqrt(4 * c3 / n)) < 1e-9
    assert abs(r - quaternion_oracle_rmsd(xs, ys)) < 1e-9


def test_jacobi_eigen() -> None:
    rng = random.Random(7)
    for _ in range(200):
        m = [[rng.uniform(-5, 5) for _ in range(3)] for _ in range(3)]
        a = [[m[i][j] + m[j][i] for j in range(3)] for i in range(3)]
        vals, vecs = jacobi_eigen_sym3(a)
        assert vals[0] >= vals[1] >= vals[2]
        for k in range(3):
            v = [vecs[r][k] for r in range(3)]
            av = [sum(a[r][c] * v[c] for c in range(3)) for r in range(3)]
            assert all(abs(av[r] - vals[k] * v[r]) < 1e-9 for r in range(3))


def test_edges() -> None:
    p = [(1.0, 2.0, 3.0)]
    rot, t, r = kabsch_algorithm(p, [(4.0, 5.0, 6.0)])
    check_rotation(rot)
    assert r < 1e-12
    line = [(float(i), 2.0 * i, -1.0 * i) for i in range(5)]
    rng = random.Random(3)
    r0 = random_rotation(rng)
    rot, t, r = kabsch_algorithm(line, transform(r0, (1.0, 0.0, 0.0), line))
    check_rotation(rot)
    assert r < 1e-7
    same = [(1.0, 1.0, 1.0)] * 4
    rot, t, r = kabsch_algorithm(same, [(0.0, 0.0, 0.0)] * 4)
    check_rotation(rot)
    assert r < 1e-12


def test_known_rotations_random() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(3, 12)
        xs = random_points(rng, n)
        r0 = random_rotation(rng)
        t0 = tuple(rng.uniform(-20, 20) for _ in range(3))
        ys = transform(r0, t0, xs)
        rot, t, r = kabsch_algorithm(xs, ys)
        check_rotation(rot)
        assert r < 1e-6
        assert all(abs(rot[i][j] - r0[i][j]) < 1e-6 for i in range(3) for j in range(3))


def test_against_quaternion_oracle_and_random_rotations() -> None:
    rng = random.Random(99)
    for trial in range(500):
        n = rng.randint(3, 9)
        xs = random_points(rng, n)
        if trial % 3 == 0:  # mirror images force the reflection case
            ys = [(p[0], p[1], -p[2]) for p in xs]
        else:
            ys = [tuple(c + rng.gauss(0, 2.0) for c in p) for p in transform(random_rotation(rng), (0, 0, 0), xs)]
        rot, t, r = kabsch_algorithm(xs, ys)
        check_rotation(rot)
        assert abs(r - rmsd_after(rot, t, xs, ys)) < TOL
        assert abs(r - quaternion_oracle_rmsd(xs, ys)) < TOL
        for _ in range(20):  # no sampled rotation does better
            assert r <= best_rmsd_for_rotation(random_rotation(rng), xs, ys) + 1e-9


def test_grid_search_brute_force() -> None:
    rng = random.Random(5)
    xs = random_points(rng, 6)
    ys = [tuple(c + rng.gauss(0, 1.0) for c in p) for p in transform(random_rotation(rng), (0, 0, 0), xs)]
    _, _, r = kabsch_algorithm(xs, ys)
    best, best_q = math.inf, None
    steps = 12
    for i in range(steps):  # quaternions on a grid of the 3-sphere, in hyperspherical angles
        for j in range(steps):
            for k in range(steps):
                a1, a2, a3 = math.pi * (i + 0.5) / steps, math.pi * (j + 0.5) / steps, 2 * math.pi * k / steps
                q = (math.cos(a1), math.sin(a1) * math.cos(a2), math.sin(a1) * math.sin(a2) * math.cos(a3),
                     math.sin(a1) * math.sin(a2) * math.sin(a3))
                val = best_rmsd_for_rotation(rotation_from_quaternion(q), xs, ys)
                if val < best:
                    best, best_q = val, q
    assert r <= best + 1e-9
    step = 0.3  # local refinement of the best grid point by random perturbations
    for _ in range(80):
        for _ in range(25):
            q = [c + rng.gauss(0, step) for c in best_q]
            norm = math.sqrt(sum(c * c for c in q))
            q = [c / norm for c in q]
            val = best_rmsd_for_rotation(rotation_from_quaternion(q), xs, ys)
            if val < best:
                best, best_q = val, q
        step *= 0.88
    assert r <= best + 1e-9
    assert best - r < 1e-3  # the search reaches the optimum, and Kabsch is not worse
