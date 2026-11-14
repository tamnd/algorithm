# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/curvature-tensor-estimation/. The authors are listed in prov/TJZ7S2.jsonl.

import math
import random

from curvature_tensor_estimation import dihedral, edge_curvature, principal_from_samples, taubin_curvature
from mx1mesh import (box_mesh, cylinder, dot, edge_faces, icosphere, mat_vec, neighbours, rotation_matrix, scale,
                     to_float, unit)


def inner(res):
    return [r for r in res if r is not None]


def euler(k1, k2, phi, theta):
    """The normal curvature in the direction theta when k1 is along phi (Euler's formula)."""
    return k1 * math.cos(theta - phi) ** 2 + k2 * math.sin(theta - phi) ** 2


# ---- Taubin's step on exact samples ----


def test_balanced_directions_give_the_exact_curvatures() -> None:
    rng = random.Random(1)
    for count in (5, 6, 7, 8):
        for _ in range(20):
            k1, k2 = sorted((rng.uniform(-3, 3), rng.uniform(-3, 3)), reverse=True)
            phi, start = rng.uniform(0, math.pi), rng.uniform(0, math.pi)
            th = [start + 2 * math.pi * j / count for j in range(count)]
            s = [(1.0, euler(k1, k2, phi, t), math.cos(t), math.sin(t)) for t in th]
            a, b, v1, _ = principal_from_samples(s)
            assert abs(a - k1) < 1e-12 and abs(b - k2) < 1e-12
            if k1 - k2 > 1e-3:
                assert abs(abs(v1[0] * math.cos(phi) + v1[1] * math.sin(phi)) - 1) < 1e-9


def test_four_directions_are_not_enough() -> None:
    # 4 equal directions: sum of e^(4 i theta) is not 0, and the estimate is biased
    k1, k2 = 1.0, 0.0
    s = [(1.0, euler(k1, k2, 0.0, t), math.cos(t), math.sin(t)) for t in (0, math.pi / 2, math.pi, 3 * math.pi / 2)]
    a, b, _, _ = principal_from_samples(s)
    assert abs(a - 1.5) < 1e-12 and abs(b + 0.5) < 1e-12
    assert abs((a + b) / 2 - 0.5) < 1e-12  # the mean is still right
    s = [(1.0, euler(k1, k2, 0.0, t), math.cos(t), math.sin(t)) for t in (math.pi / 4, 3 * math.pi / 4, 5 * math.pi / 4, 7 * math.pi / 4)]
    a, b, _, _ = principal_from_samples(s)
    assert abs(a - 0.5) < 1e-12 and abs(b - 0.5) < 1e-12  # turned by 45 degrees: no split at all


# ---- spheres ----


def test_taubin_on_a_sphere() -> None:
    r = 2.0
    p, f = icosphere(3, r)
    nb = neighbours(len(p), f)
    exact = [unit(q) for q in p]
    res = taubin_curvature(p, f, exact)
    for k1, k2, d1, d2, n in res:
        assert abs(k1 + k2 - 2 / r) < 1e-12  # the trace is exact with the true normals
        assert abs(dot(d1, d2)) < 1e-12 and abs(dot(d1, n)) < 1e-12
    for i in range(len(p)):
        if len(nb[i]) == 5:  # five equal directions: exact
            assert abs(res[i][0] - 1 / r) < 1e-12 and abs(res[i][1] - 1 / r) < 1e-12
    for k1, k2, *_ in taubin_curvature(p, f):  # the normals of the mesh
        assert abs(k1 + k2 - 2 / r) < 0.01


def test_edge_tensor_on_a_sphere_converges_with_a_larger_region() -> None:
    r = 2.0
    errs = []
    for level in (2, 3):
        p, f = icosphere(level, r)
        res = inner(edge_curvature(p, f, rings=1))
        errs.append(max(max(abs(k1 - 1 / r), abs(k2 - 1 / r)) for k1, k2, *_ in res))
    assert errs[1] < errs[0] / 2 and errs[1] < 0.012


# ---- cylinders ----


def test_edge_tensor_on_a_cylinder_has_a_closed_form() -> None:
    for m in (8, 16, 32):
        c = 2 * math.sin(math.pi / m)
        p, f = cylinder(1.0, 6 * c, m, 6)
        exp = (math.pi / m) / math.sin(math.pi / m)
        for rings in (0, 1):
            res = inner(edge_curvature(p, f, rings=rings))
            assert res
            for k1, k2, d1, d2, n in res:
                assert abs(k1 - exp) < 1e-12 and abs(k2) < 1e-12
                assert abs(abs(d2[2]) - 1) < 1e-12 and abs(d1[2]) < 1e-12  # k2 = 0 along the axis


def test_taubin_on_a_twisted_cylinder_converges() -> None:
    err = []
    for m in (16, 32):
        c = 2 * math.sin(math.pi / m)
        p, f = cylinder(1.0, 6 * c * math.sqrt(3) / 2, m, 6, twisted=True)
        res = inner(taubin_curvature(p, f))
        err.append(max(max(abs(k1 - 1), abs(k2)) for k1, k2, *_ in res))
        assert all(abs(abs(d2[2]) - 1) < 1e-9 for _, _, _, d2, _ in res)
    assert err[1] < err[0] / 3 and err[1] < 0.001


def test_taubin_on_the_plain_cylinder_keeps_a_bias() -> None:
    # six unequal directions: the limit is 1/2 + sqrt(5)/3, not 1, while the mean is right
    p, f = cylinder(1.0, 6 * 2 * math.sin(math.pi / 64), 64, 6)
    for k1, k2, *_ in inner(taubin_curvature(p, f)):
        assert abs(k1 - (0.5 + math.sqrt(5) / 3)) < 2e-3
        assert abs((k1 + k2) / 2 - 0.5) < 1e-3


# ---- signs, symmetry, and a saddle ----


def test_a_dent_has_negative_curvature() -> None:
    p, f = icosphere(2)
    f = [(a, c, b) for a, b, c in f]  # the normals now point in
    for fn in (taubin_curvature, edge_curvature):
        for k1, k2, *_ in inner(fn(p, f)):
            assert k1 < 0 and k2 < 0


def test_rotation_moves_the_directions_and_keeps_the_curvatures() -> None:
    rng = random.Random(4)
    p, f = icosphere(2)
    p = [scale(1 + 0.1 * rng.random(), q) for q in p]
    R = rotation_matrix((1, 2, 2), 0.7)
    q = [tuple(mat_vec(R, x)) for x in p]
    for fn in (taubin_curvature, edge_curvature):
        for a, b in zip(fn(p, f), fn(q, f)):
            assert abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9
            if a[0] - a[1] > 1e-3:
                assert abs(abs(dot(mat_vec(R, a[2]), b[2])) - 1) < 1e-6


def test_saddle() -> None:
    k = 16
    idx, p, f = {}, [], []
    for a in range(-4, 5):
        for b in range(-4, 5):
            idx[(a, b)] = len(p)
            x, y = a / k, b / k
            p.append((x, y, (x * x - y * y) / 2))
    for a in range(-4, 4):
        for b in range(-4, 4):
            A, B, C, D = idx[(a, b)], idx[(a + 1, b)], idx[(a + 1, b + 1)], idx[(a, b + 1)]
            f += [(A, B, C), (A, C, D)]
    o = idx[(0, 0)]
    k1, k2, d1, d2, n = edge_curvature(p, f)[o]
    assert abs(k1 - 1) < 0.01 and abs(k2 + 1) < 0.01 and abs(abs(d1[1]) - 1) < 1e-9
    k1, k2, *_ = taubin_curvature(p, f)[o]
    assert abs(k1 - 4 / 3) < 0.01 and abs(k2 + 4 / 3) < 0.01  # the grid's directions bias it by 4/3


def test_dihedral_signs_on_a_box() -> None:
    p, f = box_mesh((2, 3, 5), (2, 2, 2))
    p = to_float(p)
    for e, fs in edge_faces(f).items():
        b = dihedral(p, f, e, *fs)
        assert b == 0 or abs(b - math.pi / 2) < 1e-12
    assert sum(1 for e, fs in edge_faces(f).items() if dihedral(p, f, e, *fs) > 0) == 12 * 2
