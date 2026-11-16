# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harris-affine-detector/. The authors are listed in prov/3SB3Q7.jsonl.

import math
import random

from harris_affine_detector import (
    adapt_point,
    gaussian_kernel,
    harris_affine,
    moments,
    sym_eig,
    sym_inv,
    sym_inv_sqrt,
    sym_sqrt,
    warp,
)


def mul(m, n):
    return [[sum(m[i][k] * n[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def full(s):
    return [[s[0], s[1]], [s[1], s[2]]]


def ablob(n, cx, cy, s1, s2, th):
    c, s = math.cos(th), math.sin(th)
    sig = (c * c * s1 * s1 + s * s * s2 * s2, c * s * (s1 * s1 - s2 * s2), s * s * s1 * s1 + c * c * s2 * s2)
    ia, ib, ic = sym_inv(sig)
    img = [[math.exp(-0.5 * (ia * (u - cx) ** 2 + 2 * ib * (u - cx) * (v - cy) + ic * (v - cy) ** 2))
            for u in range(n)] for v in range(n)]
    return img, sig


def shape(U):
    a, b, c = U
    s = (a * a + b * b, a * b + b * c, b * b + c * c)
    return [x / (s[0] + s[2]) for x in s]


def test_two_by_two_algebra_against_definitions():
    rng = random.Random(1997)
    for _ in range(600):
        a, c = rng.uniform(0.01, 5), rng.uniform(0.01, 5)
        b = rng.uniform(-0.99, 0.99) * math.sqrt(a * c)
        m = (a, b, c)
        r = full(sym_sqrt(m))
        rr = mul(r, r)
        assert all(abs(rr[i][j] - full(m)[i][j]) < 1e-9 * (a + c) for i in range(2) for j in range(2))
        assert min(sym_eig(sym_sqrt(m))) > 0
        q = full(sym_inv_sqrt(m))
        e = mul(mul(q, full(m)), q)
        assert all(abs(e[i][j] - (i == j)) < 1e-7 for i in range(2) for j in range(2))
        lo, hi = sym_eig(m)
        for lam in (lo, hi):
            assert abs((a - lam) * (c - lam) - b * b) < 1e-9 * (a + c) ** 2
        assert lo <= hi


def test_warp_is_exact_on_linear_images():
    rng = random.Random(7)
    for _ in range(200):
        g, k, o = rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-1, 1)
        img = [[g * u + k * v + o for u in range(30)] for v in range(30)]
        x, y = rng.uniform(12, 17), rng.uniform(12, 17)
        U = (rng.uniform(0.5, 1), rng.uniform(-0.3, 0.3), rng.uniform(0.5, 1))
        P = warp(img, x, y, U, 4)
        for q in range(-4, 5):
            for p in range(-4, 5):
                want = g * (x + U[0] * p + U[1] * q) + k * (y + U[1] * p + U[2] * q) + o
                assert abs(P[q + 4][p + 4] - want) < 1e-9
    img = [[float(u * 31 + v) for u in range(9)] for v in range(9)]
    assert warp(img, 4.0, 4.0, (1.0, 0.0, 1.0), 2) == [row[2:7] for row in img[2:7]]


def test_moments_match_direct_sums():
    rng = random.Random(3)
    P = [[rng.random() for _ in range(31)] for _ in range(31)]
    si, sd = 1.5, 1.0
    kd, ki = gaussian_kernel(sd), gaussian_kernel(si)
    rd, ri = len(kd) // 2, len(ki) // 2

    def L(u, v):
        return sum(kd[i + rd] * kd[j + rd] * P[v + j][u + i] for i in range(-rd, rd + 1) for j in range(-rd, rd + 1))

    mom = moments(P, si, sd)
    for (p, q), (m, det_h) in mom.items():
        A = B = C = 0.0
        for j in range(-ri, ri + 1):
            for i in range(-ri, ri + 1):
                u, v, w = 15 + p + i, 15 + q + j, ki[i + ri] * ki[j + ri]
                gx, gy = (L(u + 1, v) - L(u - 1, v)) / 2, (L(u, v + 1) - L(u, v - 1)) / 2
                A, B, C = A + w * gx * gx, B + w * gx * gy, C + w * gy * gy
        assert all(abs(x - sd * sd * y) < 1e-12 for x, y in zip(m, (A, B, C)))
        u, v = 15 + p, 15 + q
        dxx = L(u + 1, v) - 2 * L(u, v) + L(u - 1, v)
        dyy = L(u, v + 1) - 2 * L(u, v) + L(u, v - 1)
        dxy = (L(u + 1, v + 1) - L(u - 1, v + 1) - L(u + 1, v - 1) + L(u - 1, v - 1)) / 4
        assert abs(det_h - sd ** 4 * (dxx * dyy - dxy * dxy)) < 1e-12


def test_worked_example_anisotropic_blob():
    img, sig = ablob(41, 20, 20, 3.0, 1.5, math.pi / 6)
    x, y, s, U = adapt_point(img, 20.0, 20.0, 2.0, measure="hessian")
    assert (x, y) == (20.0, 20.0)
    assert abs(s - 2.796) < 1e-3
    lo, hi = sym_eig(U)
    assert abs(hi - 1.0) < 1e-12
    assert abs(lo - 0.5135) < 1e-3
    a, b, c = U
    assert abs(0.5 * math.degrees(math.atan2(2 * b, a - c)) - 30.0) < 0.1
    want = [z / (sig[0] + sig[2]) for z in sig]
    assert all(abs(g - w) < 0.01 for g, w in zip(shape(U), want))
    assert adapt_point(img, 20.0, 20.0, 2.0, measure="hessian", max_iter=1) is None


def test_isotropic_blob_needs_one_step():
    img, _ = ablob(31, 15, 15, 2.5, 2.5, 0.0)
    x, y, s, U = adapt_point(img, 15.0, 15.0, 2.0, measure="hessian", max_iter=1)
    assert (x, y) == (15.0, 15.0)
    assert abs(U[0] - 1) < 1e-9 and abs(U[1]) < 1e-9 and abs(U[2] - 1) < 1e-9


def test_rotation_by_90_degrees():
    img, _ = ablob(35, 17, 17, 2.5, 1.4, 0.4)
    h = len(img)
    rot = [[img[h - 1 - j][i] for j in range(h)] for i in range(h)]
    x, y, s, U = adapt_point(img, 17.0, 17.0, 2.0, measure="hessian")
    x2, y2, s2, U2 = adapt_point(rot, 17.0, 17.0, 2.0, measure="hessian")
    assert (x2, y2) == (17.0, 17.0) and abs(s - s2) < 1e-9
    # The rotated image has I'(u', v') = I(v', h - 1 - u'), so U' = A^T U A with A = [[0, 1], [-1, 0]].
    assert abs(U2[0] - U[2]) < 1e-9 and abs(U2[1] + U[1]) < 1e-9 and abs(U2[2] - U[0]) < 1e-9


def test_edges_and_flat_regions_are_rejected():
    edge = [[1.0 if u >= 15 else 0.0 for u in range(31)] for v in range(31)]
    flat = [[0.3] * 31 for _ in range(31)]
    img, _ = ablob(31, 15, 15, 2.5, 1.5, 0.3)
    assert adapt_point(edge, 15.0, 15.0, 2.0) is None
    assert adapt_point(flat, 15.0, 15.0, 2.0) is None
    out = harris_affine(img, [(15.0, 15.0, 2.0)], measure="hessian")
    assert len(out) == 1 and out[0][:2] == (15.0, 15.0)
