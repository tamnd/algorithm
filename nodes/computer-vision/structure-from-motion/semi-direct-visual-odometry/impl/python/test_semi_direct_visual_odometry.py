# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-direct-visual-odometry/. The authors are listed in prov/BR51JE.jsonl.
"""Tests for semi_direct_visual_odometry.

Most tests use an analytic image: the exact image of a textured plane, so
the steps can be checked to high accuracy. The depth filter update is
compared with moments computed by numerical integration. The last test runs
the whole pipeline on pixel grids.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import semi_direct_visual_odometry as svo  # noqa: E402
from cvla import matvec, mul, norm, transpose  # noqa: E402

K = (40.0, 40.0, 23.5, 17.5)
W, H = 48, 36
IDENT = (svo.eye(3), [0.0, 0.0, 0.0])


def radiance(x, y):
    return (120.0 + 35.0 * math.sin(1.3 * x + 0.5 * y) + 30.0 * math.cos(0.7 * x - 1.6 * y)
            + 25.0 * math.sin(2.1 * x + 1.5 * y) + 20.0 * math.cos(1.9 * x - 2.4 * y))


class Plane:
    """The world plane Z = z0 + sx X with the texture radiance(X, Y)."""

    def __init__(self, z0, sx=0.0):
        self.z0, self.sx = z0, sx

    def depth(self, pose, u, v, Kl=K):
        fx, fy, cx, cy = Kl
        c = svo.center(pose)
        ray = matvec(transpose(pose[0]), [(u - cx) / fx, (v - cy) / fy, 1.0])
        return (self.z0 + self.sx * c[0] - c[2]) / (ray[2] - self.sx * ray[0])


class AnalyticImage:
    """The exact image L + b of a plane seen by a camera, with
    central-difference gradients and the border rule of GridImage."""

    def __init__(self, plane, pose, b=0.0, Kl=K, w=W, h=H):
        self.plane, self.Kl, self.w, self.h, self.b = plane, Kl, w, h, b
        self.rt, self.c = transpose(pose[0]), svo.center(pose)

    def value(self, u, v):
        fx, fy, cx, cy = self.Kl
        x, y = (u - cx) / fx, (v - cy) / fy
        rt, c, pl = self.rt, self.c, self.plane
        ray = [rt[i][0] * x + rt[i][1] * y + rt[i][2] for i in range(3)]
        s = (pl.z0 + pl.sx * c[0] - c[2]) / (ray[2] - pl.sx * ray[0])
        return radiance(c[0] + s * ray[0], c[1] + s * ray[1]) + self.b

    def sample(self, u, v):
        if not (1.0 <= u <= self.w - 2.0 and 1.0 <= v <= self.h - 2.0):
            return None
        e = 1e-4
        return (self.value(u, v), (self.value(u + e, v) - self.value(u - e, v)) / (2 * e),
                (self.value(u, v + e) - self.value(u, v - e)) / (2 * e))


def analytic_pyramid(plane, pose, levels):
    return [AnalyticImage(plane, pose, 0.0, svo.level_K(K, l), W >> l, H >> l) for l in range(levels)]


def make_pose(w, c):
    R = svo.so3_exp(w)
    return R, [-x for x in matvec(R, c)]


def pose_err(p, q):
    rd = mul(p[0], transpose(q[0]))
    ang = 2.0 * math.asin(min(1.0, norm([[rd[i][j] - (i == j) for j in range(3)] for i in range(3)]) / math.sqrt(8)))
    return ang, norm([a - b for a, b in zip(p[1], q[1])])


def grid(step, margin=7):
    return [(float(u), float(v)) for v in range(margin, H - margin, step) for u in range(margin, W - margin, step)]


def test_inverse_compositional_jacobian():
    plane = Plane(5.0)
    img = AnalyticImage(plane, IDENT)
    feats = [(17.3, 12.6, 5.0), (30.2, 21.4, 5.0)]
    rows = svo.sparse_alignment_setup(img, K, feats)
    assert len(rows) == 2 * 16
    e = 1e-6
    for X, iref, J in rows[::7]:
        p = svo.project(K, X)
        assert abs(img.sample(*p)[0] - iref) < 1e-9
        for k in range(6):
            d = [0.0] * 6
            d[k] = e
            hi = img.sample(*svo.project(K, svo.transform(svo.increment(d), X)))[0]
            d[k] = -e
            lo = img.sample(*svo.project(K, svo.transform(svo.increment(d), X)))[0]
            num = (hi - lo) / (2 * e)
            assert abs(num - J[k]) <= 1e-4 * (1.0 + abs(num))


def test_sparse_image_alignment_recovers_motion():
    plane = Plane(5.0)
    truth = make_pose([0.004, -0.007, 0.003], [0.1, -0.05, 0.12])
    rp, cp = analytic_pyramid(plane, IDENT, 2), analytic_pyramid(plane, truth, 2)
    feats = [(u, v, 5.0) for u, v in grid(6)]
    T = svo.sparse_image_alignment(rp, cp, K, feats, IDENT)
    ang, dt = pose_err(T, truth)
    assert ang < 1e-7 and dt < 1e-6


def test_affine_warp_and_feature_alignment():
    plane = Plane(5.0)
    # moving toward a fronto-parallel plane scales the image by z / (z - 1)
    A = svo.affine_warp(K, IDENT, make_pose([0, 0, 0], [0.0, 0.0, 1.0]), (20.0, 15.0), 5.0)
    assert abs(A[0][0] - 1.25) < 1e-9 and abs(A[1][1] - 1.25) < 1e-9
    assert abs(A[0][1]) < 1e-9 and abs(A[1][0]) < 1e-9
    # a sideways move shifts the image by f t / z; the 2D alignment finds it
    # from a start 1.3 pixels away, with a brightness offset of 6
    cur = make_pose([0, 0, 0], [0.3, -0.2, 0.0])
    ref_img, cur_img = AnalyticImage(plane, IDENT), AnalyticImage(plane, cur, 6.0)
    A = svo.affine_warp(K, IDENT, cur, (20.0, 15.0), 5.0)
    assert abs(A[0][0] - 1) < 1e-9 and abs(A[1][1] - 1) < 1e-9
    want = (20.0 - 40.0 * 0.3 / 5.0, 15.0 + 40.0 * 0.2 / 5.0)
    (u, v), rms = svo.feature_alignment(cur_img, ref_img, (20.0, 15.0), A, (want[0] + 1.0, want[1] - 0.8))
    assert abs(u - want[0]) < 1e-6 and abs(v - want[1]) < 1e-6
    assert rms < 1e-6


def test_motion_only_ba():
    rng = random.Random(4)
    truth = make_pose([0.02, -0.03, 0.01], [0.3, 0.1, -0.2])
    obs = []
    for _ in range(20):
        X = [rng.uniform(-2, 2), rng.uniform(-1.5, 1.5), rng.uniform(4, 8)]
        obs.append((X, svo.project(K, svo.transform(truth, X))))
    start = (mul(svo.so3_exp([0.02, 0.01, -0.015]), truth[0]), [a + b for a, b in zip(truth[1], [0.05, -0.04, 0.06])])
    pose, hist = svo.motion_only_ba(K, start, obs)
    assert all(x > y for x, y in zip(hist, hist[1:]))
    ang, dt = pose_err(pose, truth)
    assert ang < 1e-9 and dt < 1e-9


def test_structure_only_ba():
    X = [0.4, -0.3, 5.5]
    poses = [IDENT, make_pose([0, 0.02, 0], [0.3, 0, 0]), make_pose([0.01, 0, 0], [0.5, 0.1, 0.05])]
    obs = [(p, svo.project(K, svo.transform(p, X))) for p in poses]
    got = svo.structure_only_ba(K, [0.5, -0.2, 6.0], obs, iters=10)
    assert norm([a - b for a, b in zip(got, X)]) < 1e-9


def simpson(f, a, b, n=2000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def test_depth_filter_update_matches_numerical_moments():
    seed = svo.Seed(0, 10.0, 10.0, mu=0.25, z_range=0.5, a=6.0, b=3.0)
    seed.sigma2 = 0.04 ** 2
    a, b, mu, s2, zr = seed.a, seed.b, seed.mu, seed.sigma2, seed.z_range
    x, tau2 = 0.28, 0.03 ** 2
    seed.update(x, tau2)
    # posterior p(Z, pi) ~ (pi N(x | Z, tau2) + (1 - pi) / zr) N(Z | mu, s2) Beta(pi | a, b)
    beta = math.gamma(a + b) / (math.gamma(a) * math.gamma(b))

    def bpdf(p):
        return beta * p ** (a - 1) * (1 - p) ** (b - 1)

    def zpdf(z):
        return svo.gauss_pdf(z, mu, math.sqrt(s2))

    lo, hi = mu - 12 * math.sqrt(s2), mu + 12 * math.sqrt(s2)
    zin = [simpson(lambda z, k=k: z ** k * svo.gauss_pdf(x, z, math.sqrt(tau2)) * zpdf(z), lo, hi) for k in range(3)]
    zout = [simpson(lambda z, k=k: z ** k * zpdf(z) / zr, lo, hi) for k in range(3)]
    pin = [simpson(lambda p, k=k: p ** (k + 1) * bpdf(p), 0, 1) for k in range(3)]
    pout = [simpson(lambda p, k=k: p ** k * (1 - p) * bpdf(p), 0, 1) for k in range(3)]
    norm0 = zin[0] * pin[0] + zout[0] * pout[0]
    ez = (zin[1] * pin[0] + zout[1] * pout[0]) / norm0
    ez2 = (zin[2] * pin[0] + zout[2] * pout[0]) / norm0
    ep = (zin[0] * pin[1] + zout[0] * pout[1]) / norm0
    ep2 = (zin[0] * pin[2] + zout[0] * pout[2]) / norm0
    assert abs(seed.mu - ez) < 1e-9
    assert abs(seed.sigma2 - (ez2 - ez * ez)) < 1e-9
    fa, fb = seed.a, seed.b
    assert abs(fa / (fa + fb) - ep) < 1e-8
    assert abs(fa * (fa + 1) / ((fa + fb) * (fa + fb + 1)) - ep2) < 1e-8


def test_depth_filter_converges_and_rejects_outliers():
    rng = random.Random(11)
    seed = svo.Seed(0, 10.0, 10.0, mu=0.3, z_range=0.5)
    for k in range(40):
        if k % 4 == 3:
            seed.update(rng.uniform(0.0, 0.5), 0.01 ** 2)
        else:
            seed.update(rng.gauss(0.2, 0.01), 0.01 ** 2)
    assert abs(seed.mu - 0.2) < 0.005
    assert math.sqrt(seed.sigma2) < 0.003
    assert 0.6 < seed.a / (seed.a + seed.b) < 0.9
    bad = svo.Seed(0, 10.0, 10.0, mu=0.3, z_range=0.5)
    for _ in range(20):
        bad.update(rng.uniform(0.0, 0.5), 0.01 ** 2)
    # pure outliers push the inlier ratio down from its start of 0.5
    assert bad.a / (bad.a + bad.b) < 0.4


def test_epipolar_measurement_and_depth_along_ray():
    rel = make_pose([0.01, -0.02, 0.005], [0.4, 0.1, -0.1])
    Xr = [0.3, -0.2, 4.0]
    fr = [Xr[0] / Xr[2], Xr[1] / Xr[2], 1.0]
    Xc = svo.transform(rel, Xr)
    assert abs(svo.depth_along_ray(fr, [Xc[0] / Xc[2], Xc[1] / Xc[2], 1.0], rel) - 4.0) < 1e-12
    plane = Plane(4.0)
    cur = make_pose([0, 0, 0], [0.35, 0.05, 0.0])
    seed = svo.Seed(0, 22.0, 16.0, mu=0.3, z_range=0.5)
    x, tau2 = svo.epipolar_measurement(K, AnalyticImage(plane, IDENT), AnalyticImage(plane, cur, 4.0), IDENT, cur, seed)
    assert abs(x - 0.25) < 1e-6
    # one pixel along the epipolar line is 1 / (f |t|) in inverse depth for this motion
    assert abs(math.sqrt(tau2) - 1.0 / (40.0 * math.hypot(0.35, 0.05))) < 1e-9


def test_needs_keyframe_by_hand():
    kfs = [IDENT, make_pose([0, 0, 0], [1.0, 0.0, 0.0])]
    assert not svo.needs_keyframe(make_pose([0, 0, 0], [0.5, 0.0, 0.0]), kfs, 5.0)  # 0.5 < 0.6
    assert svo.needs_keyframe(make_pose([0, 0, 0], [0.5, 0.7, 0.0]), kfs, 5.0)


def test_shi_tomasi_cells():
    flat = svo.GridImage([[80.0] * 32 for _ in range(32)])
    assert svo.shi_tomasi_cells(flat, 16, 1.0) == []
    # a bright square with one corner in each 16 x 16 cell; straight edges
    # have a zero smaller eigenvalue, so only the corners are found
    sq = svo.GridImage([[200.0 if 8 <= u < 24 and 8 <= v < 24 else 0.0 for u in range(32)] for v in range(32)])
    got = svo.shi_tomasi_cells(sq, 16, 1.0)
    assert len(got) == 4 and len({(u // 16, v // 16) for u, v in got}) == 4
    for u, v in got:
        assert min(abs(u - 7.5), abs(u - 23.5)) <= 1.5 and min(abs(v - 7.5), abs(v - 23.5)) <= 1.5
    assert svo.shi_tomasi_cells(sq, 16, 1.0, taken=[(20.0, 20.0)]) == [p for p in got if (p[0] // 16, p[1] // 16) != (1, 1)]


def test_run_svo_on_pixel_grids():
    # Bilinear sampling of a pixel grid is not the true image, so the
    # estimates are not exact here; the bounds are loose on purpose.
    plane = Plane(5.0, 0.1)
    n = 8
    truth = [make_pose([0.0, 0.003 * k, 0.001 * k], [0.12 * k, 0.02 * k, 0.03 * k]) for k in range(n)]
    frames = []
    for pose in truth:
        img = AnalyticImage(plane, pose)
        frames.append(svo.GridImage([[img.value(u, v) for u in range(W)] for v in range(H)]))
    out = svo.run_svo(frames, K, lambda u, v: plane.depth(IDENT, u, v), levels=2, cell=8, kf_ratio=0.05,
                      converge=50.0, px_sigma=0.2)
    assert len(out["keyframes"]) >= 3
    assert out["added"] > 0  # some seeds converged and became map points
    path = sum(norm([a - b for a, b in zip(svo.center(truth[k]), svo.center(truth[k - 1]))]) for k in range(1, n))
    for k in range(n):
        ang, _ = pose_err(out["poses"][k], truth[k])
        dc = norm([a - b for a, b in zip(svo.center(out["poses"][k]), svo.center(truth[k]))])
        assert ang < math.radians(1.0)
        assert dc < 0.1 * path
