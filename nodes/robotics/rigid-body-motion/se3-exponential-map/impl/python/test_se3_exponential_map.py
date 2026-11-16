# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/se3-exponential-map/. The authors are listed in prov/25FNCG.jsonl.
"""Tests of the page code and of the shared helper rbm.py."""

import itertools
import math
import random

import pytest

import rbm
from se3_exponential_map import exp_coords, exp_screw, log_coords, screw_axis

TOL = 1e-12


def maxdiff(a, b):
    if a and isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def series_exp(m, terms=80):
    """Matrix exponential by its power series sum m^k / k!."""
    n = len(m)
    out = rbm.eye(n)
    term = rbm.eye(n)
    for k in range(1, terms):
        term = rbm.scale(rbm.mul(term, m), 1.0 / k)
        out = rbm.add(out, term)
    return out


def rand_unit(rng):
    while True:
        v = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        n = rbm.norm(v)
        if 0.1 < n <= 1.0:
            return [x / n for x in v]


def rand_xi(rng, tmax=math.pi):
    w = rbm.scale(rand_unit(rng), rng.uniform(0.0, tmax))
    return w + [rng.uniform(-2.0, 2.0) for _ in range(3)]


def is_pose(t):
    r = [row[:3] for row in t[:3]]
    assert maxdiff(rbm.mul(rbm.transpose(r), r), rbm.eye(3)) < TOL
    assert abs(rbm.det(r) - 1.0) < TOL
    assert t[3] == [0.0, 0.0, 0.0, 1.0]


# ---------------------------------------------------------------- page code


def test_check_value():
    s = screw_axis([0.0, 1.0, 0.0], [0.0, 0.0, 1.0], 0.0)
    assert maxdiff(s, [0.0, 0.0, 1.0, 1.0, 0.0, 0.0]) < TOL
    t = exp_screw(s, math.pi / 2.0)
    want = rbm.make_T(rbm.rot_z(math.pi / 2.0), [1.0, 1.0, 0.0])
    assert maxdiff(t, want) < TOL
    assert maxdiff(exp_coords(rbm.scale(s, math.pi / 2.0)), want) < TOL


def test_against_power_series_and_helper():
    rng = random.Random(1)
    for _ in range(150):
        xi = rand_xi(rng)
        t = exp_coords(xi)
        is_pose(t)
        assert maxdiff(t, series_exp(rbm.hat6(xi))) < 1e-11
        assert maxdiff(t, rbm.se3_exp(xi)) < TOL


def test_prismatic_and_errors():
    t = exp_screw([0.0, 0.0, 0.0, 0.0, 0.6, 0.8], 2.5)
    assert maxdiff(t, rbm.make_T(rbm.eye(3), [0.0, 1.5, 2.0])) < TOL
    assert maxdiff(exp_coords([0.0, 0.0, 0.0, 1.0, -2.0, 3.0]), rbm.make_T(rbm.eye(3), [1.0, -2.0, 3.0])) == 0.0
    with pytest.raises(ValueError):
        exp_screw([0.0, 0.0, 2.0, 0.0, 0.0, 0.0], 1.0)
    with pytest.raises(ValueError):
        exp_screw([0.0, 0.0, 0.0, 0.0, 0.0, 2.0], 1.0)


def test_small_angles_are_continuous():
    rng = random.Random(2)
    for _ in range(50):
        xi = rand_xi(rng)
        for th in (0.1, 1e-2 * (1 + 1e-9), 1e-2 * (1 - 1e-9), 1e-4, 1e-6, 1e-9, 1e-14):
            w = rbm.scale(rbm.scale(xi[:3], 1.0 / rbm.norm(xi[:3])), th)
            x = w + xi[3:]
            want = series_exp(rbm.hat6(x), 30)
            assert maxdiff(exp_coords(x), want) < 1e-13
            assert maxdiff(rbm.se3_exp(x), want) < 1e-13
            assert maxdiff(rbm.so3_exp(w), series_exp(rbm.hat3(w), 30)) < 1e-15


def test_screw_motion_geometry():
    rng = random.Random(3)
    for _ in range(50):
        q = [rng.uniform(-2.0, 2.0) for _ in range(3)]
        s_hat = rand_unit(rng)
        h = rng.uniform(-1.0, 1.0)
        th = rng.uniform(-6.0, 6.0)
        t = exp_screw(screw_axis(q, s_hat, h), th)
        # a point on the axis moves along the axis by h theta
        assert maxdiff(rbm.T_apply(t, q), rbm.add(q, rbm.scale(s_hat, h * th))) < 1e-11
        # one-parameter subgroup
        a, b = rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0)
        s = screw_axis(q, s_hat, h)
        assert maxdiff(rbm.mul(exp_screw(s, a), exp_screw(s, b)), exp_screw(s, a + b)) < 1e-11


def test_derivative_is_twist():
    rng = random.Random(4)
    for _ in range(20):
        s = screw_axis([rng.uniform(-1, 1) for _ in range(3)], rand_unit(rng), rng.uniform(-1, 1))
        th = rng.uniform(-3.0, 3.0)
        h = 1e-6
        d = rbm.scale(rbm.sub(exp_screw(s, th + h), exp_screw(s, th - h)), 1.0 / (2 * h))
        assert maxdiff(d, rbm.mul(rbm.hat6(s), exp_screw(s, th))) < 1e-6


def test_log_round_trips():
    rng = random.Random(5)
    for _ in range(200):
        xi = rand_xi(rng, math.pi - 1e-6)
        if rbm.norm(xi[:3]) < 1e-3:
            continue
        assert maxdiff(log_coords(exp_coords(xi)), xi) < 1e-10
    for _ in range(100):
        t = exp_coords(rand_xi(rng, 3.0 * math.pi))
        x = log_coords(t)
        assert rbm.norm(x[:3]) <= math.pi + 1e-12
        assert maxdiff(exp_coords(x), t) < 1e-11
        assert maxdiff(x, rbm.se3_log(t)) < 1e-9
    for th in (0.0, 1e-9, 1e-5, math.pi - 1e-3, math.pi - 1e-7, math.pi):
        for _ in range(10):
            xi = rbm.scale(rand_unit(rng), th) + [rng.uniform(-2, 2) for _ in range(3)]
            t = exp_coords(xi)
            assert maxdiff(exp_coords(log_coords(t)), t) < 1e-10


# ---------------------------------------------------------------- helper rbm


def test_rbm_self_test():
    assert rbm.self_test()


def test_rbm_linear_algebra():
    rng = random.Random(6)
    for n in range(1, 6):
        for _ in range(20):
            a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
            x = [rng.uniform(-1, 1) for _ in range(n)]
            b = rbm.matvec(a, x)
            assert maxdiff(rbm.matvec(a, rbm.solve(a, b)), b) < 1e-9
            assert maxdiff(rbm.mul(a, rbm.inv(a)), rbm.eye(n)) < 1e-8
            want = 0.0
            for perm in itertools.permutations(range(n)):
                sign = 1
                for i in range(n):
                    for j in range(i + 1, n):
                        if perm[i] > perm[j]:
                            sign = -sign
                prod = 1.0
                for i in range(n):
                    prod *= a[i][perm[i]]
                want += sign * prod
            assert abs(rbm.det(a) - want) < 1e-12
            spd = rbm.add(rbm.mul(a, rbm.transpose(a)), rbm.scale(rbm.eye(n), 0.1))
            low = rbm.cholesky(spd)
            assert all(low[i][j] == 0.0 for i in range(n) for j in range(i + 1, n))
            assert maxdiff(rbm.mul(low, rbm.transpose(low)), spd) < 1e-12
    with pytest.raises(ValueError):
        rbm.solve([[1.0, 2.0], [2.0, 4.0]], [1.0, 1.0])
    with pytest.raises(ValueError):
        rbm.cholesky([[1.0, 2.0], [2.0, 1.0]])
    assert rbm.det([[1.0, 2.0], [2.0, 4.0]]) == 0.0
    j = [[rng.uniform(-1, 1) for _ in range(5)] for _ in range(3)]
    jp = rbm.pinv_right(j)
    assert len(jp) == 5 and len(jp[0]) == 3
    assert maxdiff(rbm.mul(j, jp), rbm.eye(3)) < 1e-10
    assert rbm.zeros(2, 3) == [[0.0] * 3, [0.0] * 3]
    assert rbm.cross([1, 0, 0], [0, 1, 0]) == [0, 0, 1]
    assert rbm.dot([1, 2, 3], [4, 5, 6]) == 32
    assert rbm.norm([3.0, 4.0]) == 5.0
    assert rbm.sub([1, 2], [1, 1]) == [0, 1]
    m = rbm.solve([[2.0, 0.0], [0.0, 4.0]], [[2.0, 4.0], [4.0, 8.0]])
    assert m == [[1.0, 2.0], [1.0, 2.0]]


def test_rbm_hat_vee_and_rotations():
    rng = random.Random(7)
    for _ in range(50):
        a = [rng.uniform(-2, 2) for _ in range(3)]
        b = [rng.uniform(-2, 2) for _ in range(3)]
        assert maxdiff(rbm.matvec(rbm.hat3(a), b), rbm.cross(a, b)) < 1e-15
        assert rbm.vee3(rbm.hat3(a)) == a
        v = a + b
        assert rbm.vee6(rbm.hat6(v)) == v
        th = rng.uniform(-4, 4)
        assert maxdiff(rbm.rot_x(th), rbm.so3_exp([th, 0.0, 0.0])) < TOL
        assert maxdiff(rbm.rot_y(th), rbm.so3_exp([0.0, th, 0.0])) < TOL
        assert maxdiff(rbm.rot_z(th), rbm.so3_exp([0.0, 0.0, th])) < TOL
        r, p, y = (rng.uniform(-3, 3) for _ in range(3))
        want = rbm.mul(rbm.rot_z(y), rbm.mul(rbm.rot_y(p), rbm.rot_x(r)))
        assert maxdiff(rbm.rpy(r, p, y), want) < 1e-15
        w = rbm.scale(rand_unit(rng), rng.uniform(0.0, 3.0))
        rot = rbm.so3_exp(w)
        assert maxdiff(rot, series_exp(rbm.hat3(w))) < 1e-12
        assert maxdiff(rbm.mul(rbm.transpose(rot), rot), rbm.eye(3)) < TOL
        assert abs(rbm.det(rot) - 1.0) < TOL


def test_rbm_so3_log():
    rng = random.Random(8)
    for _ in range(200):
        w = rbm.scale(rand_unit(rng), rng.uniform(1e-3, math.pi - 1e-6))
        assert maxdiff(rbm.so3_log(rbm.so3_exp(w)), w) < 1e-10
    for th in (0.0, 1e-12, 1e-6, 1e-2 * (1 - 1e-9), 1e-2 * (1 + 1e-9), 0.5,math.pi - 0.02, math.pi - 1e-3, math.pi - 1e-8, math.pi):
        for _ in range(10):
            rot = rbm.so3_exp(rbm.scale(rand_unit(rng), th))
            w = rbm.so3_log(rot)
            assert rbm.norm(w) <= math.pi + 1e-15
            assert maxdiff(rbm.so3_exp(w), rot) < 1e-12
    w = rbm.so3_log(rbm.rot_x(math.pi))
    assert maxdiff(w, [math.pi, 0.0, 0.0]) < TOL
    assert rbm.so3_log(rbm.eye(3)) == [0.0, 0.0, 0.0]


def test_rbm_poses_and_adjoint():
    rng = random.Random(9)
    for _ in range(50):
        t1 = rbm.se3_exp(rand_xi(rng))
        t2 = rbm.se3_exp(rand_xi(rng))
        is_pose(t1)
        assert maxdiff(rbm.mul(t1, rbm.T_inv(t1)), rbm.eye(4)) < TOL
        x = [rng.uniform(-1, 1) for _ in range(3)]
        assert maxdiff(rbm.T_apply(t1, x), rbm.matvec(t1, x + [1.0])[:3]) < 1e-15
        a12 = rbm.adjoint(rbm.mul(t1, t2))
        assert maxdiff(a12, rbm.mul(rbm.adjoint(t1), rbm.adjoint(t2))) < 1e-11
        v = [rng.uniform(-1, 1) for _ in range(6)]
        lhs = rbm.mul(rbm.mul(t1, rbm.hat6(v)), rbm.T_inv(t1))
        assert maxdiff(lhs, rbm.hat6(rbm.matvec(rbm.adjoint(t1), v))) < 1e-11
        xi = rand_xi(rng, math.pi - 1e-6)
        if rbm.norm(xi[:3]) > 1e-3:
            assert maxdiff(rbm.se3_log(rbm.se3_exp(xi)), xi) < 1e-10
        assert maxdiff(rbm.se3_exp(rbm.se3_log(t1)), t1) < 1e-11


def test_rbm_quaternions():
    q = rbm.quat_from_axis_angle([0.0, 0.0, 1.0], math.pi / 2.0)
    assert maxdiff(q, [0.70711, 0.0, 0.0, 0.70711]) < 1e-5
    assert maxdiff(rbm.quat_to_rot(q), rbm.rot_z(math.pi / 2.0)) < TOL
    assert maxdiff(rbm.quat_from_axis_angle([1.0, 0.0, 0.0], math.pi), [0.0, 1.0, 0.0, 0.0]) < 1e-15
    assert rbm.quat_from_axis_angle([0.0, 0.0, 0.0], 0.0) == [1.0, 0.0, 0.0, 0.0]
    with pytest.raises(ValueError):
        rbm.quat_from_axis_angle([0.0, 0.0, 0.0], 1.0)
    rng = random.Random(10)
    for _ in range(50):
        a, b = rand_unit(rng), rand_unit(rng)
        ta, tb = rng.uniform(-4, 4), rng.uniform(-4, 4)
        qa = rbm.quat_from_axis_angle(rbm.scale(a, 2.5), ta)
        qb = rbm.quat_from_axis_angle(b, tb)
        ra = rbm.quat_to_rot(qa)
        assert maxdiff(ra, rbm.so3_exp(rbm.scale(a, ta))) < TOL
        assert maxdiff(rbm.quat_to_rot(rbm.quat_mul(qa, qb)), rbm.mul(ra, rbm.quat_to_rot(qb))) < TOL
        v = [rng.uniform(-1, 1) for _ in range(3)]
        rotated = rbm.quat_mul(rbm.quat_mul(qa, [0.0] + v), rbm.quat_conj(qa))
        assert abs(rotated[0]) < TOL
        assert maxdiff(rotated[1:], rbm.matvec(ra, v)) < TOL
        assert maxdiff(rbm.quat_to_rot(rbm.scale(qa, -3.0)), ra) < TOL


def test_rbm_num_jacobian():
    def f(x):
        return [math.sin(x[0]) * x[1], x[0] * x[0] + math.exp(x[1]), x[1]]

    x = [0.3, -0.7]
    want = [[math.cos(0.3) * -0.7, math.sin(0.3)], [0.6, math.exp(-0.7)], [0.0, 1.0]]
    assert maxdiff(rbm.num_jacobian(f, x, 1e-6), want) < 1e-8
    assert maxdiff(rbm.num_jacobian(f, x), want) < 1e-8
