# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feldkamp-davis-kress/. The authors are listed in prov/7MNYCN.jsonl.

import math
import random

from feldkamp_davis_kress import cone_ray, detector_coordinates, fdk, fdk_filter, filter_row, ram_lak

DIST = 3.0
A, M, D, N = 32, 13, 41, 16
TAU = 3.0 / (D - 1)
ZETA = 2.0 / (M - 1)
XS = [-1.0 + (2 * j + 1) / N for j in range(N)]
YS = [1.0 - (2 * i + 1) / N for i in range(N)]


def gauss3(src, v, c=(0.2, -0.1, 0.0), alpha=8.0):
    """Line integral of exp(-alpha |x - c|^2) along the line src + t v, with v a unit vector."""
    w = [c[i] - src[i] for i in range(3)]
    t = sum(w[i] * v[i] for i in range(3))
    d2 = sum(w[i] ** 2 for i in range(3)) - t * t
    return math.sqrt(math.pi / alpha) * math.exp(-alpha * d2)


def cylinder(src, v, c=(0.2, -0.1), r=0.4):
    """Line integral of the infinite cylinder (x - c1)^2 + (y - c2)^2 < r^2 with density 1."""
    nxy = math.hypot(v[0], v[1])
    ux, uy = v[0] / nxy, v[1] / nxy
    wx, wy = c[0] - src[0], c[1] - src[1]
    t = wx * ux + wy * uy
    d2 = wx * wx + wy * wy - t * t
    return 2.0 * math.sqrt(r * r - d2) / nxy if d2 < r * r else 0.0


def cone_data(fun, a=A, m=M, d=D):
    out = []
    for k in range(a):
        beta = 2.0 * math.pi * k / a
        proj = []
        for r in range(m):
            z = (r - (m - 1) / 2.0) * ZETA
            proj.append([fun(*cone_ray(beta, (j - (d - 1) / 2.0) * TAU, z, DIST)) for j in range(d)])
        out.append(proj)
    return out


def test_kernel_and_filter() -> None:
    assert ram_lak(0, 0.5) == 1.0 and ram_lak(2, 0.5) == 0.0
    assert abs(ram_lak(1, 0.5) + 4.0 / math.pi ** 2) < 1e-15
    kern = [ram_lak(i, 1.0) for i in range(-2, 3)]
    q = filter_row([0.0, 1.0, 0.0], kern, 1.0)
    assert q == [kern[1], kern[2], kern[3]]
    # one projection with a single nonzero entry at (t, z) = (0, 0): weight 1, kernel h / 2
    data = [[[0.0] * 5 for _ in range(3)]]
    data[0][1][2] = 1.0
    out = fdk_filter(data, DIST, 0.5, 0.5)
    assert out[0][0] == [0.0] * 5 and out[0][2] == [0.0] * 5
    assert all(abs(out[0][1][j] - 0.25 * ram_lak(j - 2, 0.5)) < 1e-15 for j in range(5))


def test_ray_geometry() -> None:
    rng = random.Random(3)
    for _ in range(50):
        x, y, z = rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)
        beta = rng.uniform(0, 2 * math.pi)
        u, tp, zp = detector_coordinates(x, y, z, beta, DIST)
        src, v = cone_ray(beta, tp, zp, DIST)
        w = (x - src[0], y - src[1], z - src[2])
        cross = (w[1] * v[2] - w[2] * v[1], w[2] * v[0] - w[0] * v[2], w[0] * v[1] - w[1] * v[0])
        assert max(abs(c) for c in cross) < 1e-12
        # D U is the depth of the point along the central ray
        depth = (-src[0]) * w[0] + (-src[1]) * w[1]
        assert abs(depth / DIST - DIST * u) < 1e-12


def test_gaussian_blob() -> None:
    vol = fdk(cone_data(gauss3), DIST, TAU, ZETA, N, [0.0, 0.25])
    for sl, h in enumerate([0.0, 0.25]):
        for i in range(N):
            for j in range(N):
                want = math.exp(-8.0 * ((XS[j] - 0.2) ** 2 + (YS[i] + 0.1) ** 2 + h * h))
                assert abs(vol[sl][i][j] - want) < 0.03


def test_mid_plane_uses_only_the_mid_row() -> None:
    rng = random.Random(11)
    data = cone_data(gauss3)
    changed = [[row if r == (M - 1) // 2 else [rng.uniform(-3, 3) for _ in row] for r, row in enumerate(p)] for p in data]
    assert fdk(changed, DIST, TAU, ZETA, N, [0.0]) == fdk(data, DIST, TAU, ZETA, N, [0.0])


def test_z_invariant_object_is_exact_at_every_height() -> None:
    vol = fdk(cone_data(cylinder), DIST, TAU, ZETA, N, [0.0, 0.3, -0.45])
    for i in range(N):
        for j in range(N):
            assert abs(vol[1][i][j] - vol[0][i][j]) < 1e-9
            assert abs(vol[2][i][j] - vol[0][i][j]) < 1e-9
            r = math.hypot(XS[j] - 0.2, YS[i] + 0.1)
            if r < 0.3:
                assert abs(vol[0][i][j] - 1.0) < 0.05
            elif r > 0.55:
                # 32 views of a sharp edge leave small streaks outside the object
                assert abs(vol[0][i][j]) < 0.2


def test_linearity() -> None:
    d1 = cone_data(gauss3, a=8)
    d2 = cone_data(cylinder, a=8)
    mix = [[[2.0 * u - 0.5 * v for u, v in zip(r1, r2)] for r1, r2 in zip(p1, p2)] for p1, p2 in zip(d1, d2)]
    v1 = fdk(d1, DIST, TAU, ZETA, 4, [0.2])
    v2 = fdk(d2, DIST, TAU, ZETA, 4, [0.2])
    vm = fdk(mix, DIST, TAU, ZETA, 4, [0.2])
    for i in range(4):
        for j in range(4):
            assert abs(vm[0][i][j] - (2.0 * v1[0][i][j] - 0.5 * v2[0][i][j])) < 1e-12
