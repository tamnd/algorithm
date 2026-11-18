# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deformation-gradient/. The authors are listed in prov/1C1F35.jsonl.
"""Tests of the deformation gradient of linear triangles and tetrahedra.

F reproduces every affine map, does not depend on the order of the
vertices, has det F equal to the ratio of the measures, composes by the
product rule, and approaches the Jacobian of a smooth map at first order.
The Green strain is zero exactly for rigid motions and is the symmetric
gradient at first order. The 2D polar factor is checked against a scan of
all rotations.
"""

import itertools
import math
import random

from anim import det, mul, q_normalize, q_to_mat3, transpose
from deformation_gradient import deformation_gradient, green_strain, polar_decomposition, simplex_measure


def close(a, b, tol):
    return all(abs(a[i][j] - b[i][j]) <= tol for i in range(len(a)) for j in range(len(a[0])))


def rand_mat(rng, d, amount=1.0):
    return [[(1.0 if i == j else 0.0) + rng.uniform(-amount, amount) for j in range(d)] for i in range(d)]


def rand_simplex(rng, d):
    while True:
        pts = [tuple(rng.uniform(-1, 1) for _ in range(d)) for _ in range(d + 1)]
        if abs(simplex_measure(pts)) > 0.05:
            return pts


def apply(a, t, p):
    return tuple(sum(a[i][k] * p[k] for k in range(len(p))) + t[i] for i in range(len(p)))


def rotation(rng, d):
    if d == 2:
        th = rng.uniform(-math.pi, math.pi)
        return [[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]]
    return q_to_mat3(q_normalize([rng.gauss(0, 1) for _ in range(4)]))


def test_affine_maps_are_reproduced_exactly():
    rng = random.Random(1)
    for d in (2, 3):
        for _ in range(200):
            a, t = rand_mat(rng, d), [rng.uniform(-3, 3) for _ in range(d)]
            rest = rand_simplex(rng, d)
            f = deformation_gradient(rest, [apply(a, t, p) for p in rest])
            assert close(f, a, 1e-9)


def test_vertex_order_does_not_matter():
    rng = random.Random(2)
    for d in (2, 3):
        rest = rand_simplex(rng, d)
        cur = [tuple(c + rng.uniform(-0.3, 0.3) for c in p) for p in rest]
        f0 = deformation_gradient(rest, cur)
        for perm in itertools.permutations(range(d + 1)):
            f = deformation_gradient([rest[i] for i in perm], [cur[i] for i in perm])
            assert close(f, f0, 1e-9)


def test_det_is_the_ratio_of_measures():
    rng = random.Random(3)
    for d in (2, 3):
        for _ in range(200):
            rest = rand_simplex(rng, d)
            cur = [tuple(c + rng.uniform(-0.6, 0.6) for c in p) for p in rest]
            j = det(deformation_gradient(rest, cur))
            assert abs(j - simplex_measure(cur) / simplex_measure(rest)) < 1e-9 * (1 + abs(j))


def test_inversion_flips_the_sign_of_j():
    rest = [(0, 0), (1, 0), (0, 1)]
    for y, sign in ((0.5, 1), (1e-9, 1), (-1e-9, -1), (-0.5, -1)):
        assert math.copysign(1, det(deformation_gradient(rest, [(0, 0), (1, 0), (0.2, y)]))) == sign


def test_composition_is_the_product():
    rng = random.Random(4)
    for d in (2, 3):
        a, b = rand_mat(rng, d, 0.5), rand_mat(rng, d, 0.5)
        rest = rand_simplex(rng, d)
        mid = [apply(a, [0.0] * d, p) for p in rest]
        end = [apply(b, [1.0] * d, p) for p in mid]
        f = deformation_gradient(rest, end)
        assert close(f, mul(deformation_gradient(mid, end), deformation_gradient(rest, mid)), 1e-9)


def test_green_strain_is_zero_exactly_for_rigid_motions():
    rng = random.Random(5)
    for d in (2, 3):
        for _ in range(100):
            q = rotation(rng, d)
            f = rand_mat(rng, d, 0.4)
            assert close(green_strain(q), [[0.0] * d for _ in range(d)], 1e-12)
            assert close(green_strain(mul(q, f)), green_strain(f), 1e-12)
            e = green_strain(f)
            if max(abs(v) for r in e for v in r) > 1e-3:
                assert not close(e, [[0.0] * d for _ in range(d)], 1e-6)


def test_green_strain_is_the_symmetric_gradient_at_first_order():
    rng = random.Random(6)
    h = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
    errs = []
    for eps in (1e-2, 5e-3):
        f = [[(1.0 if i == j else 0.0) + eps * h[i][j] for j in range(3)] for i in range(3)]
        e = green_strain(f)
        errs.append(max(abs(e[i][j] - 0.5 * eps * (h[i][j] + h[j][i])) for i in range(3) for j in range(3)))
    assert 3.5 < errs[0] / errs[1] < 4.5


def test_small_elements_approach_the_jacobian():
    def phi(p):
        x, y = p
        return (x + 0.3 * math.sin(y) + 0.2 * x * x, y + 0.1 * x * y)

    x0 = (0.4, 0.7)
    jac = [[1 + 0.4 * x0[0], 0.3 * math.cos(x0[1])], [0.1 * x0[1], 1 + 0.1 * x0[0]]]
    errs = []
    for hstep in (0.02, 0.01, 0.005):
        rest = [x0, (x0[0] + hstep, x0[1]), (x0[0], x0[1] + hstep)]
        f = deformation_gradient(rest, [phi(p) for p in rest])
        errs.append(max(abs(f[i][j] - jac[i][j]) for i in range(2) for j in range(2)))
    assert 1.8 < errs[0] / errs[1] < 2.2 and 1.8 < errs[1] / errs[2] < 2.2


def test_polar_decomposition_in_3d():
    rng = random.Random(8)
    for _ in range(50):
        f = rand_mat(rng, 3, 0.6)
        if abs(det(f)) < 0.05:
            continue
        r, s = polar_decomposition(f)
        assert close(mul(transpose(r), r), [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 1e-10) and det(r) > 0
        assert close(mul(r, s), f, 1e-10) and close(s, transpose(s), 1e-12)
        assert close(green_strain(f), green_strain(s), 1e-10)


def test_polar_decomposition_in_2d():
    rng = random.Random(7)
    for _ in range(300):
        f = rand_mat(rng, 2, 1.5)
        r, s = polar_decomposition(f)
        assert close(mul(transpose(r), r), [[1, 0], [0, 1]], 1e-12) and det(r) > 0
        assert close(mul(r, s), f, 1e-12) and s[0][1] == s[1][0]
        if det(f) > 0:
            assert s[0][0] > 0 and det(s) > 0
        tr = r[0][0] * f[0][0] + r[1][0] * f[1][0] + r[0][1] * f[0][1] + r[1][1] * f[1][1]
        for k in range(360):
            c, sn = math.cos(k * math.pi / 180), math.sin(k * math.pi / 180)
            assert c * (f[0][0] + f[1][1]) + sn * (f[1][0] - f[0][1]) <= tr + 1e-12
