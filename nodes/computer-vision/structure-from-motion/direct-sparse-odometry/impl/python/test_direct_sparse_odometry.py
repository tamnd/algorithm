# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-sparse-odometry/. The authors are listed in prov/YH2YPH.jsonl.
"""Tests for direct_sparse_odometry.

Most tests use an analytic image: the exact image of a textured plane, so a
correct estimate makes every residual zero and the estimates can be checked
to high accuracy. The last test runs the whole pipeline on pixel grids.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import direct_sparse_odometry as dso  # noqa: E402
from cvla import matvec, mul, norm, solve, transpose  # noqa: E402

K = (40.0, 40.0, 23.5, 17.5)
W, H = 48, 36


def radiance(x, y):
    return (120.0 + 35.0 * math.sin(1.3 * x + 0.5 * y) + 30.0 * math.cos(0.7 * x - 1.6 * y)
            + 25.0 * math.sin(2.1 * x + 1.5 * y) + 20.0 * math.cos(1.9 * x - 2.4 * y))


class Plane:
    """The world plane Z = z0 + sx X with the texture radiance(X, Y)."""

    def __init__(self, z0, sx=0.0):
        self.z0, self.sx = z0, sx

    def hit(self, pose, Kl, u, v):
        R, t = pose
        fx, fy, cx, cy = Kl
        c = dso.center(pose)
        ray = matvec(transpose(R), [(u - cx) / fx, (v - cy) / fy, 1.0])
        s = (self.z0 + self.sx * c[0] - c[2]) / (ray[2] - self.sx * ray[0])
        return [c[i] + s * ray[i] for i in range(3)], s

    def inv_depth(self, pose, u, v):
        return 1.0 / self.hit(pose, K, u, v)[1]


class AnalyticImage:
    """The exact image exp(a) L + b of a plane seen by a camera, with
    central-difference gradients. It has the same border rule as GridImage."""

    def __init__(self, plane, pose, a, b, Kl=K, w=W, h=H):
        self.plane, self.pose, self.a, self.b, self.Kl, self.w, self.h = plane, pose, a, b, Kl, w, h
        self.rt, self.c, self.gain = transpose(pose[0]), dso.center(pose), math.exp(a)

    def value(self, u, v):
        fx, fy, cx, cy = self.Kl
        x, y = (u - cx) / fx, (v - cy) / fy
        rt, c, pl = self.rt, self.c, self.plane
        ray = [rt[i][0] * x + rt[i][1] * y + rt[i][2] for i in range(3)]
        s = (pl.z0 + pl.sx * c[0] - c[2]) / (ray[2] - pl.sx * ray[0])
        return self.gain * radiance(c[0] + s * ray[0], c[1] + s * ray[1]) + self.b

    def sample(self, u, v):
        if not (1.0 <= u <= self.w - 2.0 and 1.0 <= v <= self.h - 2.0):
            return None
        e = 1e-4
        return (self.value(u, v), (self.value(u + e, v) - self.value(u - e, v)) / (2 * e),
                (self.value(u, v + e) - self.value(u, v - e)) / (2 * e))


def analytic_pyramid(plane, state, levels):
    pose, a, b = state
    return [AnalyticImage(plane, pose, a, b, dso.level_K(K, l), W >> l, H >> l) for l in range(levels)]


def make_pose(w, c):
    R = dso.so3_exp(w)
    return R, [-x for x in matvec(R, c)]


def pose_err(p, q):
    rd = mul(p[0], transpose(q[0]))
    ang = 2.0 * math.asin(min(1.0, norm([[rd[i][j] - (i == j) for j in range(3)] for i in range(3)]) / math.sqrt(8)))
    return ang, norm([a - b for a, b in zip(p[1], q[1])])


def grid_points(step, margin=6):
    return [(float(u), float(v)) for v in range(margin, H - margin, step) for u in range(margin, W - margin, step)]


IDENT = (dso.eye(3), [0.0, 0.0, 0.0])


def test_jacobians_match_finite_differences():
    plane = Plane(5.0, 0.2)
    host = (make_pose([0.02, -0.03, 0.01], [0.1, -0.2, 0.3]), 0.15, 4.0)
    tgt = (make_pose([-0.01, 0.04, 0.02], [0.4, 0.1, 0.2]), -0.1, -3.0)
    himg = AnalyticImage(plane, *host)
    timg = AnalyticImage(plane, *tgt)
    q, d = (21.3, 16.7), 0.21
    r, _, _, jt, jh, jd = dso.residual(himg, timg, K, q, d, host, tgt, True)
    e = 1e-6

    def r_of(h, t, dd):
        return dso.residual(himg, timg, K, q, dd, h, t)[0]

    def bump(state, k, s):
        pose, a, b = state
        if k < 6:
            delta = [0.0] * 6
            delta[k] = s
            return dso.apply_update(pose, delta), a, b
        return (pose, a + s, b) if k == 6 else (pose, a, b + s)

    for k in range(8):
        num = (r_of(host, bump(tgt, k, e), d) - r_of(host, bump(tgt, k, -e), d)) / (2 * e)
        assert abs(num - jt[k]) <= 1e-4 * (1.0 + abs(num))
        num = (r_of(bump(host, k, e), tgt, d) - r_of(bump(host, k, -e), tgt, d)) / (2 * e)
        assert abs(num - jh[k]) <= 1e-4 * (1.0 + abs(num))
    num = (r_of(host, tgt, d + e) - r_of(host, tgt, d - e)) / (2 * e)
    assert abs(num - jd) <= 1e-4 * (1.0 + abs(num))
    assert abs(r - r_of(host, tgt, d)) == 0.0


def test_tracking_recovers_pose_and_brightness():
    plane = Plane(5.0)
    host = (IDENT, 0.1, 3.0)
    truth = (make_pose([0.004, -0.008, 0.003], [0.08, -0.05, 0.1]), -0.15, 7.0)
    hp = analytic_pyramid(plane, host, 2)
    tp = analytic_pyramid(plane, truth, 2)
    pts = [(u, v, plane.inv_depth(IDENT, u, v)) for u, v in grid_points(6)]
    (pose, a, b), rmse = dso.track_frame(pts, hp, tp, K, host, (IDENT, 0.0, 0.0))
    ang, dt = pose_err(pose, truth[0])
    assert ang < 1e-7 and dt < 1e-6
    assert abs(a - truth[1]) < 1e-6 and abs(b - truth[2]) < 1e-4
    assert rmse < 1e-5


def test_search_depth_finds_inverse_depth():
    plane = Plane(4.0)
    host = (IDENT, 0.0, 0.0)
    tgt = (make_pose([0.0, 0.01, 0.0], [0.3, 0.05, 0.0]), 0.05, 2.0)
    himg, timg = AnalyticImage(plane, *host), AnalyticImage(plane, *tgt)
    for p in [(14.0, 12.0), (30.0, 20.0), (22.0, 9.0)]:
        d, rmse = dso.search_depth(himg, timg, K, p, host, tgt, 0.05, 0.6)
        assert abs(d - 0.25) < 1e-6
        assert rmse < 1e-5


def test_schur_complement_equals_joint_minimum():
    rng = random.Random(3)
    n = 7
    A = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    Hm = [[sum(A[k][i] * A[k][j] for k in range(n)) + (1.0 if i == j else 0.0) for j in range(n)] for i in range(n)]
    b = [rng.uniform(-1, 1) for _ in range(n)]
    keep, drop = [0, 2, 5], [1, 3, 4, 6]
    Hn, bn = dso.schur_marginalize(Hm, b, keep, drop)
    full = solve(Hm, b)
    red = solve(Hn, bn)
    for i, k in enumerate(keep):
        assert abs(red[i] - full[k]) < 1e-10

    def energy(x):
        return -sum(p * q for p, q in zip(b, x)) + 0.5 * sum(x[i] * Hm[i][j] * x[j] for i in range(n) for j in range(n))

    def reduced_gap(xk):
        # min over the dropped part, compared with the reduced quadratic
        rhs = [b[d] - sum(Hm[d][k] * xk[i] for i, k in enumerate(keep)) for d in drop]
        xd = solve([[Hm[d][e] for e in drop] for d in drop], rhs)
        x = [0.0] * n
        for i, k in enumerate(keep):
            x[k] = xk[i]
        for i, d in enumerate(drop):
            x[d] = xd[i]
        er = -sum(p * q for p, q in zip(bn, xk)) + 0.5 * sum(xk[i] * Hn[i][j] * xk[j] for i in range(3) for j in range(3))
        return energy(x) - er

    g1 = reduced_gap([0.3, -0.2, 0.7])
    g2 = reduced_gap([-1.1, 0.4, 0.0])
    assert abs(g1 - g2) < 1e-10


def window_scene():
    plane = Plane(5.0)
    truth = {0: (IDENT, 0.0, 0.0),
             1: (make_pose([0.0, 0.0, 0.0], [0.2, 0.05, 0.1]), 0.1, 4.0),
             2: (make_pose([0.006, -0.01, 0.004], [0.4, -0.05, 0.15]), -0.12, -5.0),
             3: (make_pose([0.0, 0.0, 0.0], [0.55, 0.02, 0.2]), 0.05, 2.0)}
    kfs = {f: dso.Keyframe(f, AnalyticImage(plane, *s), s[0], s[1], s[2], fixed=(f == 0)) for f, s in truth.items()}
    pts = [dso.Point(0, u, v, plane.inv_depth(IDENT, u, v), fixed=(k == 0)) for k, (u, v) in enumerate(grid_points(7))]
    c1 = truth[1][0]
    pts += [dso.Point(1, u, v, plane.inv_depth(c1, u, v)) for u, v in grid_points(9, 8)]
    return plane, truth, kfs, pts


def perturb(kfs, pts, rng, fids):
    for f in fids:
        kf = kfs[f]
        kf.pose = dso.apply_update(kf.pose, [rng.uniform(-0.004, 0.004) for _ in range(3)]
                                   + [rng.uniform(-0.02, 0.02) for _ in range(3)])
        kf.a += rng.uniform(-0.03, 0.03)
        kf.b += rng.uniform(-1.0, 1.0)
    for p in pts:
        if not p.fixed:
            p.d *= 1.0 + rng.uniform(-0.03, 0.03)


def check_truth(kfs, pts, truth, plane, tol):
    for f, kf in kfs.items():
        ang, dt = pose_err(kf.pose, truth[f][0])
        assert ang < tol and dt < tol
        assert abs(kf.a - truth[f][1]) < tol and abs(kf.b - truth[f][2]) < 100 * tol
    for p in pts:
        assert abs(p.d - plane.inv_depth(truth[p.host][0], p.u, p.v)) < tol


def test_window_optimization_recovers_truth():
    plane, truth, kfs, pts = window_scene()
    del kfs[3]
    rng = random.Random(5)
    perturb(kfs, pts, rng, [1, 2])
    hist = dso.optimize_window(kfs, pts, K, None, iters=10)
    assert all(x > y for x, y in zip(hist, hist[1:]))
    assert hist[-1] < 1e-12 * hist[0]
    check_truth(kfs, pts, truth, plane, 1e-6)


def test_marginalization_keeps_the_truth():
    plane, truth, kfs, pts = window_scene()
    pts, prior = dso.marginalize_keyframe(kfs, pts, K, None, 1)
    assert sorted(kfs) == [0, 2, 3]
    assert all(p.host == 0 for p in pts)
    assert prior.fids == [2, 3] and len(prior.H) == 16
    assert max(abs(x) for x in prior.b) < 1e-6
    for i in range(16):
        for j in range(16):
            assert abs(prior.H[i][j] - prior.H[j][i]) < 1e-6 * (1.0 + abs(prior.H[i][j]))
    # the prior plus the remaining residuals still have their minimum at the truth
    rng = random.Random(9)
    perturb(kfs, pts, rng, [2, 3])
    hist = dso.optimize_window(kfs, pts, K, prior, iters=10)
    assert all(x > y for x, y in zip(hist, hist[1:]))
    check_truth(kfs, pts, truth, plane, 1e-6)


def test_keyframe_score_by_hand():
    host = (IDENT, 0.1, 0.0)
    pts = [(K[2], K[3], 0.2)]
    tgt = (make_pose([0.0, 0.0, 0.0], [-0.5, 0.0, 0.0]), 0.4, 0.0)  # moves 0.5 to the left
    s = dso.keyframe_score(pts, K, host, tgt, 1.0, 2.0, 10.0)
    assert abs(s - (4.0 + 2.0 * 4.0 + 10.0 * 0.3)) < 1e-12
    rot = (dso.relative(make_pose([0.0, 0.01, 0.0], [0.0, 0.0, 0.0]), IDENT), 0.1, 0.0)
    s = dso.keyframe_score(pts, K, host, rot, 0.0, 1.0, 0.0)
    assert abs(s) < 1e-12
    s = dso.keyframe_score(pts, K, host, rot, 1.0, 0.0, 0.0)
    assert abs(s - 40.0 * math.tan(0.01)) < 1e-9


def test_select_points():
    flat = dso.GridImage([[50.0] * 20 for _ in range(16)])
    assert dso.select_points(flat, 4, 3.0) == []
    edge = dso.GridImage([[0.0 if u < 10 else 100.0 for u in range(20)] for _ in range(16)])
    got = dso.select_points(edge, 4, 3.0)
    assert got and all(u in (9, 10) for u, _ in got)
    assert len(set(got)) == len(got)


def test_choose_marginalized_by_hand():
    plane = Plane(5.0)
    kfs = {}
    xs = [0.0, 0.1, 0.5, 0.6, 0.7]
    for f, x in enumerate(xs):
        pose = make_pose([0.0, 0.0, 0.0], [x, 0.0, 0.0])
        kfs[f] = dso.Keyframe(f, AnalyticImage(plane, pose, 0.0, 0.0), pose)
    pts = [dso.Point(f, 24.0, 18.0, 0.2) for f in kfs]
    eps = 1e-3

    def score(f):
        return math.sqrt(abs(xs[f] - xs[4])) * sum(1.0 / (abs(xs[f] - xs[j]) + eps) for j in range(4) if j != f)

    want = max(range(3), key=score)
    assert dso.choose_marginalized(kfs, pts, K, 4, eps) == want
    assert dso.choose_marginalized(kfs, pts, K, 5, eps) is None
    # a keyframe whose points all leave the newest image goes first
    pts.append(dso.Point(2, 24.0, 18.0, 0.2))
    pts[2] = dso.Point(1, 2.0, 18.0, 0.2)
    pts[1] = dso.Point(1, 2.0, 18.0, 0.2)
    assert dso.choose_marginalized(kfs, pts, K, 5, eps) == 1


def test_run_dso_on_pixel_grids():
    # Bilinear sampling of a pixel grid is not the true image, so the
    # estimates are not exact here. Even a single tracking step from frame 0
    # to frame 1 with the true depths is off by about 0.05 degree, and a
    # rotation about the vertical axis looks much like a sideways move, so
    # the errors add up along the path. The bounds below are loose on purpose.
    plane = Plane(5.0, 0.1)
    n = 7
    truth = [(make_pose([0.0, 0.003 * k, 0.001 * k], [0.12 * k, 0.02 * k, 0.03 * k]), 0.02 * k, 1.5 * k)
             for k in range(n)]
    frames = []
    for pose, a, b in truth:
        img = AnalyticImage(plane, pose, a, b)
        frames.append(dso.GridImage([[img.value(u, v) for u in range(W)] for v in range(H)]))
    out = dso.run_dso(frames, K, lambda u, v: plane.inv_depth(IDENT, u, v), levels=2, n_max=3, block=6,
                      g_th=3.0, t_kf=4.0)
    assert len(out["keyframes"]) == 3
    assert out["prior"] is not None  # at least one keyframe was marginalized
    path = 0.0
    for k in range(1, n):
        path += norm([a - b for a, b in zip(dso.center(truth[k][0]), dso.center(truth[k - 1][0]))])
    for k in range(n):
        ang, _ = pose_err(out["states"][k][0], truth[k][0])
        dc = norm([a - b for a, b in zip(dso.center(out["states"][k][0]), dso.center(truth[k][0]))])
        assert ang < math.radians(1.0)
        assert dc < 0.1 * path
        assert abs(out["states"][k][1] - truth[k][1]) < 0.03
