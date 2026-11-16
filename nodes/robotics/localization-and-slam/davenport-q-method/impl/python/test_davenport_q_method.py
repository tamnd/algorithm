# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/davenport-q-method/. The authors are listed in prov/98191D.jsonl.

import math
import random

import pytest

import rbm
from davenport_q_method import (
    attitude_matrix,
    attitude_profile,
    davenport_matrix,
    jacobi_eigen,
    q_method,
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


def max_diff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


def same_rotation(q, p):
    """Return the distance between q and p up to sign."""
    return min(rbm.norm(rbm.sub(q, p)), rbm.norm(rbm.add(q, p)))


def make_data(rng, q_true, n, noise):
    a_true = attitude_matrix(q_true)
    rs = [random_unit(rng) for _ in range(n)]
    bs = []
    for r in rs:
        b = rbm.matvec(rbm.mul(rbm.so3_exp([rng.gauss(0.0, noise) for _ in range(3)]), a_true), r)
        bs.append(b)
    weights = [rng.uniform(0.2, 1.0) for _ in range(n)]
    return bs, rs, weights


def test_check_rotation():
    # R_sb is 120 degrees about (1, 1, 1) / sqrt(3): q = (1/2, 1/2, 1/2, 1/2).
    r_sb = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    rs = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    bs = [rbm.matvec(rbm.transpose(r_sb), r) for r in rs]
    q, loss = q_method(bs, rs, [1.0, 1.0, 1.0])
    assert max(abs(x - 0.5) for x in q) < 1e-12
    assert loss < 1e-12


def test_quarter_turn_about_z():
    r_sb = rbm.rot_z(math.pi / 2.0)
    rs = [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    bs = [rbm.matvec(rbm.transpose(r_sb), r) for r in rs]
    q, _ = q_method(bs, rs, [1.0, 1.0])
    h = math.sqrt(0.5)
    assert rbm.norm(rbm.sub(q, [h, 0.0, 0.0, h])) < 1e-12


def test_quaternion_quadratic_form_is_trace():
    # q^T K q = tr(A B^T) for every unit q, with A = attitude_matrix(q).
    rng = random.Random(1)
    for _ in range(50):
        bs, rs, w = make_data(rng, random_quat(rng), 4, 0.3)
        bmat, _ = attitude_profile(bs, rs, w)
        k = davenport_matrix(bmat)
        q = random_quat(rng)
        qkq = rbm.dot(q, rbm.matvec(k, q))
        a = attitude_matrix(q)
        tr = sum(a[i][j] * bmat[i][j] for i in range(3) for j in range(3))
        assert abs(qkq - tr) < 1e-12
        assert abs(k[0][0] + k[1][1] + k[2][2] + k[3][3]) < 1e-12


def test_noise_free_recovery():
    rng = random.Random(2)
    for _ in range(100):
        q_true = random_quat(rng)
        bs, rs, w = make_data(rng, q_true, rng.randint(2, 6), 0.0)
        q, loss = q_method(bs, rs, w)
        assert same_rotation(q, q_true) < 1e-10
        assert loss < 1e-12


def test_rotation_by_pi():
    rng = random.Random(3)
    for _ in range(20):
        axis = random_unit(rng)
        q_true = [0.0] + axis
        bs, rs, w = make_data(rng, q_true, 3, 0.0)
        q, _ = q_method(bs, rs, w)
        assert same_rotation(q, q_true) < 1e-10


def test_eigen_residual_and_loss_formula():
    rng = random.Random(4)
    for _ in range(50):
        bs, rs, w = make_data(rng, random_quat(rng), 5, 0.1)
        bmat, lam0 = attitude_profile(bs, rs, w)
        k = davenport_matrix(bmat)
        vals, vecs = jacobi_eigen(k)
        for j in range(4):
            v = [vecs[i][j] for i in range(4)]
            res = rbm.sub(rbm.matvec(k, v), rbm.scale(v, vals[j]))
            assert rbm.norm(res) < 1e-12
        vt_v = rbm.mul(rbm.transpose(vecs), vecs)
        assert max_diff(vt_v, rbm.eye(4)) < 1e-13
        q, loss = q_method(bs, rs, w)
        assert abs(rbm.norm(q) - 1.0) < 1e-14 and q[0] >= 0.0
        assert abs(loss - wahba_loss(attitude_matrix(q), bs, rs, w)) < 1e-12
        assert abs(loss - (lam0 - max(vals))) < 1e-12


def descend(a, bmat, steps=300):
    for _ in range(steps):
        m = rbm.mul(rbm.transpose(a), bmat)
        g = [m[2][1] - m[1][2], m[0][2] - m[2][0], m[1][0] - m[0][1]]
        a = rbm.mul(a, rbm.so3_exp(rbm.scale(g, 0.2)))
    return a


def test_optimal_against_multistart_descent():
    rng = random.Random(5)
    for _ in range(10):
        bs, rs, w = make_data(rng, random_quat(rng), 3, 0.4)
        q, loss = q_method(bs, rs, w)
        bmat, _ = attitude_profile(bs, rs, w)
        for _ in range(4):
            a0 = attitude_matrix(random_quat(rng))
            assert wahba_loss(descend(a0, bmat), bs, rs, w) >= loss - 1e-12
        # A random rotation never beats the q-method.
        for _ in range(20):
            assert wahba_loss(attitude_matrix(random_quat(rng)), bs, rs, w) >= loss - 1e-12


def test_bad_input():
    with pytest.raises(ValueError):
        q_method([[1.0, 0.0, 0.0]], [[1.0, 0.0, 0.0]], [0.0])
    with pytest.raises(ValueError):
        q_method([[1.0, 0.0, 0.0]], [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [1.0])
    with pytest.raises(ValueError):
        q_method([[0.0, 0.0, 0.0]], [[1.0, 0.0, 0.0]], [1.0])


def test_single_vector_gives_degenerate_maximum():
    # One pair fixes the attitude only up to a rotation about b: lambda_max is double.
    vals, _ = jacobi_eigen(davenport_matrix(attitude_profile([[0.0, 0.0, 1.0]], [[1.0, 0.0, 0.0]], [1.0])[0]))
    vals.sort()
    assert abs(vals[3] - vals[2]) < 1e-12
    q, loss = q_method([[0.0, 0.0, 1.0]], [[1.0, 0.0, 0.0]], [1.0])
    assert loss < 1e-12
    a = attitude_matrix(q)
    assert rbm.norm(rbm.sub(rbm.matvec(a, [1.0, 0.0, 0.0]), [0.0, 0.0, 1.0])) < 1e-12
