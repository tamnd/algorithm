# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/error-state-kalman-filter/. The authors are listed in prov/2VDFY7.jsonl.

import math
import random

import pytest

import rbm
import robest
from error_state_kalman_filter import attitude_error, eskf_correct, eskf_predict, quat_of_rotvec

DIRS = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]
DT = 0.01
SIGMA_G = 0.05
SIGMA_W = 0.002
SIGMA_V = 0.05


def max_diff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


def omega_at(t):
    return [0.4 * math.sin(0.7 * t), 0.3 * math.cos(0.4 * t), 0.2]


def diag(values):
    return [[values[i] if i == j else 0.0 for j in range(len(values))] for i in range(len(values))]


def test_predict_jacobian_matches_finite_differences():
    q = rbm.quat_from_axis_angle([0.3, -0.5, 0.8], 1.1)
    b = [0.02, -0.01, 0.03]
    omega_m = [0.9, -0.4, 0.6]
    dt = 0.01

    def propagate_error(dx):
        q_t = rbm.quat_mul(q, quat_of_rotvec(dx[:3]))
        b_t = rbm.add(b, dx[3:])
        q_t1 = rbm.quat_mul(q_t, quat_of_rotvec(rbm.scale(rbm.sub(omega_m, b_t), dt)))
        q1 = rbm.quat_mul(q, quat_of_rotvec(rbm.scale(rbm.sub(omega_m, b), dt)))
        return attitude_error(q_t1, q1) + list(dx[3:])

    num = rbm.num_jacobian(propagate_error, [0.0] * 6, h=1e-6)
    _, _, f = eskf_predict(q, b, rbm.eye(6), omega_m, dt, 0.0, 0.0)
    # With P = I and Q = 0 the predicted covariance is F F^T. Rebuild F itself:
    wdt = rbm.scale(rbm.sub(omega_m, b), dt)
    rt = rbm.transpose(rbm.so3_exp(wdt))
    f_model = [rt[i] + [(-dt if i == j else 0.0) for j in range(3)] for i in range(3)]
    f_model += [[0.0] * 3 + [1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    assert max_diff(rbm.mul(f_model, rbm.transpose(f_model)), f) < 1e-15
    # The rotation block is exact; the bias block -I dt is the first-order
    # form of -J_r(omega dt) dt, off by about |omega| dt^2 / 2.
    assert max_diff([row[:3] for row in num[:3]], [row[:3] for row in f_model[:3]]) < 1e-8
    assert max_diff(num, f_model) < 1e-4


def test_measurement_jacobian_matches_finite_differences():
    q = rbm.quat_from_axis_angle([-0.2, 0.7, 0.4], 2.0)
    for d in DIRS + [[0.6, -0.48, 0.64]]:
        def h_of(dx):
            r = rbm.quat_to_rot(rbm.quat_mul(q, quat_of_rotvec(dx[:3])))
            return rbm.matvec(rbm.transpose(r), d)

        num = rbm.num_jacobian(h_of, [0.0] * 6, h=1e-6)
        y_hat = h_of([0.0] * 6)
        h = [row + [0.0, 0.0, 0.0] for row in rbm.hat3(y_hat)]
        assert max_diff(num, h) < 1e-8


def test_reset_jacobian():
    a = [0.01, -0.02, 0.015]

    def reset(dtheta):
        return attitude_error(quat_of_rotvec(dtheta), quat_of_rotvec(a))

    num = rbm.num_jacobian(reset, a, h=1e-7)
    g = rbm.sub(rbm.eye(3), rbm.hat3(rbm.scale(a, 0.5)))
    assert max_diff(num, g) < 1e-3  # error O(|a|^2)
    assert max_diff(num, rbm.eye(3)) > 5e-3  # the identity is a worse guess


def run(rng, steps, dx0, p0, correct_every=10):
    q_t = rbm.quat_from_axis_angle([0.1, 0.2, 0.9], 0.7)
    b_t = [0.01, -0.02, 0.015]
    q = rbm.quat_mul(q_t, quat_of_rotvec(rbm.scale(dx0[:3], -1.0)))
    b = rbm.sub(b_t, dx0[3:])
    p = [row[:] for row in p0]
    nees = []
    for k in range(steps):
        om = omega_at(k * DT)
        gyro = [om[i] + b_t[i] + rng.gauss(0.0, SIGMA_G) for i in range(3)]
        q, b, p = eskf_predict(q, b, p, gyro, DT, SIGMA_G, SIGMA_W)
        q_t = rbm.quat_mul(q_t, quat_of_rotvec(rbm.scale(om, DT)))
        b_t = [x + rng.gauss(0.0, SIGMA_W * math.sqrt(DT)) for x in b_t]
        if (k + 1) % correct_every == 0:
            r_t = rbm.quat_to_rot(q_t)
            for d in DIRS:
                y = [x + rng.gauss(0.0, SIGMA_V) for x in rbm.matvec(rbm.transpose(r_t), d)]
                q, b, p = eskf_correct(q, b, p, y, d, SIGMA_V)
            err = attitude_error(q_t, q) + rbm.sub(b_t, b)
            nees.append(robest.mahalanobis2(err, [0.0] * 6, p))
    return q_t, q, b_t, b, p, nees


def test_converges_from_thirty_degrees():
    rng = random.Random(1)
    p0 = diag([0.3 ** 2] * 3 + [0.05 ** 2] * 3)
    dx0 = [math.radians(30.0) / math.sqrt(3.0)] * 3 + [0.0, 0.0, 0.0]
    q_t, q, b_t, b, p, _ = run(rng, 400, dx0, p0)
    assert rbm.norm(attitude_error(q_t, q)) < math.radians(1.5)
    # The covariance stays symmetric and positive definite.
    assert max_diff(p, rbm.transpose(p)) < 1e-15
    rbm.cholesky(p)


def test_quaternion_stays_unit():
    rng = random.Random(2)
    p0 = diag([0.1 ** 2] * 3 + [0.02 ** 2] * 3)
    _, q, _, _, _, _ = run(rng, 200, [0.05, -0.05, 0.02, 0.0, 0.0, 0.0], p0)
    assert abs(rbm.norm(q) - 1.0) < 1e-14


def test_nees_is_near_the_state_dimension():
    # Measurement: average NEES over 4 runs of 20 corrections each. A
    # consistent filter gives about 6, the error-state dimension. Seeds 3, 4
    # and 5 gave 7.3, 5.1 and 9.0. The bound is loose because the runs are
    # short and the samples are correlated.
    rng = random.Random(3)
    p0 = diag([0.1 ** 2] * 3 + [0.02 ** 2] * 3)
    total, count = 0.0, 0
    for _ in range(4):
        dx0 = robest.gauss_sample(rng, [0.0] * 6, p0)
        *_, nees = run(rng, 200, dx0, p0)
        total += sum(nees)
        count += len(nees)
    mean = total / count
    assert 3.0 < mean < 12.0


def test_correct_with_zero_innovation_keeps_the_mean():
    q = rbm.quat_from_axis_angle([1.0, 1.0, 0.0], 0.4)
    b = [0.01, 0.02, 0.03]
    p = diag([0.01] * 3 + [0.001] * 3)
    d = DIRS[0]
    y = rbm.matvec(rbm.transpose(rbm.quat_to_rot(q)), d)
    q2, b2, p2 = eskf_correct(q, b, p, y, d, SIGMA_V)
    assert rbm.norm(rbm.sub(q, q2)) < 1e-15 and b2 == b
    # A direction gives no information about rotation about itself.
    assert rbm.dot(y, rbm.matvec([row[:3] for row in p2[:3]], y)) == pytest.approx(
        rbm.dot(y, rbm.matvec([row[:3] for row in p[:3]], y)), rel=1e-12
    )
    assert p2[0][0] < p[0][0] or p2[1][1] < p[1][1]
