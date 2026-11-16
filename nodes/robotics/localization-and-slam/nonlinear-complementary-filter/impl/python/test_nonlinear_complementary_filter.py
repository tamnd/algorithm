# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonlinear-complementary-filter/. The authors are listed in prov/R8HFJF.jsonl.

import math
import random

import pytest

import rbm
from nonlinear_complementary_filter import ecf_step, measurement_error

V0S = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]  # gravity up and magnetic north
KS = [1.0, 0.5]  # M0 = diag(0.5, 0, 1) has three distinct eigenvalues
BIAS = [0.02, -0.03, 0.01]


def omega_at(t):
    return [0.3 * math.sin(0.5 * t), 0.2 * math.cos(0.3 * t), 0.1]


def angle(r_hat, r):
    return rbm.norm(rbm.so3_log(rbm.mul(r_hat, rbm.transpose(r))))


def lyapunov(r_hat, b_hat, r, k_i):
    """V = E_mes + |b - b_hat|^2 / (2 k_I); its time derivative is -k_P |w_mes|^2."""
    vs = [rbm.matvec(rbm.transpose(r), v0) for v0 in V0S]
    bt = rbm.sub(BIAS, b_hat)
    return measurement_error(r_hat, vs, V0S, KS) + rbm.dot(bt, bt) / (2.0 * k_i)


def simulate(r_hat, b_hat, steps, k_p=2.0, k_i=0.5, dt=0.02, rng=None, noise=0.0, v0s=V0S, ks=KS, bias=BIAS):
    r = rbm.eye(3)
    history = []
    for k in range(steps):
        om = omega_at(k * dt)
        rt = rbm.transpose(r)
        vs = [rbm.matvec(rt, v0) for v0 in v0s]
        gyro = [o + b for o, b in zip(om, bias)]
        if rng is not None:
            vs = [[x + rng.gauss(0.0, noise) for x in v] for v in vs]
            gyro = [x + rng.gauss(0.0, noise) for x in gyro]
        r_hat, b_hat, _ = ecf_step(r_hat, b_hat, gyro, vs, v0s, ks, k_p, k_i, dt)
        r = rbm.mul(r, rbm.so3_exp([o * dt for o in om]))
        history.append((r_hat, b_hat, r))
    return history


def test_converges_from_large_error_and_learns_bias():
    hist = simulate(rbm.so3_exp([1.5, -1.0, 0.5]), [0.0, 0.0, 0.0], 800)
    r_hat, b_hat, r = hist[-1]
    assert angle(r_hat, r) < 2e-2
    assert rbm.norm(rbm.sub(b_hat, BIAS)) < 2e-2
    # The error keeps shrinking: compare with the error halfway.
    assert angle(r_hat, r) < 0.2 * angle(hist[400][0], hist[400][2])


def test_lyapunov_function_never_increases():
    k_i = 0.5
    hist = simulate(rbm.so3_exp([1.5, -1.0, 0.5]), [0.0, 0.0, 0.0], 600, k_i=k_i)
    vals = [lyapunov(rh, bh, r, k_i) for rh, bh, r in hist]
    for a, b in zip(vals, vals[1:]):
        assert b <= a + 1e-9
    assert vals[-1] < 1e-2 * vals[0]


def test_estimate_stays_on_so3():
    hist = simulate(rbm.so3_exp([0.4, 0.2, -0.3]), [0.0, 0.0, 0.0], 600, rng=random.Random(1), noise=0.01)
    r_hat = hist[-1][0]
    rtr = rbm.mul(rbm.transpose(r_hat), r_hat)
    assert max(abs(rtr[i][j] - (1.0 if i == j else 0.0)) for i in range(3) for j in range(3)) < 1e-12
    assert abs(rbm.det(r_hat) - 1.0) < 1e-12


def test_unstable_equilibria_are_fixed_points():
    # R_hat = D_i R with b_hat = b gives w_mes = 0 exactly.
    for d in ([1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0]):
        dm = [[d[i] if i == j else 0.0 for j in range(3)] for i in range(3)]
        r = rbm.so3_exp([0.3, -0.2, 0.7])
        vs = [rbm.matvec(rbm.transpose(r), v0) for v0 in V0S]
        _, _, w = ecf_step(rbm.mul(dm, r), BIAS, [0.0, 0.0, 0.0], vs, V0S, KS, 1.0, 0.3, 0.01)
        assert rbm.norm(w) < 1e-15


def test_unstable_equilibrium_is_left_after_a_small_push():
    d1 = [[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]]
    start = rbm.mul(rbm.so3_exp([0.0, 1e-3, 1e-3]), d1)
    hist = simulate(start, list(BIAS), 1000)
    r_hat, _, r = hist[-1]
    assert angle(r_hat, r) < 5e-2


def test_single_direction_aligns_that_direction():
    # Corollary 5.2 setting: one vector, no bias. v_hat tends to v, the
    # rotation about v0 is not observable.
    v0s, ks = [[0.0, 0.0, 1.0]], [1.0]
    hist = simulate(rbm.so3_exp([1.0, 0.5, 0.0]), [0.0, 0.0, 0.0], 800, k_i=0.0, v0s=v0s, ks=ks, bias=[0.0, 0.0, 0.0])
    r_hat, _, r = hist[-1]
    v = rbm.matvec(rbm.transpose(r), v0s[0])
    v_hat = rbm.matvec(rbm.transpose(r_hat), v0s[0])
    assert rbm.norm(rbm.sub(v, v_hat)) < 1e-4


def test_noisy_run_stays_close():
    # Measurement: with noise of 0.01 on every channel, the error after
    # convergence stays below 2 degrees in this run.
    hist = simulate(rbm.so3_exp([0.5, 0.5, 0.5]), [0.0, 0.0, 0.0], 800, rng=random.Random(2), noise=0.01)
    worst = max(angle(rh, r) for rh, _, r in hist[500:])
    assert worst < math.radians(2.0)


def test_zero_measurement_vector_is_rejected():
    with pytest.raises(ValueError):
        ecf_step(rbm.eye(3), [0.0] * 3, [0.0] * 3, [[0.0, 0.0, 0.0]], [[0.0, 0.0, 1.0]], [1.0], 1.0, 0.1, 0.01)
