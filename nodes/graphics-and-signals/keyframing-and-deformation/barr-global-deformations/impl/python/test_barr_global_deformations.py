# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barr-global-deformations/. The authors are listed in prov/702PFN.jsonl.
import math
import random

from barr_global_deformations import bend, cofactor, deform, deform_point, det3, jacobian, mat_vec, taper, twist


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def close(a, b, eps=1e-9):
    return all(abs(x - y) <= eps for x, y in zip(a, b))


def lin_taper():
    return taper(lambda z: 1.0 - 0.4 * z, lambda z: -0.4)


def lin_twist():
    return twist(lambda z: 0.8 * z, lambda z: 0.8)


def sample_ops():
    return [
        [lin_taper()],
        [lin_twist()],
        [bend(0.7, 0.0, -1.0, 1.0)],
        [lin_taper(), lin_twist(), bend(0.5, 0.2, -0.5, 0.8)],
        [twist(lambda z: math.sin(z), math.cos), taper(lambda z: 1 + 0.2 * z * z, lambda z: 0.4 * z)],
    ]


def fd_jacobian(p, ops, h=1e-6):
    cols = []
    for c in range(3):
        a, b = list(p), list(p)
        a[c] += h
        b[c] -= h
        fa, fb = deform_point(a, ops), deform_point(b, ops)
        cols.append([(fa[r] - fb[r]) / (2 * h) for r in range(3)])
    return [[cols[c][r] for c in range(3)] for r in range(3)]


def test_jacobian_matches_finite_differences():
    rng = random.Random(21)
    for ops in sample_ops():
        for _ in range(10):
            p = [rng.uniform(-1.5, 1.5) for _ in range(3)]
            # Stay away from the bend region ends, where the Jacobian jumps.
            if any(abs(p[1] - e) < 1e-3 for e in (-1.0, 1.0, -0.5, 0.8)):
                continue
            j, f = jacobian(p, ops), fd_jacobian(p, ops)
            for r in range(3):
                assert close(j[r], f[r], 1e-5)


def test_cofactor_maps_cross_products():
    rng = random.Random(22)
    for ops in sample_ops():
        for _ in range(5):
            p = [rng.uniform(-1, 1) for _ in range(3)]
            j = jacobian(p, ops)
            a = [rng.uniform(-1, 1) for _ in range(3)]
            b = [rng.uniform(-1, 1) for _ in range(3)]
            assert close(mat_vec(cofactor(j), cross(a, b)), cross(mat_vec(j, a), mat_vec(j, b)), 1e-12)


def test_normal_stays_perpendicular_to_moved_tangents():
    rng = random.Random(23)
    for ops in sample_ops():
        for _ in range(5):
            p = [rng.uniform(-1, 1) for _ in range(3)]
            n = [rng.uniform(-1, 1) for _ in range(3)]
            # Two tangent vectors perpendicular to n.
            t1 = cross(n, (1.0, 0.3, -0.2))
            t2 = cross(n, t1)
            _, n2 = deform(p, n, ops)
            j = jacobian(p, ops)
            for t in (t1, t2):
                jt = mat_vec(j, t)
                assert abs(sum(x * y for x, y in zip(jt, n2))) < 1e-12
            assert abs(math.sqrt(sum(v * v for v in n2)) - 1) < 1e-12


def test_determinants():
    rng = random.Random(24)
    for _ in range(10):
        p = [rng.uniform(-1, 1) for _ in range(3)]
        r = 1.0 - 0.4 * p[2]
        assert abs(det3(jacobian(p, [lin_taper()])) - r * r) < 1e-12
        assert abs(det3(jacobian(p, [lin_twist()])) - 1) < 1e-12
        k = 0.7
        inside = -1.0 <= p[1] <= 1.0
        want = 1 - k * p[2] if inside else 1.0
        assert abs(det3(jacobian(p, [bend(k, 0.0, -1.0, 1.0)])) - want) < 1e-12
        p_out = [p[0], 1.5 + abs(p[1]), p[2]]
        assert abs(det3(jacobian(p_out, [bend(k, 0.0, -1.0, 1.0)])) - 1) < 1e-12


def test_identity_parameters():
    ops = [taper(lambda z: 1.0, lambda z: 0.0), twist(lambda z: 0.0, lambda z: 0.0)]
    rng = random.Random(25)
    for _ in range(10):
        p = tuple(rng.uniform(-2, 2) for _ in range(3))
        n = (0.0, 0.6, 0.8)
        q, m = deform(p, n, ops)
        assert close(q, p) and close(m, n)


def test_bend_maps_axis_onto_circle_and_is_continuous():
    k, y0 = 0.5, 0.0
    op = [bend(k, y0, -2.0, 2.0)]
    for y in (-2.0, -1.0, 0.0, 0.7, 2.0):
        q = deform_point((0.0, y, 0.0), op)
        # The line z = 0 lands on the circle of radius 1/k about (y0, 1/k).
        assert abs(math.hypot(q[1] - y0, q[2] - 1 / k) - 1 / k) < 1e-12
    for e in (-2.0, 2.0):
        a = deform_point((0.1, e - 1e-9, 0.3), op)
        b = deform_point((0.1, e + 1e-9, 0.3), op)
        assert math.dist(a, b) < 1e-8


def test_bend_jacobian_jumps_at_region_end_off_axis():
    op = [bend(0.5, 0.0, -2.0, 2.0)]
    z = 0.4
    ja = jacobian((0.0, 2.0, z), op)
    jb = jacobian((0.0, 2.0 + 1e-9, z), op)
    assert abs(det3(ja) - (1 - 0.5 * z)) < 1e-12
    assert abs(det3(jb) - 1) < 1e-12


def test_order_of_operations():
    tw = twist(lambda z: 0.8 * z, lambda z: 0.8)
    tp = taper(lambda z: 1.0 - 0.4 * z, lambda z: -0.4)
    # A z-dependent taper and twist commute; a bend and a twist do not.
    p = (0.3, 0.4, 0.9)
    assert close(deform_point(p, [tp, tw]), deform_point(p, [tw, tp]), 1e-12)
    b = bend(0.6, 0.0, -1.0, 1.0)
    assert math.dist(deform_point(p, [b, tw]), deform_point(p, [tw, b])) > 1e-2
