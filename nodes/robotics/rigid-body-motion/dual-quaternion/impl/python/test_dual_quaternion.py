# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-quaternion/. The authors are listed in prov/YTDVB1.jsonl.
"""Tests of the dual quaternion operations against the 4x4 poses of rbm."""

import math
import random

import rbm
from dual_quaternion import apply, conj_both, from_pose, from_screw, mul, to_matrix, to_pose

TOL = 1e-12


def maxdiff(a, b):
    if a and isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def quat_of(r):
    """Unit quaternion of a rotation matrix, through so3_log (rbm has no direct map)."""
    w = rbm.so3_log(r)
    th = rbm.norm(w)
    if th == 0.0:
        return [1.0, 0.0, 0.0, 0.0]
    return rbm.quat_from_axis_angle(w, th)


def dq_of(t):
    return from_pose(quat_of([row[:3] for row in t[:3]]), [t[0][3], t[1][3], t[2][3]])


def random_pose(rng):
    xi = [rng.uniform(-1.5, 1.5) for _ in range(3)] + [rng.uniform(-3.0, 3.0) for _ in range(3)]
    return rbm.se3_exp(xi)


def same_up_to_sign(a, b):
    fa = a[0] + a[1]
    fb = b[0] + b[1]
    return min(maxdiff(fa, fb), maxdiff(fa, [-x for x in fb]))


def test_check_values():
    h = math.pi / 2.0
    t = rbm.se3_exp([0.0, 0.0, h, h, 0.0, 0.0])
    s = dq_of(t)
    c = math.sqrt(0.5)
    assert maxdiff(s[0], [c, 0.0, 0.0, c]) < TOL
    assert maxdiff(s[1], [0.0, c, 0.0, 0.0]) < TOL
    q, p = to_pose(s)
    assert maxdiff(p, [1.0, 1.0, 0.0]) < TOL
    assert maxdiff(to_matrix(s), rbm.make_T(rbm.rot_z(h), [1.0, 1.0, 0.0])) < TOL
    # The same motion as the screw about the line through (0, 1, 0), pitch 0.
    assert same_up_to_sign(from_screw([0.0, 0.0, 1.0], [0.0, 1.0, 0.0], 0.0, h), s) < TOL
    # A half turn about x has the quaternion (0, 1, 0, 0).
    assert maxdiff(quat_of(rbm.rot_x(math.pi)), [0.0, 1.0, 0.0, 0.0]) < TOL


def test_unit_conditions_and_round_trip():
    rng = random.Random(1)
    for _ in range(200):
        t = random_pose(rng)
        s = dq_of(t)
        assert abs(rbm.dot(s[0], s[0]) - 1.0) < TOL
        assert abs(rbm.dot(s[0], s[1])) < TOL
        assert maxdiff(to_matrix(s), t) < 1e-11


def test_product_composes_poses():
    rng = random.Random(2)
    for _ in range(200):
        t1, t2 = random_pose(rng), random_pose(rng)
        assert same_up_to_sign(mul(dq_of(t1), dq_of(t2)), dq_of(rbm.mul(t1, t2))) < 1e-11
        assert maxdiff(to_matrix(mul(dq_of(t1), dq_of(t2))), rbm.mul(t1, t2)) < 1e-11


def test_apply_moves_points():
    rng = random.Random(3)
    for _ in range(200):
        t = random_pose(rng)
        x = [rng.uniform(-2.0, 2.0) for _ in range(3)]
        assert maxdiff(apply(dq_of(t), x), rbm.T_apply(t, x)) < 1e-11


def test_double_cover():
    rng = random.Random(4)
    for _ in range(100):
        s = dq_of(random_pose(rng))
        neg = [[-x for x in s[0]], [-x for x in s[1]]]
        assert maxdiff(to_matrix(neg), to_matrix(s)) < TOL
        x = [rng.uniform(-2.0, 2.0) for _ in range(3)]
        assert maxdiff(apply(neg, x), apply(s, x)) < TOL


def test_inverse_is_the_conjugate():
    rng = random.Random(5)
    for _ in range(100):
        t = random_pose(rng)
        s = dq_of(t)
        inv = [rbm.quat_conj(s[0]), rbm.quat_conj(s[1])]
        assert maxdiff(to_matrix(inv), rbm.T_inv(t)) < 1e-11
        one = mul(s, inv)
        assert maxdiff(one[0] + one[1], [1.0, 0, 0, 0, 0, 0, 0, 0]) < 1e-12
        assert len(conj_both(s)) == 2


def test_screw_form_matches_exponential():
    rng = random.Random(6)
    for _ in range(200):
        w = [rng.gauss(0.0, 1.0) for _ in range(3)]
        s = [x / rbm.norm(w) for x in w]
        q = [rng.uniform(-2.0, 2.0) for _ in range(3)]
        h = rng.uniform(-1.0, 1.0)
        th = rng.uniform(-3.0, 3.0)
        v = rbm.add(rbm.scale(rbm.cross(s, q), -1.0), rbm.scale(s, h))
        t = rbm.se3_exp([x * th for x in s + v])
        assert same_up_to_sign(from_screw(s, q, h, th), dq_of(t)) < 1e-11
        assert maxdiff(to_matrix(from_screw(s, q, h, th)), t) < 1e-11
