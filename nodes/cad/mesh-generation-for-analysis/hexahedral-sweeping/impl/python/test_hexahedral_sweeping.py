# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hexahedral-sweeping/. The authors are listed in prov/AETFHW.jsonl.

import random
from fractions import Fraction as F

import pytest

from hexahedral_sweeping import certify, grid_mesh, planar_layer, slab_coefficients, sweep
from mg4geom import (
    FACES,
    REF,
    corner_jacobians,
    det3,
    hex_volume,
    jacobian_bernstein,
    jacobian_det,
    sub,
    trilinear,
)

CENTER = (1, 1)


def about(pts, loop, a, z, c=CENTER):
    t = (c[0] - a[0][0] * c[0] - a[0][1] * c[1], c[1] - a[1][0] * c[0] - a[1][1] * c[1])
    return planar_layer(pts, loop, a, t, z)


def page_example():
    pts, quads, loop = grid_mesh([0, 1, 2], [0, 1, 2])
    a0 = [[1, 0], [0, 1]]
    a1 = [[F(1), F(-1, 2)], [F(1, 2), F(1)]]
    a2 = [[0, -1], [1, 0]]
    layers = [about(pts, loop, a0, 0), about(pts, loop, a1, 1), about(pts, loop, a2, 2)]
    return pts, quads, loop, layers


def test_reference_tables():
    cube = [tuple(F(c) for c in p) for p in REF]
    assert corner_jacobians(cube) == [1] * 8
    assert hex_volume(cube) == 1
    assert all(c == 1 for c in jacobian_bernstein(cube))
    for f in FACES:
        p = [cube[i] for i in f]
        n = det3(sub(p[1], p[0]), sub(p[3], p[0]), sub(p[0], (F(1, 2), F(1, 2), F(1, 2))))
        assert n > 0  # each face is counterclockwise seen from outside


def test_page_example():
    pts, quads, loop, layers = page_example()
    nodes, hexes, maps, ok = sweep(pts, quads, loop, layers)
    assert ok and certify(pts, loop, nodes, maps)
    assert len(hexes) == 8
    assert nodes[1][4] == (1, 1, 1) and nodes[1][0] == (F(1, 2), F(-1, 2), 1)
    for h in hexes[:4]:
        assert corner_jacobians(h) == [1, 1, 1, 1, F(5, 4), F(5, 4), F(5, 4), F(5, 4)]
        assert hex_volume(h) == F(13, 12)
    for h in hexes[4:]:
        assert corner_jacobians(h) == [F(5, 4)] * 4 + [1] * 4
        assert hex_volume(h) == F(11, 12)
    assert sum(hex_volume(h) for h in hexes) == 8
    assert slab_coefficients(maps[0], maps[1], pts[0]) == (1, 1, F(5, 4))
    assert slab_coefficients(maps[1], maps[2], pts[0]) == (F(5, 4), F(1, 2), 1)
    # the target face mesh is the source mesh turned by 90 degrees about (1, 1)
    for v, (x, y) in enumerate(pts):
        assert nodes[2][v] == (2 - y, x, 2)


def test_half_turn_has_positive_corners_but_is_not_valid():
    pts, quads, loop = grid_mesh([0, 1, 2], [0, 1, 2])
    layers = [about(pts, loop, [[1, 0], [0, 1]], 0), about(pts, loop, [[-1, 0], [0, -1]], 1)]
    nodes, hexes, maps, ok = sweep(pts, quads, loop, layers)
    assert ok  # all 8 corner Jacobians are positive
    assert not certify(pts, loop, nodes, maps)
    half = F(1, 2)
    for h in hexes:
        assert corner_jacobians(h) == [1] * 8
        assert jacobian_det(h, half, half, half) == 0
        assert trilinear(h, half, half, half) == (1, 1, half)  # every hex passes through the axis point
        assert hex_volume(h) == F(1, 3)


def test_stretched_half_turn_is_inverted_inside():
    pts, quads, loop = grid_mesh([0, 1, 2], [0, 1, 2])
    layers = [about(pts, loop, [[1, 0], [0, 1]], 0), about(pts, loop, [[-1, 0], [0, -2]], 1)]
    nodes, hexes, maps, ok = sweep(pts, quads, loop, layers)
    assert ok and not certify(pts, loop, nodes, maps)
    w = F(2, 5)  # det((1 - w) I + w diag(-1, -2)) = (1 - 2w)(1 - 3w) < 0
    assert all(jacobian_det(h, F(1, 2), F(1, 2), w) < 0 for h in hexes)


def test_boundary_nodes_are_kept_and_corner_check_is_exact():
    pts, quads, loop = grid_mesh([0, 1, 3], [0, 2, 3])
    l0 = about(pts, loop, [[1, 0], [0, 1]], 0)
    l1 = [(x + (F(1, 3) if i == 2 else 0), y, z) for i, (x, y, z) in enumerate(about(pts, loop, [[1, 0], [0, 1]], 1))]
    nodes, hexes, maps, ok = sweep(pts, quads, loop, [l0, l1])
    for i, v in enumerate(loop):
        assert nodes[1][v] == l1[i]
    assert ok == all(d > 0 for h in hexes for d in corner_jacobians(h))
    assert not certify(pts, loop, nodes, maps)  # layer 1 is not an affine image


def test_rejects_collinear_loop():
    pts = [(F(0), F(0)), (F(1), F(0)), (F(2), F(0))]
    with pytest.raises(ValueError):
        sweep(pts, [], [0, 1, 2], [[(0, 0, 0)] * 3, [(0, 0, 1)] * 3])


def random_instance(rng):
    nx, ny = rng.randint(2, 4), rng.randint(2, 4)
    xs = sorted(rng.sample(range(0, 9), nx))
    ys = sorted(rng.sample(range(0, 9), ny))
    pts, quads, loop = grid_mesh(xs, ys)
    k = rng.randint(1, 3)
    zs = [0]
    for _ in range(k):
        zs.append(zs[-1] + rng.randint(1, 3))
    mats = [[[1, 0], [0, 1]]]
    for _ in range(k):
        while True:
            a = [[F(rng.randint(-4, 4), 2) for _ in range(2)] for _ in range(2)]
            if a[0][0] * a[1][1] - a[0][1] * a[1][0] > 0:
                break
        mats.append(a)
    ts = [(0, 0)] + [(F(rng.randint(-4, 4), 2), F(rng.randint(-4, 4), 2)) for _ in range(k)]
    layers = [planar_layer(pts, loop, a, t, z) for a, t, z in zip(mats, ts, zs)]
    return pts, quads, loop, mats, ts, zs, layers


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def oracle_slab_positive(a0, a1):
    """min over w in [0, 1] of det((1 - w) A0 + w A1) > 0, by exact minimization of the quadratic."""
    m = lambda w: [[(1 - w) * a0[i][j] + w * a1[i][j] for j in range(2)] for i in range(2)]
    q0, qh, q1 = det2(m(F(0))), det2(m(F(1, 2))), det2(m(F(1)))
    # q(w) = q0 + b w + c w^2 from three samples
    c = 2 * (q0 + q1 - 2 * qh)
    b = q1 - q0 - c
    cands = [F(0), F(1)]
    if c != 0:
        w = -b / (2 * c)
        if 0 < w < 1:
            cands.append(w)
    return min(q0 + b * w + c * w * w for w in cands) > 0


def test_random_sweeps_against_oracles():
    rng = random.Random(20261115)
    certified = 0
    for trial in range(500):
        pts, quads, loop, mats, ts, zs, layers = random_instance(rng)
        nodes, hexes, maps, ok = sweep(pts, quads, loop, layers)
        # every layer is the exact affine image, so the fit is exact and the target mesh matches
        for k, (a, t, z) in enumerate(zip(mats, ts, zs)):
            for v, (x, y) in enumerate(pts):
                assert nodes[k][v] == (a[0][0] * x + a[0][1] * y + t[0], a[1][0] * x + a[1][1] * y + t[1], z)
        assert len(hexes) == (len(zs) - 1) * len(quads)
        assert ok == all(d > 0 for h in hexes for d in corner_jacobians(h))
        # the certificate agrees with an exact minimization of det((1 - w) A_k + w A_k+1)
        expect = all(oracle_slab_positive(mats[k], mats[k + 1]) for k in range(len(mats) - 1))
        cert = certify(pts, loop, nodes, maps)
        assert cert == expect
        if trial % 5 == 0:
            # the hex volumes add up to area times the integral of the slab determinant
            area = (pts[-1][0] - pts[0][0]) * (pts[-1][1] - pts[0][1])
            vol = 0
            for k in range(len(mats) - 1):
                a0, a1 = mats[k], mats[k + 1]
                mid = (a0[0][0] * a1[1][1] - a0[1][0] * a1[0][1] + a1[0][0] * a0[1][1] - a1[1][0] * a0[0][1]) / F(2)
                vol += area * (zs[k + 1] - zs[k]) * (det2(a0) + mid + det2(a1)) / 3
            assert sum(hex_volume(h) for h in hexes) == vol
        if cert:
            certified += 1
            assert ok
            for h in hexes[:3]:
                for _ in range(3):
                    u, v, w = (F(rng.randint(0, 8), 8) for _ in range(3))
                    assert jacobian_det(h, u, v, w) > 0
    assert certified > 100
