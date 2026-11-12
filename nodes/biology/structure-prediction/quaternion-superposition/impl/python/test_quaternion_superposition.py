# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quaternion-superposition/. The authors are listed in prov/AMR9P8.jsonl.

import math
import random

from quaternion_superposition import (horn_matrix, qcp_rmsd, quaternion_superposition,
                                      rotation_from_quaternion)

TOL = 1e-6  # angstrom


def random_unit_quaternion(rng):
    q = [rng.gauss(0, 1) for _ in range(4)]
    n = math.sqrt(sum(c * c for c in q))
    return [c / n for c in q]


def transform(rot, t, pts):
    return [tuple(sum(rot[r][c] * p[c] for c in range(3)) + t[r] for r in range(3)) for p in pts]


def rmsd_direct(rot, t, xs, ys):
    moved = transform(rot, t, xs)
    return math.sqrt(sum((p[k] - y[k]) ** 2 for p, y in zip(moved, ys) for k in range(3)) / len(xs))


def best_rmsd_for_rotation(rot, xs, ys):
    n = len(xs)
    xbar = [sum(p[k] for p in xs) / n for k in range(3)]
    ybar = [sum(p[k] for p in ys) / n for k in range(3)]
    t = [ybar[r] - sum(rot[r][c] * xbar[c] for c in range(3)) for r in range(3)]
    return rmsd_direct(rot, t, xs, ys)


# ---- an independent Kabsch oracle: closed-form 3 x 3 eigenvalues, eigenvectors by cross products

def _cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def _unit(a):
    n = math.sqrt(sum(c * c for c in a))
    return [c / n for c in a]


def _eigvec(m, lam):
    rows = [[m[i][j] - (lam if i == j else 0.0) for j in range(3)] for i in range(3)]
    cands = [_cross(rows[0], rows[1]), _cross(rows[0], rows[2]), _cross(rows[1], rows[2])]
    return _unit(max(cands, key=lambda c: sum(x * x for x in c)))


def _eigvals_sym3(m):
    p1 = m[0][1] ** 2 + m[0][2] ** 2 + m[1][2] ** 2
    q = (m[0][0] + m[1][1] + m[2][2]) / 3
    p2 = sum((m[i][i] - q) ** 2 for i in range(3)) + 2 * p1
    p = math.sqrt(p2 / 6)
    b = [[(m[i][j] - (q if i == j else 0.0)) / p for j in range(3)] for i in range(3)]
    detb = (b[0][0] * (b[1][1] * b[2][2] - b[1][2] * b[2][1]) - b[0][1] * (b[1][0] * b[2][2] - b[1][2] * b[2][0])
            + b[0][2] * (b[1][0] * b[2][1] - b[1][1] * b[2][0]))
    r = max(-1.0, min(1.0, detb / 2))
    phi = math.acos(r) / 3
    l1 = q + 2 * p * math.cos(phi)
    l3 = q + 2 * p * math.cos(phi + 2 * math.pi / 3)
    return l1, 3 * q - l1 - l3, l3


def kabsch_oracle(xs, ys):
    n = len(xs)
    xbar = [sum(p[k] for p in xs) / n for k in range(3)]
    ybar = [sum(p[k] for p in ys) / n for k in range(3)]
    a = [[p[k] - xbar[k] for k in range(3)] for p in xs]
    b = [[p[k] - ybar[k] for k in range(3)] for p in ys]
    h = [[sum(ai[r] * bi[c] for ai, bi in zip(a, b)) for c in range(3)] for r in range(3)]
    m = [[sum(h[k][r] * h[k][c] for k in range(3)) for c in range(3)] for r in range(3)]
    l1, l2, _ = _eigvals_sym3(m)
    v1, v2 = _eigvec(m, l1), _eigvec(m, l2)
    v3 = _cross(v1, v2)
    hv = lambda v: [sum(h[r][c] * v[c] for c in range(3)) for r in range(3)]
    u1 = _unit(hv(v1))
    w = hv(v2)
    d = sum(w[k] * u1[k] for k in range(3))
    u2 = _unit([w[k] - d * u1[k] for k in range(3)])
    u3 = _cross(u1, u2)
    vs, us = (v1, v2, v3), (u1, u2, u3)
    rot = [[sum(vs[k][r] * us[k][c] for k in range(3)) for c in range(3)] for r in range(3)]
    t = [ybar[r] - sum(rot[r][c] * xbar[c] for c in range(3)) for r in range(3)]
    return rot, rmsd_direct(rot, t, xs, ys)


def test_example_of_the_page() -> None:
    xs = [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 4.0)]
    rz = [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    ys = transform(rz, (1.0, 2.0, 3.0), xs)
    rot, t, r, q = quaternion_superposition(xs, ys)
    assert r < 1e-6
    h = math.sqrt(0.5)
    assert all(abs(q[k] - (h, 0.0, 0.0, h)[k]) < 1e-9 for k in range(4))
    assert all(abs(rot[i][j] - rz[i][j]) < 1e-9 for i in range(3) for j in range(3))
    mirror = [(p[0], p[1], -p[2]) for p in xs]
    _, _, r2, _ = quaternion_superposition(xs, mirror)
    assert abs(r2 - 1.2674395608605) < 1e-9
    assert abs(qcp_rmsd(xs, mirror) - r2) < 1e-9


def test_horn_identity() -> None:
    rng = random.Random(11)
    for _ in range(500):
        s = [[rng.uniform(-5, 5) for _ in range(3)] for _ in range(3)]
        q = random_unit_quaternion(rng)
        nm = horn_matrix(s)
        rot = rotation_from_quaternion(q)
        lhs = sum(q[i] * nm[i][j] * q[j] for i in range(4) for j in range(4))
        rhs = sum(rot[r][c] * s[c][r] for r in range(3) for c in range(3))
        assert abs(lhs - rhs) < 1e-9


def test_edges() -> None:
    rot, t, r, q = quaternion_superposition([(1.0, 2.0, 3.0)], [(0.0, 0.0, 0.0)])
    assert r < 1e-12 and abs(sum(c * c for c in q) - 1.0) < 1e-12
    line = [(float(i), 0.5 * i, 2.0 * i) for i in range(6)]
    rng = random.Random(4)
    r0 = rotation_from_quaternion(random_unit_quaternion(rng))
    _, _, r, _ = quaternion_superposition(line, transform(r0, (3.0, 1.0, 2.0), line))
    assert r < 1e-6


def test_known_rotations() -> None:
    rng = random.Random(31)
    for _ in range(500):
        n = rng.randint(3, 10)
        xs = [tuple(rng.uniform(-10, 10) for _ in range(3)) for _ in range(n)]
        q0 = random_unit_quaternion(rng)
        r0 = rotation_from_quaternion(q0)
        t0 = tuple(rng.uniform(-10, 10) for _ in range(3))
        rot, t, r, q = quaternion_superposition(xs, transform(r0, t0, xs))
        assert r < 1e-5
        assert all(abs(rot[i][j] - r0[i][j]) < 1e-6 for i in range(3) for j in range(3))
        sign = 1.0 if q0[0] >= 0 else -1.0
        assert all(abs(q[k] - sign * q0[k]) < 1e-6 for k in range(4))


def test_equals_kabsch_and_beats_random_rotations() -> None:
    rng = random.Random(77)
    for trial in range(500):
        n = rng.randint(4, 9)
        xs = [tuple(rng.uniform(-10, 10) for _ in range(3)) for _ in range(n)]
        if trial % 4 == 0:
            ys = [(p[0], -p[1], p[2]) for p in xs]  # mirror image: reflection case
        else:
            r0 = rotation_from_quaternion(random_unit_quaternion(rng))
            ys = [tuple(c + rng.gauss(0, 2.0) for c in p) for p in transform(r0, (0, 0, 0), xs)]
        rot, t, r, _ = quaternion_superposition(xs, ys)
        assert abs(r - rmsd_direct(rot, t, xs, ys)) < TOL
        _, rk = kabsch_oracle(xs, ys)
        assert abs(r - rk) < TOL
        assert abs(qcp_rmsd(xs, ys) - r) < TOL
        for _ in range(10):
            other = rotation_from_quaternion(random_unit_quaternion(rng))
            assert r <= best_rmsd_for_rotation(other, xs, ys) + 1e-9
