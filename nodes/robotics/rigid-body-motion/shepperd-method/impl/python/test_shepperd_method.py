# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shepperd-method/. The authors are listed in prov/DK6ZQE.jsonl.
"""Tests of Shepperd's method.

The references are the shared helper rbm: quat_to_rot (quaternion to
matrix) for the round trip, and so3_log with quat_from_axis_angle as a
second, independent way from the matrix to the quaternion.
"""

import math
import random

import rbm
from shepperd_method import branch, quat_textbook, shepperd


def unit(rng, n=3):
    while True:
        v = [rng.gauss(0.0, 1.0) for _ in range(n)]
        s = math.sqrt(sum(x * x for x in v))
        if s > 1e-3:
            return [x / s for x in v]


def mdiff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(3) for j in range(3))


def qdiff(p, q):
    """Distance of two quaternions up to the sign, since q and -q agree."""
    return min(max(abs(a - b) for a, b in zip(p, q)), max(abs(a + b) for a, b in zip(p, q)))


def test_check_values():
    q = shepperd(rbm.rot_z(math.pi / 2.0))
    assert qdiff(q, [math.sqrt(0.5), 0.0, 0.0, math.sqrt(0.5)]) < 1e-15
    assert abs(q[0] - 0.70711) < 1e-5 and abs(q[3] - 0.70711) < 1e-5
    # The rotation by 2 pi / 3 about (1, 1, 1) / sqrt(3).
    q = shepperd([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    assert q == [0.5, 0.5, 0.5, 0.5]
    # The rotation by pi about x: w = 0, and the x branch is used.
    r = [[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]]
    assert branch(r) == 1
    assert shepperd(r) == [0.0, 1.0, 0.0, 0.0]


def test_rotations_by_pi_about_each_axis():
    # The identity and the three half turns use the four branches.
    cases = [
        ([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], 0, [1.0, 0.0, 0.0, 0.0]),
        ([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]], 1, [0.0, 1.0, 0.0, 0.0]),
        ([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]], 2, [0.0, 0.0, 1.0, 0.0]),
        ([[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]], 3, [0.0, 0.0, 0.0, 1.0]),
    ]
    for r, k, want in cases:
        assert branch(r) == k
        assert shepperd(r) == want


def test_all_four_branches_on_random_rotations():
    rng = random.Random(1)
    seen = [0, 0, 0, 0]
    for _ in range(2000):
        q0 = unit(rng, 4)
        r = rbm.quat_to_rot(q0)
        q = shepperd(r)
        seen[branch(r)] += 1
        assert abs(sum(a * a for a in q) - 1.0) < 1e-14
        assert q[0] >= 0.0
        assert qdiff(q, q0) < 1e-14
        assert mdiff(rbm.quat_to_rot(q), r) < 1e-14
    # Each branch is used for a fair share of uniform random rotations.
    assert min(seen) > 200


def test_branch_picks_the_largest_component():
    rng = random.Random(2)
    for _ in range(500):
        q0 = unit(rng, 4)
        k = branch(rbm.quat_to_rot(q0))
        # Ties are broken by rounding, so allow a tiny gap.
        assert abs(q0[k]) >= max(abs(a) for a in q0) - 1e-12
        assert abs(q0[k]) >= 0.5 - 1e-12


def test_against_log_and_axis_angle():
    rng = random.Random(3)
    for _ in range(300):
        axis = unit(rng)
        angle = rng.uniform(0.0, math.pi - 0.05)
        r = rbm.so3_exp([angle * a for a in axis])
        w = rbm.so3_log(r)
        th = math.sqrt(sum(x * x for x in w))
        ref = rbm.quat_from_axis_angle(w, th) if th > 0.0 else [1.0, 0.0, 0.0, 0.0]
        assert qdiff(shepperd(r), ref) < 1e-13


def test_half_turns_about_random_axes():
    rng = random.Random(4)
    for _ in range(300):
        u = unit(rng)
        # R = 2 u u^T - I is the rotation by pi about u, built exactly.
        r = [[2.0 * u[i] * u[j] - (1.0 if i == j else 0.0) for j in range(3)] for i in range(3)]
        q = shepperd(r)
        assert qdiff(q, [0.0] + u) < 1e-15
        assert mdiff(rbm.quat_to_rot(q), r) < 1e-15


def test_near_pi_textbook_formula_fails():
    axis = [2.0 / 7.0, 3.0 / 7.0, 6.0 / 7.0]
    for d, bad in ((1e-3, 1e-10), (1e-5, 1e-7), (1e-7, 1e-3)):
        angle = math.pi - d
        r = rbm.so3_exp([angle * a for a in axis])
        ref = rbm.quat_from_axis_angle(axis, angle)
        assert qdiff(shepperd(r), ref) < 1e-15
        assert qdiff(quat_textbook(r), ref) > bad
    r = [[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]]
    try:
        quat_textbook(r)
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError("the textbook formula should divide by zero at w = 0")


def test_matrix_with_small_error():
    # A rotation with entries rounded to 7 digits still gives a quaternion
    # within about 1e-7, and of length within 1e-6 of 1.
    rng = random.Random(5)
    for _ in range(200):
        q0 = unit(rng, 4)
        r = [[round(x, 7) for x in row] for row in rbm.quat_to_rot(q0)]
        q = shepperd(r)
        assert qdiff(q, q0) < 1e-6
        assert abs(math.sqrt(sum(a * a for a in q)) - 1.0) < 1e-6
