# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monoslam/. The authors are listed in prov/HXRXPQ.jsonl.

import math
import random

import monoslam as M
import rbm
import robest


def small_cov(pos=1e-6, vel=0.01):
    cov = [[0.0] * M.CAM for _ in range(M.CAM)]
    for i in range(3):
        cov[i][i] = pos
        cov[i + 3][i + 3] = vel
    return cov


KNOWN = [(0, [1.5, -0.3]), (1, [1.5, 0.3]), (2, [1.8, -0.1]), (3, [1.8, 0.2])]


def test_projection_jacobians():
    rng = random.Random(1)
    for _ in range(20):
        cam = [rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-0.5, 0.5)]
        p = [cam[0] + 2.0 * math.cos(cam[2]) + rng.uniform(-0.3, 0.3), cam[1] + 2.0 * math.sin(cam[2]) + rng.uniform(-0.3, 0.3)]
        dc, dp = M.project_jac(cam, p)
        nc = rbm.num_jacobian(lambda c: [M.project(c, p)], cam)[0]
        npnt = rbm.num_jacobian(lambda q: [M.project(cam, q)], p)[0]
        assert max(abs(a - b) for a, b in zip(dc, nc)) < 1e-4
        assert max(abs(a - b) for a, b in zip(dp, npnt)) < 1e-4
    assert M.project([0, 0, 0], [-1.0, 0.0]) is None
    assert M.project([0, 0, 0], [2.0, 0.4]) == 100.0


def test_prediction_moves_only_the_camera():
    s = M.MonoSLAM([0.0, 0.0, 0.0, 0.3, 0.0, 0.0], small_cov(1e-4, 0.01), KNOWN, known_var=1e-4)
    rng = random.Random(2)
    n = len(s.mu)
    for i in range(n):  # a full, correlated covariance
        for j in range(i + 1):
            v = 1e-5 * rng.uniform(-1, 1) if i != j else s.cov[i][i]
            s.cov[i][j] = s.cov[j][i] = v
    before = [row[:] for row in s.cov]
    s.predict()
    assert abs(s.mu[0] - 0.01) < 1e-15 and s.mu[1] == 0.0
    dt = s.dt
    f = rbm.eye(n)
    f[0][3] = f[1][4] = f[2][5] = dt
    want = rbm.mul(rbm.mul(f, before), rbm.transpose(f))
    for pos, vel, q in ((0, 3, (s.accel_sd * dt) ** 2), (1, 4, (s.accel_sd * dt) ** 2), (2, 5, (s.alpha_sd * dt) ** 2)):
        want[pos][pos] += q * dt * dt
        want[pos][vel] += q * dt
        want[vel][pos] += q * dt
        want[vel][vel] += q
    assert max(abs(want[i][j] - s.cov[i][j]) for i in range(n) for j in range(n)) < 1e-15
    for i in range(M.CAM, n):  # the map block stays
        for j in range(M.CAM, n):
            assert s.cov[i][j] == before[i][j]


def test_depth_samples_page_example():
    ray = M.Ray([0.0, 0.0], 0.0)
    mean, var = ray.stats()
    assert abs(mean - 2.75) < 1e-12
    assert abs(math.sqrt(var) / mean - 0.47) < 0.005
    ray.logw = [0.0 if 1.5 <= d <= 2.5 else -1e300 for d in ray.depths]
    mean, var = ray.stats()  # the 22 samples inside [1.5, 2.5] run from 1.5125 to 2.4575
    assert abs(mean - 2.0) < 0.02
    assert abs(math.sqrt(var) / mean - 0.144) < 0.005 and math.sqrt(var) / mean < 0.3


def test_gate_and_update():
    s = M.MonoSLAM([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], small_cov(1e-4, 1e-6), KNOWN[:1], known_var=1e-4)
    s.predict()
    u_hat, h, sd2 = s.predicted(M.CAM)
    assert abs(u_hat - M.project([0, 0, 0], KNOWN[0][1])) < 1e-12
    far = u_hat + 4.0 * math.sqrt(sd2)  # 16 > 6.635: rejected
    s.dt = 0.0  # no motion and no process noise, so the frame is only the update
    s.frame({0: far})
    assert s.tries[0] == [1, 1]
    near = u_hat + 1.0
    cov00 = s.cov[1][1]
    s.frame({0: near})
    assert s.tries[0] == [2, 1]
    assert s.cov[1][1] < cov00  # the reading reduced the uncertainty
    assert 2 * s.tries[0][1] <= s.tries[0][0]


def test_add_point_covariance():
    s = M.MonoSLAM([0.2, -0.1, 0.1, 0.0, 0.0, 0.0], small_cov(1e-3, 1e-2), KNOWN[:1], known_var=1e-3)
    rng = random.Random(3)
    n = len(s.mu)
    for i in range(n):
        for j in range(i):
            s.cov[i][j] = s.cov[j][i] = 1e-4 * rng.uniform(-1, 1)
    before = [row[:] for row in s.cov]
    u, depth, dvar = 37.0, 2.2, 0.05
    ray = M.Ray(s.mu[:2], s.mu[2] + math.atan2(u, M.F))
    s.add_point(9, ray, u, depth, dvar)

    def g(z):  # z = (x, y, theta, u, d)
        a = z[2] + math.atan2(z[3], M.F)
        return [z[0] + z[4] * math.cos(a), z[1] + z[4] * math.sin(a)]

    z0 = s.mu[:3] + [u, depth]
    assert max(abs(a - b) for a, b in zip(g(z0), s.point(9))) < 1e-12
    jz = rbm.num_jacobian(g, z0)
    # the new rows: J_cam Sigma_cam,all, and J Sigma_z J^T with u and d independent
    for j in range(n):
        for r in range(2):
            want = sum(jz[r][a] * before[a][j] for a in range(3))
            assert abs(s.cov[n + r][j] - want) < 1e-8
            assert s.cov[j][n + r] == s.cov[n + r][j]
    for r in range(2):
        for q in range(2):
            want = sum(jz[r][a] * before[a][b] * jz[q][b] for a in range(3) for b in range(3))
            want += jz[r][3] * jz[q][3] * s.r + jz[r][4] * jz[q][4] * dvar
            assert abs(s.cov[n + r][n + q] - want) < 1e-8


def test_delete_points_that_fail():
    s = M.MonoSLAM([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], small_cov(1e-6, 1e-8), KNOWN, known_var=1e-6)
    s.dt = 0.0
    rng = random.Random(4)
    true = [0.0, 0.0, 0.0]
    pts = dict(KNOWN)
    for _ in range(12):  # point 3 is never found
        det = M.simulate_detections(true, pts, rng)
        del det[3]
        s.frame(det)
    assert s.ids == [0, 1, 2] and len(s.mu) == M.CAM + 6 and len(s.cov) == M.CAM + 6
    assert all(len(row) == M.CAM + 6 for row in s.cov)


def run(seed, measure=True, frames=90):
    rng = random.Random(seed)
    pts = dict(KNOWN)
    for i in range(10, 26):
        pts[i] = [rng.uniform(2.0, 4.0), rng.uniform(-1.5, 3.0)]
    s = M.MonoSLAM([0.0, 0.0, 0.0, 0.0, 0.3, 0.0], small_cov(1e-6, 0.01), KNOWN, target=8)
    true = [0.0, 0.0, 0.0]
    for f in range(frames):  # the camera speeds up from 0.3 m/s to 0.7 m/s and turns
        vy, w = 0.3 + 0.4 * f / frames, 0.15 * math.cos(f / 20.0)
        true = [true[0], true[1] + vy * s.dt, true[2] + w * s.dt]
        det = M.simulate_detections(true, pts, rng) if measure else {}
        s.frame(det)
    cam_err = math.hypot(s.mu[0] - true[0], s.mu[1] - true[1])
    pt_err = [math.hypot(s.point(p)[0] - pts[p][0], s.point(p)[1] - pts[p][1]) for p in s.ids if p >= 10]
    return s, true, cam_err, pt_err


def test_simulation_measurement():
    # a measurement of this toy, not a theorem: the camera moves 1.5 m to the side and
    # turns; the known points leave the view, and the new points keep the track
    for seed in (0, 1, 2):
        s, true, cam_err, pt_err = run(seed)
        _, _, blind_err, _ = run(seed, measure=False)
        assert cam_err < 0.05
        assert abs(robest.wrap_angle(s.mu[2] - true[2])) < 0.01
        assert blind_err > 0.5  # the prediction alone keeps the first speed
        assert len(pt_err) >= 4 and max(pt_err) < 0.3
        assert sorted(pt_err)[len(pt_err) // 2] < 0.1
        assert M.project(true, KNOWN[0][1]) is None or not M.in_view(M.project(true, KNOWN[0][1]))
