# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spherical-linear-interpolation/. The authors are listed in prov/BJ0DKQ.jsonl.
"""Tests of spherical linear interpolation.

The references are the power form q0 (q0* q1)^t, and the matrix form
R0 exp(t log(R0^T R1)) built from the shared helper rbm (so3_exp, so3_log
and quat_to_rot), which does not use quaternions for the interpolation.
"""

import math
import random

import rbm
from spherical_linear_interpolation import SMALL_ANGLE, slerp, slerp_power


def unit(rng, n=4):
    while True:
        v = [rng.gauss(0.0, 1.0) for _ in range(n)]
        s = math.sqrt(sum(x * x for x in v))
        if s > 1e-3:
            return [x / s for x in v]


def mdiff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(3) for j in range(3))


def qdiff(p, q):
    return max(abs(a - b) for a, b in zip(p, q))


def angle_between(p, q):
    """The rotation angle of p* q, in [0, pi], up to the sign of q."""
    a = math.sqrt(sum((x - y) ** 2 for x, y in zip(p, q)))
    b = math.sqrt(sum((x + y) ** 2 for x, y in zip(p, q)))
    return 4.0 * math.atan2(min(a, b), max(a, b))


def test_quarter_turn_about_z():
    q0 = [1.0, 0.0, 0.0, 0.0]
    q1 = rbm.quat_from_axis_angle([0.0, 0.0, 1.0], math.pi / 2.0)
    assert qdiff(q1, [0.70711, 0.0, 0.0, 0.70711]) < 1e-5
    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
        want = rbm.quat_from_axis_angle([0.0, 0.0, 1.0], t * math.pi / 2.0)
        assert qdiff(slerp(q0, q1, t), want) < 1e-15
    q = slerp(q0, q1, 0.25)
    assert abs(q[0] - 0.98079) < 1e-5 and abs(q[3] - 0.19509) < 1e-5


def test_end_points():
    rng = random.Random(1)
    for _ in range(200):
        q0, q1 = unit(rng), unit(rng)
        assert qdiff(slerp(q0, q1, 0.0), q0) < 1e-15
        sign = 1.0 if sum(a * b for a, b in zip(q0, q1)) >= 0.0 else -1.0
        assert qdiff(slerp(q0, q1, 1.0), [sign * x for x in q1]) < 1e-15


def test_against_power_form_and_matrix_form():
    rng = random.Random(2)
    for _ in range(200):
        q0, q1 = unit(rng), unit(rng)
        r0, r1 = rbm.quat_to_rot(q0), rbm.quat_to_rot(q1)
        w = rbm.so3_log(rbm.mul(rbm.transpose(r0), r1))
        if math.sqrt(sum(x * x for x in w)) > math.pi - 1e-3:
            continue
        for t in (0.1, 0.3, 0.5, 0.9):
            q = slerp(q0, q1, t)
            assert abs(sum(a * a for a in q) - 1.0) < 1e-14
            assert qdiff(q, slerp_power(q0, q1, t)) < 1e-13
            want = rbm.mul(r0, rbm.so3_exp([t * x for x in w]))
            assert mdiff(rbm.quat_to_rot(q), want) < 1e-12


def test_constant_angular_speed():
    rng = random.Random(3)
    for _ in range(50):
        q0, q1 = unit(rng), unit(rng)
        total = angle_between(q0, q1)
        steps = 10
        pts = [slerp(q0, q1, k / steps) for k in range(steps + 1)]
        for a, b in zip(pts, pts[1:]):
            assert abs(angle_between(a, b) - total / steps) < 1e-12


def test_one_fixed_axis():
    # Every intermediate rotation differs from q0 by a turn about one axis.
    rng = random.Random(4)
    for _ in range(50):
        q0, q1 = unit(rng), unit(rng)
        r0 = rbm.quat_to_rot(q0)
        axes = []
        for t in (0.2, 0.5, 0.8):
            r = rbm.quat_to_rot(slerp(q0, q1, t))
            w = rbm.so3_log(rbm.mul(rbm.transpose(r0), r))
            n = math.sqrt(sum(x * x for x in w))
            axes.append([x / n for x in w])
        for a in axes[1:]:
            assert qdiff(a, axes[0]) < 1e-10


def test_sign_flip_takes_the_short_arc():
    qa = rbm.quat_from_axis_angle([0.0, 0.0, 1.0], math.radians(170.0))
    qb = rbm.quat_from_axis_angle([0.0, 0.0, 1.0], math.radians(-170.0))
    assert sum(a * b for a, b in zip(qa, qb)) < 0.0
    mid = slerp(qa, qb, 0.5)
    # The short way from 170 to 190 degrees passes 180 degrees.
    assert qdiff(mid, [0.0, 0.0, 0.0, 1.0]) < 1e-15
    # The same rotations with the sign of qb changed give the same path.
    assert qdiff(slerp(qa, [-x for x in qb], 0.5), mid) < 1e-15


def test_small_angles():
    rng = random.Random(5)
    for scale in (1e-3, 1e-6, 0.5e-6, 1e-9, 1e-12, 0.0):
        for _ in range(50):
            q0 = unit(rng)
            u = unit(rng, 3)
            q1 = rbm.quat_mul(q0, rbm.quat_from_axis_angle(u, scale))
            for t in (0.0, 0.3, 1.0):
                want = rbm.quat_mul(q0, rbm.quat_from_axis_angle(u, t * scale)) if scale > 0.0 else q0
                q = slerp(q0, q1, t)
                assert qdiff(q, want) < 1e-15
                assert abs(sum(a * a for a in q) - 1.0) < 1e-15
    assert SMALL_ANGLE == 1e-6


def test_check_value_through_matrices():
    # Halfway from I to the rotation by 2 pi / 3 about (1, 1, 1) / sqrt(3).
    q = slerp([1.0, 0.0, 0.0, 0.0], [0.5, 0.5, 0.5, 0.5], 0.5)
    w = rbm.so3_log(rbm.quat_to_rot(q))
    assert max(abs(x - math.pi / 3.0 / math.sqrt(3.0)) for x in w) < 1e-14
    assert abs(q[0] - math.sqrt(3.0) / 2.0) < 1e-15
