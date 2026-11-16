# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quest-algorithm/. The authors are listed in prov/Z02XZG.jsonl.

import math
import random

import pytest

import rbm
from quest_algorithm import (
    adjugate_column,
    attitude_matrix,
    attitude_profile,
    char_poly,
    newton_lambda,
    quest,
    wahba_loss,
)


def random_unit(rng):
    while True:
        v = [rng.gauss(0.0, 1.0) for _ in range(3)]
        n = rbm.norm(v)
        if n > 1e-3:
            return [x / n for x in v]


def random_quat(rng):
    q = [rng.gauss(0.0, 1.0) for _ in range(4)]
    n = rbm.norm(q)
    q = [x / n for x in q]
    return q if q[0] >= 0.0 else [-x for x in q]


def same_rotation(q, p):
    return min(rbm.norm(rbm.sub(q, p)), rbm.norm(rbm.add(q, p)))


def make_data(rng, q_true, n, noise):
    a_true = attitude_matrix(q_true)
    rs = [random_unit(rng) for _ in range(n)]
    bs = [rbm.matvec(rbm.mul(rbm.so3_exp([rng.gauss(0.0, noise) for _ in range(3)]), a_true), r) for r in rs]
    weights = [rng.uniform(0.2, 1.0) for _ in range(n)]
    return bs, rs, weights


def davenport_k(bmat):
    sigma = bmat[0][0] + bmat[1][1] + bmat[2][2]
    z = [bmat[1][2] - bmat[2][1], bmat[2][0] - bmat[0][2], bmat[0][1] - bmat[1][0]]
    k = [[sigma] + z]
    for i in range(3):
        k.append([z[i]] + [bmat[i][j] + bmat[j][i] - (sigma if i == j else 0.0) for j in range(3)])
    return k


def power_top(k, lam0, steps=1000):
    """Top eigenvector of K by power iteration on K + lam0 I (all eigenvalues >= 0)."""
    m = [[k[i][j] + (lam0 if i == j else 0.0) for j in range(4)] for i in range(4)]
    v = [1.0, 0.3, -0.2, 0.1]
    for _ in range(steps):
        v = rbm.matvec(m, v)
        n = rbm.norm(v)
        v = [x / n for x in v]
    return v


def test_check_rotation():
    r_sb = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    rs = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    bs = [rbm.matvec(rbm.transpose(r_sb), r) for r in rs]
    q, loss, info = quest(bs, rs, [1.0, 1.0, 1.0])
    assert max(abs(x - 0.5) for x in q) < 1e-12
    assert loss < 1e-12
    assert info["frame"] is None


def test_characteristic_polynomial_matches_determinant():
    rng = random.Random(1)
    for _ in range(30):
        bs, rs, w = make_data(rng, random_quat(rng), 4, 0.5)
        bmat, _ = attitude_profile(bs, rs, w)
        k = davenport_k(bmat)
        p2, p1, p0 = char_poly(bmat)
        for lam in (-1.3, 0.0, 0.7, 2.1):
            psi = lam ** 4 + p2 * lam * lam + p1 * lam + p0
            want = rbm.det([[(lam if i == j else 0.0) - k[i][j] for j in range(4)] for i in range(4)])
            assert abs(psi - want) < 1e-11


def test_against_power_iteration():
    rng = random.Random(2)
    for _ in range(20):
        bs, rs, w = make_data(rng, random_quat(rng), 3, 0.2)
        bmat, lam0 = attitude_profile(bs, rs, w)
        k = davenport_k(bmat)
        v = power_top(k, lam0)
        q, loss, _ = quest(bs, rs, w)
        assert same_rotation(q, v) < 1e-8
        res = rbm.sub(rbm.matvec(k, q), rbm.scale(q, lam0 - loss))
        assert rbm.norm(res) < 1e-10
        assert abs(loss - wahba_loss(attitude_matrix(q), bs, rs, w)) < 1e-12


def test_rayleigh_quotient_never_exceeds_lambda_max():
    rng = random.Random(3)
    bs, rs, w = make_data(rng, random_quat(rng), 4, 0.3)
    bmat, lam0 = attitude_profile(bs, rs, w)
    k = davenport_k(bmat)
    _, loss, _ = quest(bs, rs, w)
    lam = lam0 - loss
    for _ in range(500):
        v = random_quat(rng)
        assert rbm.dot(v, rbm.matvec(k, v)) <= lam + 1e-12


def test_noise_free_recovery_and_one_newton_step():
    rng = random.Random(4)
    for _ in range(100):
        q_true = random_quat(rng)
        bs, rs, w = make_data(rng, q_true, 3, 0.0)
        q, loss, info = quest(bs, rs, w)
        assert same_rotation(q, q_true) < 1e-9
        assert loss < 1e-12
        # lambda0 is already the root, so the first step is tiny.
        assert info["iterations"] <= 2


def test_newton_iterations_with_noise():
    # Measurement: from lambda0, Newton needs few steps at sensor-level noise.
    rng = random.Random(5)
    worst = 0
    for _ in range(100):
        bs, rs, w = make_data(rng, random_quat(rng), 3, 0.01)
        _, _, info = quest(bs, rs, w)
        worst = max(worst, info["iterations"])
    assert worst <= 4


def test_newton_stops_at_the_rounding_floor():
    # With large noise the gap below lambda_max is small, psi' is small, and
    # the last Newton steps swing by one unit of roundoff. The stopping rule
    # must end there instead of running to the step limit.
    rng = random.Random(11)
    worst = 0
    for noise in (0.05, 0.2, 0.5):
        for _ in range(150):
            n = rng.randint(2, 6)
            bs, rs, w = make_data(rng, random_quat(rng), n, noise)
            q, loss, info = quest(bs, rs, w)
            worst = max(worst, info["iterations"])
            assert abs(rbm.norm(q) - 1.0) < 1e-12
            assert wahba_loss(attitude_matrix(q), bs, rs, w) == pytest.approx(loss, abs=1e-10)
    assert worst <= 10


def test_newton_monotone_from_above():
    # All roots of psi are real, so Newton from lambda0 >= lambda_max decreases
    # monotonically to lambda_max.
    rng = random.Random(6)
    bs, rs, w = make_data(rng, random_quat(rng), 3, 0.8)
    bmat, lam0 = attitude_profile(bs, rs, w)
    p2, p1, p0 = char_poly(bmat)
    lam, prev = lam0, lam0 + 1.0
    for _ in range(30):
        psi = lam ** 4 + p2 * lam * lam + p1 * lam + p0
        dpsi = 4.0 * lam ** 3 + 2.0 * p2 * lam + p1
        if psi == 0.0:
            break
        assert lam <= prev + 1e-14 * lam0
        prev, lam = lam, lam - psi / dpsi
    lam_n, _ = newton_lambda(bmat, lam0)
    assert abs(lam - lam_n) < 1e-12


def test_rotation_by_pi_uses_another_frame():
    rng = random.Random(7)
    for _ in range(30):
        q_true = [0.0] + random_unit(rng)
        bs, rs, w = make_data(rng, q_true, 3, 0.0)
        bmat, lam0 = attitude_profile(bs, rs, w)
        col, dpsi = adjugate_column(bmat, lam0)
        assert rbm.norm(col) < 1e-9 * abs(dpsi)
        q, _, info = quest(bs, rs, w)
        assert info["frame"] is not None
        assert same_rotation(q, q_true) < 1e-9


def test_near_pi_with_noise():
    rng = random.Random(8)
    for _ in range(30):
        axis = random_unit(rng)
        q_true = rbm.quat_from_axis_angle(axis, math.pi - 1e-7)
        bs, rs, w = make_data(rng, q_true, 4, 0.001)
        q, loss, _ = quest(bs, rs, w)
        bmat, lam0 = attitude_profile(bs, rs, w)
        v = power_top(davenport_k(bmat), lam0)
        assert same_rotation(q, v) < 1e-8
        assert abs(rbm.norm(q) - 1.0) < 1e-14


def test_adjugate_column_norm_is_dpsi_times_q0():
    rng = random.Random(9)
    for _ in range(30):
        q_true = random_quat(rng)
        bs, rs, w = make_data(rng, q_true, 3, 0.05)
        bmat, lam0 = attitude_profile(bs, rs, w)
        lam, _ = newton_lambda(bmat, lam0)
        col, dpsi = adjugate_column(bmat, lam)
        q, _, _ = quest(bs, rs, w)
        assert abs(rbm.norm(col) - abs(dpsi) * abs(q[0])) < 1e-9


def test_bad_input():
    with pytest.raises(ValueError):
        quest([[1.0, 0.0, 0.0]], [[1.0, 0.0, 0.0]], [-1.0])
    with pytest.raises(ValueError):
        quest([], [], [])
