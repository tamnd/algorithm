# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/so3-logarithm-map/. The authors are listed in prov/7X28ZK.jsonl.
"""Tests of the logarithm map of SO(3).

The reference exponential is the power series of the matrix exponential,
summed to 60 terms, which is independent of Rodrigues' formula. The second
reference is rbm.so3_log, the shared helper.
"""

import math
import random

import rbm
from so3_logarithm_map import NEAR_PI, SMALL_THETA, axis_angle, log_textbook, so3_log


def series_exp(w, terms=60):
    """exp([w]) as the sum of [w]^k / k! for k < terms."""
    k = [[0.0, -w[2], w[1]], [w[2], 0.0, -w[0]], [-w[1], w[0], 0.0]]
    out = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    term = [row[:] for row in out]
    for n in range(1, terms):
        term = [[sum(term[i][m] * k[m][j] for m in range(3)) / n for j in range(3)] for i in range(3)]
        out = [[out[i][j] + term[i][j] for j in range(3)] for i in range(3)]
    return out


def unit(rng):
    while True:
        v = [rng.gauss(0.0, 1.0) for _ in range(3)]
        n = math.sqrt(sum(x * x for x in v))
        if n > 1e-3:
            return [x / n for x in v]


def vdiff(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def mdiff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(3) for j in range(3))


def test_check_value():
    r = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    w = so3_log(r)
    axis, theta = axis_angle(r)
    assert abs(theta - 2.0943951) < 1e-7
    assert abs(theta - 2.0 * math.pi / 3.0) < 1e-15
    assert vdiff(axis, [1.0 / math.sqrt(3.0)] * 3) < 1e-15
    assert vdiff(w, [2.0 * math.pi / 3.0 / math.sqrt(3.0)] * 3) < 1e-15
    assert mdiff(series_exp(w), r) < 1e-14


def test_simple_rotations():
    assert so3_log(rbm.eye(3)) == [0.0, 0.0, 0.0]
    assert axis_angle(rbm.eye(3)) == (None, 0.0)
    assert vdiff(so3_log(rbm.rot_z(math.pi / 2.0)), [0.0, 0.0, math.pi / 2.0]) < 1e-15
    assert vdiff(so3_log(rbm.rot_x(-0.3)), [-0.3, 0.0, 0.0]) < 1e-15
    # A rotation by 3 pi / 2 about z is a rotation by pi / 2 about -z.
    assert vdiff(so3_log(rbm.rot_z(1.5 * math.pi)), [0.0, 0.0, -math.pi / 2.0]) < 1e-15


def test_round_trip_against_power_series():
    rng = random.Random(11)
    for _ in range(300):
        w0 = [rng.uniform(0.0, math.pi) * x for x in unit(rng)]
        r = series_exp(w0)
        w = so3_log(r)
        assert vdiff(w, w0) < 1e-12
        assert mdiff(series_exp(w), r) < 1e-13
        assert math.sqrt(sum(x * x for x in w)) <= math.pi


def test_exp_of_log_for_any_rotation():
    rng = random.Random(12)
    for _ in range(200):
        # Angles beyond pi map back into [0, pi] with the opposite axis.
        w0 = [rng.uniform(0.0, 3.0 * math.pi) * x for x in unit(rng)]
        r = series_exp(w0, terms=90)
        w = so3_log(r)
        assert math.sqrt(sum(x * x for x in w)) <= math.pi + 1e-15
        assert mdiff(series_exp(w), r) < 1e-12


def test_agrees_with_helper():
    rng = random.Random(13)
    thetas = [0.0, 1e-12, 1e-6, SMALL_THETA, 1e-2, 0.5, 2.0, math.pi - 0.02, math.pi - 1e-3, math.pi - 1e-8]
    for th in thetas:
        for _ in range(20):
            r = rbm.so3_exp([th * x for x in unit(rng)])
            assert vdiff(so3_log(r), rbm.so3_log(r)) < 1e-14


def test_small_angles():
    rng = random.Random(14)
    for th in (1e-300, 1e-16, 1e-12, 1e-8, SMALL_THETA * (1.0 - 1e-9), SMALL_THETA * (1.0 + 1e-9), 3e-3):
        for _ in range(20):
            w0 = [th * x for x in unit(rng)]
            w = so3_log(series_exp(w0))
            assert vdiff(w, w0) <= 1e-14 * th


def test_near_pi():
    rng = random.Random(15)
    for d in (0.1, NEAR_PI * (1.0 - 1e-9), NEAR_PI * (1.0 + 1e-9), 1e-4, 1e-8, 1e-12):
        for _ in range(20):
            w0 = [(math.pi - d) * x for x in unit(rng)]
            w = so3_log(series_exp(w0))
            assert vdiff(w, w0) < 1e-12


def test_angle_pi_has_two_answers():
    rng = random.Random(16)
    for _ in range(50):
        u = unit(rng)
        # R = 2 u u^T - I is the rotation by pi about u, built exactly.
        r = [[2.0 * u[i] * u[j] - (1.0 if i == j else 0.0) for j in range(3)] for i in range(3)]
        w = so3_log(r)
        good = [math.pi * x for x in u]
        assert min(vdiff(w, good), vdiff(w, [-x for x in good])) < 1e-12
        assert mdiff(series_exp(w), r) < 1e-12
    # The rotation by pi about x: the skew part is exactly zero.
    w = so3_log([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]])
    assert w == [math.pi, 0.0, 0.0]


def test_textbook_method_loses_accuracy():
    axis = [2.0 / 7.0, 3.0 / 7.0, 6.0 / 7.0]
    # In the middle range both methods are accurate.
    w0 = [1.0 * a for a in axis]
    r = series_exp(w0)
    assert vdiff(log_textbook(r), w0) < 1e-14
    assert vdiff(so3_log(r), w0) < 1e-14
    # Near 0, arccos of a number near 1 loses half of the digits.
    w0 = [1e-9 * a for a in axis]
    r = series_exp(w0)
    assert vdiff(log_textbook(r), w0) > 1e-3 * 1e-9
    assert vdiff(so3_log(r), w0) <= 1e-14 * 1e-9
    # Near pi, the skew part is small and the division by sin(theta) fails.
    w0 = [(math.pi - 1e-6) * a for a in axis]
    r = series_exp(w0)
    assert vdiff(log_textbook(r), w0) > 1e-6
    assert vdiff(so3_log(r), w0) < 1e-14
