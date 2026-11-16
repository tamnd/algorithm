# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nister-visual-odometry/. The authors are listed in prov/RM5DZP.jsonl.
import math
import random

from cvla import cross, matvec, mul, norm, skew, svd, transpose
from nister_visual_odometry import (
    apply_update, canonical, decompose_essential, five_point, mono_vo, p3p, pose_jacobian, pose_residual,
    preemptive_select, project, refine_pose, resection, rotation_angle, so3_exp, stereo_vo, transform)

F = 500.0  # focal length in pixels; the image is 640 x 480


def inside(p):
    return p is not None and abs(p[0]) <= 320.0 / F and abs(p[1]) <= 240.0 / F


def make_poses(n):
    poses = []
    for k in range(n):
        R = so3_exp([0.01 * k, 0.03 * k, 0.005 * k])
        C = [0.15 * k, 0.02 * k, 0.35 * k]
        poses.append((R, [-v for v in matvec(R, C)]))
    return poses


def make_scene(rng, n_frames, n_points, baseline=None):
    poses = make_poses(n_frames)
    cams = list(poses)
    if baseline is not None:
        cams += [(R, [t[0] - baseline, t[1], t[2]]) for R, t in poses]
    pts = []
    while len(pts) < n_points:
        X = [rng.uniform(-5.0, 5.0), rng.uniform(-3.5, 3.5), rng.uniform(8.0, 16.0)]
        if all(inside(project(c, X)) for c in cams):
            pts.append(X)
    return poses, pts


def observe(rng, pose, pts, outlier_rate=0.0, sigma_px=0.0):
    out = {}
    for i, X in enumerate(pts):
        if rng.random() < outlier_rate:
            out[i] = (rng.uniform(-0.64, 0.64), rng.uniform(-0.48, 0.48))
            continue
        x, y = project(pose, X)
        out[i] = (x + rng.gauss(0.0, sigma_px / F), y + rng.gauss(0.0, sigma_px / F))
    return out


def test_p3p_returns_true_pose():
    rng = random.Random(1)
    for _ in range(20):
        pose = (so3_exp([rng.uniform(-0.5, 0.5) for _ in range(3)]), [rng.uniform(-1, 1) for _ in range(3)])
        R, t = pose
        pts = []
        while len(pts) < 3:
            X = [rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(4, 8)]
            if transform(pose, X)[2] > 0.5:
                pts.append(X)
        bearings = [transform(pose, X) for X in pts]
        sols = p3p(bearings, pts)
        assert 1 <= len(sols) <= 4
        for s in sols:
            assert abs(mul(transpose(s[0]), s[0])[0][0] - 1.0) < 1e-9
            for X, b in zip(pts, bearings):
                xc = transform(s, X)
                assert xc[2] > 0
                assert norm(cross(xc, b)) <= 1e-7 * norm(xc) * norm(b)
        assert any(rotation_angle(s[0], R) < 1e-8 and norm([a - b for a, b in zip(s[1], t)]) < 1e-8 for s in sols)


def test_five_point_solutions_and_truth():
    rng = random.Random(2)
    for _ in range(5):
        R = so3_exp([rng.uniform(-0.3, 0.3) for _ in range(3)])
        t = [rng.uniform(-1, 1) for _ in range(3)]
        pts = [[rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(4, 8)] for _ in range(5)]
        x1 = [(X[0] / X[2], X[1] / X[2]) for X in pts]
        x2 = [project((R, t), X) for X in pts]
        sols = five_point(x1, x2)
        assert sols
        for E in sols:
            s = svd(E)[1]
            assert abs(s[0] - s[1]) <= 1e-8 and s[2] <= 1e-8
            for p, q in zip(x1, x2):
                assert abs(sum(q2 * sum(E[i][j] * p2 for j, p2 in enumerate((p[0], p[1], 1.0)))
                               for i, q2 in enumerate((q[0], q[1], 1.0)))) <= 1e-9
        truth = canonical(mul(skew(t), R))
        assert min(norm([[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(E, truth)]) for E in sols) <= 1e-8
        R2, t2 = decompose_essential(truth, x1, x2)
        assert rotation_angle(R2, R) <= 1e-8
        assert norm([a - b / norm(t) for a, b in zip(t2, t)]) <= 1e-8


def test_preemptive_select_keeps_best():
    rng = random.Random(3)
    data = [2.0 + rng.gauss(0.0, 0.01) for _ in range(40)] + [rng.uniform(-50, 50) for _ in range(10)]
    hyps = [0.0, 1.0, 2.0, 3.0, -5.0, 10.0, 2.5, 1.5]
    best = preemptive_select(hyps, len(data), lambda h, i: (h - data[i]) ** 2, 0.2, 5, rng)
    assert best == 2.0


def test_pose_jacobian_and_refinement():
    rng = random.Random(4)
    true = (so3_exp([0.1, -0.2, 0.05]), [0.3, -0.1, 0.5])
    pts = [[rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(4, 8)] for _ in range(20)]
    obs = [project(true, X) for X in pts]
    start = apply_update(true, [0.02, -0.01, 0.015, 0.05, -0.04, 0.03])
    h = 1e-6
    for X, x in zip(pts[:5], obs[:5]):
        j = pose_jacobian(start, X)
        for c in range(6):
            d = [0.0] * 6
            d[c] = h
            rp = pose_residual(apply_update(start, d), X, x)
            d[c] = -h
            rm = pose_residual(apply_update(start, d), X, x)
            for r in range(2):
                assert abs((rp[r] - rm[r]) / (2 * h) - j[r][c]) <= 1e-6 * max(1.0, abs(j[r][c]))
    pose, hist = refine_pose(start, pts, obs)
    assert all(b < a for a, b in zip(hist, hist[1:]))
    assert rotation_angle(pose[0], true[0]) <= 1e-6
    assert norm([a - b for a, b in zip(pose[1], true[1])]) <= 1e-6


def test_resection_with_outliers():
    rng = random.Random(5)
    true = (so3_exp([0.05, 0.1, -0.02]), [0.2, 0.1, -0.3])
    pts = [[rng.uniform(-3, 3), rng.uniform(-2, 2), rng.uniform(6, 12)] for _ in range(40)]
    bad = set(rng.sample(range(40), 10))
    obs = [(rng.uniform(-0.6, 0.6), rng.uniform(-0.4, 0.4)) if i in bad else project(true, X) for i, X in enumerate(pts)]
    pose = resection(pts, obs, 0.004, 15, 8, rng)
    assert rotation_angle(pose[0], true[0]) <= 1e-6
    assert norm([a - b for a, b in zip(pose[1], true[1])]) <= 1e-6
    found = {i for i in range(40) if norm([a - b for a, b in zip(project(pose, pts[i]), obs[i])]) <= 0.004}
    assert found == set(range(40)) - bad


def test_monocular_sequence_up_to_scale():
    rng = random.Random(6)
    poses, pts = make_scene(rng, 8, 60)
    tracks = [observe(rng, p, pts, outlier_rate=0.1) for p in poses]
    est = mono_vo(tracks, firewall_every=4, seed=7)
    s = norm(est[2][1]) / norm(poses[2][1])
    for (R, t), (Re, te) in zip(poses, est):
        assert rotation_angle(R, Re) <= 1e-6
        assert norm([a - s * b for a, b in zip(te, t)]) <= 1e-6 * max(1.0, s * norm(t))


def test_stereo_sequence_exact_and_noisy():
    rng = random.Random(8)
    b = 0.5
    poses, pts = make_scene(rng, 6, 50, baseline=b)
    right = [(R, [t[0] - b, t[1], t[2]]) for R, t in poses]
    left_obs = [observe(rng, p, pts, outlier_rate=0.1) for p in poses]
    right_obs = [observe(rng, p, pts, outlier_rate=0.1) for p in right]
    # Without noise a tight threshold (0.5 pixel) keeps out wrong points that
    # an outlier near the epipolar line can create.
    est = stereo_vo(left_obs, right_obs, b, tau=0.001, seed=9)
    for (R, t), (Re, te) in zip(poses, est):
        assert rotation_angle(R, Re) <= 1e-6
        assert norm([x - y for x, y in zip(te, t)]) <= 1e-6
    # sigma = 0.5 pixel: rotation error below 1 degree and position error below
    # 5 percent of the path length after 5 steps.
    left_obs = [observe(rng, p, pts, sigma_px=0.5) for p in poses]
    right_obs = [observe(rng, p, pts, sigma_px=0.5) for p in right]
    est = stereo_vo(left_obs, right_obs, b, seed=10)
    path = norm([0.15 * 5, 0.02 * 5, 0.35 * 5])
    for (R, t), (Re, te) in zip(poses, est):
        assert rotation_angle(R, Re) <= math.radians(1.0)
        c_true = matvec(transpose(R), [-v for v in t])
        c_est = matvec(transpose(Re), [-v for v in te])
        assert norm([x - y for x, y in zip(c_true, c_est)]) <= 0.05 * path
