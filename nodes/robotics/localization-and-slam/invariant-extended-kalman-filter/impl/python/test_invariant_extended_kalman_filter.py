# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/invariant-extended-kalman-filter/. The authors are listed in prov/5ADY95.jsonl.

import math
import random

import pytest

import rbm
import robest
from invariant_extended_kalman_filter import (
    H,
    inekf_correct,
    inekf_predict,
    pose,
    se2_adjoint,
    se2_exp,
    se2_inv,
    se2_log,
)

DT = 0.1


def max_diff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


def diag(values):
    return [[values[i] if i == j else 0.0 for j in range(len(values))] for i in range(len(values))]


def twist(k):
    """The body twist increment of a car at step k: (omega dt, v dt, 0)."""
    return [0.3 * math.sin(0.05 * k) * DT, 1.0 * DT, 0.0]


def error_of(chi_hat, chi):
    return se2_log(rbm.mul(se2_inv(chi_hat), chi))


def test_exp_log_and_adjoint():
    rng = random.Random(1)
    for _ in range(200):
        xi = [rng.uniform(-3.0, 3.0), rng.uniform(-5.0, 5.0), rng.uniform(-5.0, 5.0)]
        assert max(abs(a - b) for a, b in zip(se2_log(se2_exp(xi)), xi)) < 1e-12
        small = [x * 1e-6 for x in xi]
        assert max(abs(a - b) for a, b in zip(se2_log(se2_exp(small)), small)) < 1e-18
        m = pose(rng.uniform(-3.0, 3.0), rng.uniform(-5.0, 5.0), rng.uniform(-5.0, 5.0))
        lhs = rbm.mul(rbm.mul(m, se2_exp(xi)), se2_inv(m))
        assert max_diff(lhs, se2_exp(rbm.matvec(se2_adjoint(m), xi))) < 1e-12
        assert max_diff(rbm.mul(m, se2_inv(m)), rbm.eye(3)) < 1e-14


def test_propagation_jacobian_and_observation_matrix():
    u = [0.4, 0.9, -0.3]
    num_f = rbm.num_jacobian(lambda xi: se2_log(rbm.mul(rbm.mul(se2_exp([-x for x in u]), se2_exp(xi)), se2_exp(u))), [0.0] * 3)
    assert max_diff(num_f, se2_adjoint(se2_exp([-x for x in u]))) < 1e-8
    chi_hat = pose(1.2, 3.0, -4.0)

    def innovation(xi):
        chi = rbm.mul(chi_hat, se2_exp(xi))
        y = [chi[0][2], chi[1][2]]
        inv = se2_inv(chi_hat)
        return [inv[0][0] * y[0] + inv[0][1] * y[1] + inv[0][2], inv[1][0] * y[0] + inv[1][1] * y[1] + inv[1][2]]

    assert max_diff(rbm.num_jacobian(innovation, [0.0] * 3), H) < 1e-8


def test_log_linear_error_is_exact_for_a_large_error():
    # Barrau and Bonnabel, Theorem 2: for group affine dynamics the error
    # follows the linear recursion exactly, not only to first order.
    chi_hat = pose(0.5, 1.0, 2.0)
    xi = [1.0, 2.0, -1.5]
    chi = rbm.mul(chi_hat, se2_exp(xi))
    for k in range(60):
        u = twist(k)
        chi_hat, _ = inekf_predict(chi_hat, rbm.eye(3), u, rbm.zeros(3, 3))
        chi = rbm.mul(chi, se2_exp(u))
        xi = rbm.matvec(se2_adjoint(se2_exp([-x for x in u])), xi)
    assert max(abs(a - b) for a, b in zip(error_of(chi_hat, chi), xi)) < 1e-9


def run_filter(chi_hat, p, ys, q, n):
    gains = []
    for k, y in enumerate(ys):
        chi_hat, p = inekf_predict(chi_hat, p, twist(k), q)
        chi_hat, p, kk = inekf_correct(chi_hat, p, y, n)
        gains.append(kk)
    return chi_hat, p, gains


def test_gain_and_covariance_do_not_depend_on_the_estimate():
    rng = random.Random(2)
    ys = [[rng.uniform(-10.0, 10.0), rng.uniform(-10.0, 10.0)] for _ in range(40)]
    q = diag([0.01 ** 2, 0.05 ** 2, 0.02 ** 2])
    n = diag([0.5 ** 2, 0.5 ** 2])
    p0 = diag([0.5, 4.0, 4.0])
    _, p1, k1 = run_filter(pose(0.0, 0.0, 0.0), p0, ys, q, n)
    _, p2, k2 = run_filter(pose(2.8, -30.0, 17.0), p0, ys, q, n)
    assert max_diff(p1, p2) < 1e-12
    assert max(max_diff(a, b) for a, b in zip(k1, k2)) < 1e-12


def test_converges_from_a_large_error_with_exact_data():
    chi = pose(0.0, 0.0, 0.0)
    chi_hat = pose(2.5, 10.0, -8.0)
    p = diag([math.pi ** 2, 100.0, 100.0])
    q = diag([0.01 ** 2, 0.01 ** 2, 0.01 ** 2])
    n = diag([0.1 ** 2, 0.1 ** 2])
    for k in range(150):
        u = twist(k)
        chi_hat, p = inekf_predict(chi_hat, p, u, q)
        chi = rbm.mul(chi, se2_exp(u))
        chi_hat, p, _ = inekf_correct(chi_hat, p, [chi[0][2], chi[1][2]], n)
    err = error_of(chi_hat, chi)
    assert abs(err[0]) < 1e-3
    assert math.hypot(err[1], err[2]) < 1e-2


def test_nees_is_near_the_state_dimension():
    # Measurement: average NEES over 10 runs of 60 steps. A consistent
    # filter gives about 3. The bound is loose and labeled as a measurement.
    rng = random.Random(3)
    q = diag([0.02 ** 2, 0.05 ** 2, 0.05 ** 2])
    n = diag([0.3 ** 2, 0.3 ** 2])
    p0 = diag([0.3 ** 2, 1.0, 1.0])
    total, count = 0.0, 0
    for _ in range(10):
        chi = pose(0.0, 0.0, 0.0)
        chi_hat = rbm.mul(chi, se2_exp([-x for x in robest.gauss_sample(rng, [0.0] * 3, p0)]))
        p = [row[:] for row in p0]
        for k in range(60):
            u = twist(k)
            u_m = robest.gauss_sample(rng, u, q)
            chi_hat, p = inekf_predict(chi_hat, p, u_m, q)
            chi = rbm.mul(chi, se2_exp(u))
            y = robest.gauss_sample(rng, [chi[0][2], chi[1][2]], n)
            chi_hat, p, _ = inekf_correct(chi_hat, p, y, n)
            total += robest.mahalanobis2(error_of(chi_hat, chi), [0.0] * 3, p)
            count += 1
    mean = total / count
    assert 1.5 < mean < 5.0


def test_covariance_stays_symmetric_positive_definite():
    rng = random.Random(4)
    p = diag([1.0, 1.0, 1.0])
    chi_hat = pose(0.0, 0.0, 0.0)
    q = diag([1e-4, 1e-3, 1e-3])
    n = diag([0.01, 0.01])
    for k in range(50):
        chi_hat, p = inekf_predict(chi_hat, p, twist(k), q)
        chi_hat, p, _ = inekf_correct(chi_hat, p, [rng.uniform(-1, 1), rng.uniform(-1, 1)], n)
    assert max_diff(p, rbm.transpose(p)) < 1e-14
    rbm.cholesky(p)


def test_singular_innovation_covariance_is_rejected():
    with pytest.raises(ValueError):
        inekf_correct(pose(0.0, 0.0, 0.0), rbm.zeros(3, 3), [1.0, 1.0], rbm.zeros(2, 2))
