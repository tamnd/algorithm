# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ekf-slam/. The authors are listed in prov/P959WA.jsonl.

import math
import random

import pytest

import rbm
import robest
from ekf_slam import (
    augment,
    ekf_slam,
    inverse_jacobians,
    inverse_measure,
    measure,
    measure_jacobians,
    motion,
    motion_jacobians,
    predict,
    update,
)

ALPHAS = (0.01, 0.005, 0.005, 0.01)
Q = [[0.1 ** 2, 0.0], [0.0, 0.03 ** 2]]
LANDMARKS = [[4.0, 0.0], [4.0, 4.0], [0.0, 4.0], [-3.0, 2.0], [-2.0, -3.0], [2.0, -3.0]]


def mat_close(a, b, tol):
    return all(abs(x - y) <= tol for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def copy(mu, sigma):
    return list(mu), [list(row) for row in sigma]


# ---------------------------------------------------------------- Jacobians


@pytest.mark.parametrize("x,u", [([1.0, 2.0, 0.3], (1.0, 0.4)), ([0.0, 0.0, -2.0], (0.5, -1.2)), ([2.0, -1.0, 1.0], (0.8, 0.0))])
def test_motion_jacobians_against_finite_differences(x, u):
    g, v = motion_jacobians(x, u, 0.5)
    assert mat_close(g, rbm.num_jacobian(lambda y: motion(y, u, 0.5), x), 1e-6)
    if u[1] != 0.0:
        assert mat_close(v, rbm.num_jacobian(lambda c: motion(x, c, 0.5), list(u)), 1e-6)


@pytest.mark.parametrize("x,m", [([0.0, 0.0, 0.0], [3.0, 1.0]), ([1.0, -2.0, 2.5], [-1.0, 0.5]), ([0.5, 0.5, -1.0], [0.5, 3.0])])
def test_measurement_jacobians_against_finite_differences(x, m):
    hx, hm = measure_jacobians(x, m)
    assert mat_close(hx, rbm.num_jacobian(lambda y: measure(y, m), x), 1e-6)
    assert mat_close(hm, rbm.num_jacobian(lambda y: measure(x, y), m), 1e-6)


@pytest.mark.parametrize("x,z", [([0.0, 0.0, 0.0], [3.0, 0.4]), ([1.0, -2.0, 2.5], [1.5, -2.0])])
def test_inverse_model_and_its_jacobians(x, z):
    m = inverse_measure(x, z)
    back = measure(x, m)
    assert abs(back[0] - z[0]) < 1e-12 and abs(robest.wrap_angle(back[1] - z[1])) < 1e-12
    gx, gz = inverse_jacobians(x, z)
    assert mat_close(gx, rbm.num_jacobian(lambda y: inverse_measure(y, z), x), 1e-6)
    assert mat_close(gz, rbm.num_jacobian(lambda y: inverse_measure(x, y), z), 1e-6)


# ---------------------------------------------------------------- core steps


def random_belief(rng, n):
    a = [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]
    s = rbm.add(rbm.mul(a, rbm.transpose(a)), rbm.scale(rbm.eye(n), 0.5))
    return [rng.uniform(-3.0, 3.0) for _ in range(n)], s


def test_prediction_leaves_the_map_block_unchanged():
    rng = random.Random(1)
    mu, sigma = random_belief(rng, 9)
    mu[2] = 0.4
    before = copy(mu, sigma)
    g, vj = motion_jacobians(mu, (1.0, 0.3), 1.0)
    rx = rbm.mul(rbm.mul(vj, [[0.02, 0.0], [0.0, 0.01]]), rbm.transpose(vj))
    predict(mu, sigma, 3, motion(mu, (1.0, 0.3), 1.0), g, rx)
    assert mu[3:] == before[0][3:]
    assert all(sigma[r][c] == before[1][r][c] for r in range(3, 9) for c in range(3, 9))
    want_xm = rbm.mul(g, [row[3:] for row in before[1][:3]])
    assert mat_close([row[3:] for row in sigma[:3]], want_xm, 1e-12)
    assert mat_close(sigma, rbm.transpose(sigma), 0.0)


def test_sparse_update_equals_the_dense_kalman_update():
    rng = random.Random(2)
    mu, sigma = random_belief(rng, 11)
    idx = [0, 1, 2, 7, 8]
    h = [[rng.uniform(-1, 1) for _ in range(5)] for _ in range(2)]
    nu = [0.3, -0.2]
    full_h = [[0.0] * 11 for _ in range(2)]
    for a in range(2):
        for c, j in enumerate(idx):
            full_h[a][j] = h[a][c]
    s = rbm.add(rbm.mul(rbm.mul(full_h, sigma), rbm.transpose(full_h)), Q)
    k = rbm.mul(rbm.mul(sigma, rbm.transpose(full_h)), rbm.inv(s))
    want_mu = rbm.add(mu, rbm.matvec(k, nu))
    want_sigma = rbm.mul(rbm.sub(rbm.eye(11), rbm.mul(k, full_h)), sigma)
    update(mu, sigma, idx, nu, h, Q)
    assert all(abs(a - b) < 1e-12 for a, b in zip(mu, want_mu))
    assert mat_close(sigma, want_sigma, 1e-12)


def test_augment_matches_the_joint_gaussian_of_the_inverse_model():
    mu = [1.0, 2.0, 0.5]
    sigma = [[0.04, 0.01, 0.0], [0.01, 0.05, 0.002], [0.0, 0.002, 0.01]]
    z = [2.0, 0.3]
    augment(mu, sigma, [0, 1, 2], inverse_measure(mu, z), *inverse_jacobians(mu, z), Q)
    gx, gz = inverse_jacobians(mu[:3], z)
    full = [row + [0.0, 0.0] for row in [[0.04, 0.01, 0.0], [0.01, 0.05, 0.002], [0.0, 0.002, 0.01]]]
    full += [[0.0] * 3 + [Q[0][0], 0.0], [0.0] * 3 + [0.0, Q[1][1]]]
    j = [gx[0] + gz[0], gx[1] + gz[1]]
    a = [[1.0 if i == c else 0.0 for c in range(5)] for i in range(3)] + j
    want = rbm.mul(rbm.mul(a, full), rbm.transpose(a))
    assert mat_close(sigma, want, 1e-15)


# ---------------------------------------------------------------- linear SLAM


def linear_run(rng, steps, landmarks, p0, rw, rq, stationary=False):
    """Simulate z = m_j - x + noise and x' = x + u + noise; return the data."""
    x = [0.0, 0.0]
    data = []
    for _ in range(steps):
        u = [0.0, 0.0] if stationary else [rng.uniform(-0.5, 1.0), rng.uniform(-0.5, 1.0)]
        x = rbm.add(rbm.add(x, u), robest.gauss_sample(rng, [0.0, 0.0], rw)) if not stationary else x
        zs = [(j, rbm.add(rbm.sub(m, x), robest.gauss_sample(rng, [0.0, 0.0], rq))) for j, m in enumerate(landmarks)]
        data.append((u, zs))
    return data


def linear_filter(data, p0, rw, rq, record=None):
    """EKF SLAM with the generic core on the linear translation model."""
    mu, sigma, ids = [0.0, 0.0], [list(r) for r in p0], []
    for u, zs in data:
        predict(mu, sigma, 2, rbm.add(mu[:2], u), rbm.eye(2), rw)
        for j, z in zs:
            if j not in ids:
                augment(mu, sigma, [0, 1], rbm.add(mu[:2], z), rbm.eye(2), rbm.eye(2), rq)
                ids.append(j)
                continue
            k = 2 + 2 * ids.index(j)
            nu = rbm.sub(z, rbm.sub(mu[k:k + 2], mu[:2]))
            update(mu, sigma, [0, 1, k, k + 1], nu, [[-1.0, 0.0, 1.0, 0.0], [0.0, -1.0, 0.0, 1.0]], rq)
        if record is not None:
            record.append(copy(mu, sigma))
    return mu, sigma, ids


def batch_solution(data, p0, rw, rq, nl):
    """Weighted least squares over all poses and landmarks (the full SLAM posterior)."""
    t = len(data)
    n = 2 * (t + 1) + 2 * nl
    lam = rbm.zeros(n, n)
    eta = [0.0] * n

    def add_factor(cols, a, b, info):
        # factor a y[cols] = b with information info
        at_i = rbm.mul(rbm.transpose(a), info)
        blk = rbm.mul(at_i, a)
        vec = rbm.matvec(at_i, b)
        for r, cr in enumerate(cols):
            eta[cr] += vec[r]
            for c, cc in enumerate(cols):
                lam[cr][cc] += blk[r][c]

    i2 = rbm.eye(2)
    add_factor([0, 1], i2, [0.0, 0.0], rbm.inv(p0))
    wi, qi = rbm.inv(rw), rbm.inv(rq)
    for k, (u, zs) in enumerate(data):
        a, b = 2 * k, 2 * k + 2
        add_factor([a, a + 1, b, b + 1], [[-1.0, 0.0, 1.0, 0.0], [0.0, -1.0, 0.0, 1.0]], u, wi)
        for j, z in zs:
            m = 2 * (t + 1) + 2 * j
            add_factor([b, b + 1, m, m + 1], [[-1.0, 0.0, 1.0, 0.0], [0.0, -1.0, 0.0, 1.0]], z, qi)
    return rbm.solve(lam, eta), rbm.inv(lam)


def test_linear_ekf_slam_equals_batch_least_squares():
    rng = random.Random(3)
    p0, rw, rq = [[0.02, 0.0], [0.0, 0.03]], [[0.01, 0.002], [0.002, 0.02]], [[0.05, 0.0], [0.0, 0.04]]
    landmarks = [[3.0, 1.0], [-1.0, 4.0], [2.0, -2.0]]
    data = linear_run(rng, 6, landmarks, p0, rw, rq)
    mu, sigma, ids = linear_filter(data, p0, rw, rq)
    y, cov = batch_solution(data, p0, rw, rq, len(landmarks))
    t = len(data)
    cols = [2 * t, 2 * t + 1] + [2 * (t + 1) + 2 * j + c for j in ids for c in range(2)]
    assert all(abs(mu[i] - y[c]) < 1e-9 for i, c in enumerate(cols))
    assert all(abs(sigma[i][k] - cov[c][d]) < 1e-9 for i, c in enumerate(cols) for k, d in enumerate(cols))


def test_map_determinants_never_increase_in_the_linear_case():
    rng = random.Random(4)
    p0, rw, rq = [[0.1, 0.0], [0.0, 0.1]], [[0.02, 0.0], [0.0, 0.02]], [[0.05, 0.01], [0.01, 0.05]]
    data = linear_run(rng, 25, [[3.0, 1.0], [-1.0, 4.0], [2.0, -2.0]], p0, rw, rq)
    rec = []
    linear_filter(data, p0, rw, rq, rec)
    for sub in ([2, 3], [4, 5], [2, 3, 4, 5], [2, 3, 4, 5, 6, 7], [3, 6]):
        dets = [rbm.det([[s[r][c] for c in sub] for r in sub]) for _, s in rec]
        assert all(b <= a * (1.0 + 1e-12) for a, b in zip(dets, dets[1:]))


def test_landmark_covariance_stays_above_the_initial_robot_covariance():
    rng = random.Random(5)
    p0, rw, rq = [[0.1, 0.03], [0.03, 0.2]], [[0.02, 0.0], [0.0, 0.01]], [[0.05, 0.0], [0.0, 0.05]]
    data = linear_run(rng, 40, [[3.0, 1.0], [-1.0, 4.0]], p0, rw, rq)
    rec = []
    linear_filter(data, p0, rw, rq, rec)
    for _, s in rec:
        for k in (2, 4):
            d = [[s[k][k] - p0[0][0], s[k][k + 1] - p0[0][1]], [s[k + 1][k] - p0[1][0], s[k + 1][k + 1] - p0[1][1]]]
            assert d[0][0] >= -1e-12 and d[1][1] >= -1e-12 and rbm.det(d) >= -1e-12


def test_landmarks_become_fully_correlated():
    rng = random.Random(6)
    p0, rq = [[0.1, 0.0], [0.0, 0.1]], [[0.05, 0.0], [0.0, 0.05]]
    data = linear_run(rng, 50, [[3.0, 1.0], [-1.0, 4.0]], p0, rbm.zeros(2, 2), rq, stationary=True)
    rec = []
    linear_filter(data, p0, rbm.zeros(2, 2), rq, rec)
    for k, (_, s) in enumerate(rec, start=1):
        var_diff = s[2][2] + s[4][4] - 2.0 * s[2][4]
        assert var_diff <= 2.0 * rq[0][0] / k + 1e-12
    s = rec[-1][1]
    assert s[2][4] / math.sqrt(s[2][2] * s[4][4]) > 0.98


# ---------------------------------------------------------------- planar SLAM


def planar_run(rng, steps, correspondences=True, new_gate=None):
    x = [0.0, 0.0, 0.0]
    mu, sigma, ids = [0.0, 0.0, 0.0], rbm.zeros(3, 3), []
    nees = []
    for t in range(steps):
        u = (1.0, 0.35)
        m = robest.gauss_sample(rng, [0.0, 0.0], [[ALPHAS[0] + ALPHAS[1] * u[1] ** 2, 0.0], [0.0, ALPHAS[2] + ALPHAS[3] * u[1] ** 2]])
        x = motion(x, (u[0] + m[0], u[1] + m[1]), 1.0)
        zs, cs = [], []
        for j, lm in enumerate(LANDMARKS):
            z = measure(x, lm)
            if z[0] < 5.0:
                zs.append([z[0] + rng.gauss(0.0, 0.1), robest.wrap_angle(z[1] + rng.gauss(0.0, 0.03))])
                cs.append(j)
        ekf_slam(mu, sigma, ids, u, 1.0, zs, ALPHAS, Q, cs if correspondences else None, new_gate=new_gate)
        if t == 0:
            continue  # the pose covariance has rank 2 after the first control
        e = [x[0] - mu[0], x[1] - mu[1], robest.wrap_angle(x[2] - mu[2])]
        nees.append(robest.mahalanobis2(e, [0.0, 0.0, 0.0], [row[:3] for row in sigma[:3]]))
    return mu, sigma, ids, nees


def test_planar_run_with_known_correspondences_is_close_and_consistent():
    rng = random.Random(7)
    all_nees, map_nees = [], []
    for _ in range(10):
        mu, sigma, ids, nees = planar_run(rng, 25)
        all_nees.extend(nees)
        assert sorted(ids) == list(range(len(LANDMARKS)))
        for slot, j in enumerate(ids):
            k = 3 + 2 * slot
            map_nees.append(robest.mahalanobis2(mu[k:k + 2], LANDMARKS[j], [row[k:k + 2] for row in sigma[k:k + 2]]))
    assert 1.5 < sum(all_nees) / len(all_nees) < 6.0  # measured 2.59; 3 for a consistent filter
    assert 1.0 < sum(map_nees) / len(map_nees) < 4.0  # measured 2.13; 2 for a consistent filter


def test_unknown_correspondences_find_each_landmark_once():
    rng = random.Random(8)
    mu, sigma, ids, _ = planar_run(rng, 25, correspondences=False, new_gate=100.0)
    found = []
    for slot in range(len(ids)):
        k = 3 + 2 * slot
        d = [math.hypot(mu[k] - lm[0], mu[k + 1] - lm[1]) for lm in LANDMARKS]
        j = min(range(len(LANDMARKS)), key=lambda i: d[i])
        assert d[j] < 1.5 and sorted(d)[1] > 2.0  # the map as a whole may drift; the match is clear
        found.append(j)
    assert sorted(found) == list(range(len(LANDMARKS)))
    # the shape of the map is right: pairwise distances agree within 0.2 m
    est = [mu[3 + 2 * s:5 + 2 * s] for s in range(len(ids))]
    for a in range(len(est)):
        for b in range(a):
            assert abs(math.dist(est[a], est[b]) - math.dist(LANDMARKS[found[a]], LANDMARKS[found[b]])) < 0.2
