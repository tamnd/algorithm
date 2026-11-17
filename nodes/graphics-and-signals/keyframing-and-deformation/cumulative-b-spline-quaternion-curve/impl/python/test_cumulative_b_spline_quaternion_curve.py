# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cumulative-b-spline-quaternion-curve/. The authors are listed in prov/7V1M8B.jsonl.
import math
import random

import pytest

import anim
from cumulative_b_spline_quaternion_curve import (
    CumulativeBSplineQuaternionCurve,
    cumulative_basis,
)


def random_unit(rng):
    return anim.q_normalize(tuple(rng.gauss(0.0, 1.0) for _ in range(4)))


def random_keys(rng, n, spread=1.0):
    # A random walk on the sphere, so that adjacent keys are not too far apart.
    q = [random_unit(rng)]
    for _ in range(n - 1):
        axis = tuple(rng.gauss(0.0, 1.0) for _ in range(3))
        q.append(anim.q_mul(q[-1], anim.q_from_axis_angle(axis, rng.uniform(0.2, spread * 2.0))))
    return q


def same_rotation(p, q, tol):
    return min(anim.norm(anim.sub(p, q)), anim.norm(anim.add(p, q))) < tol


def uniform_cubic_bspline(c, j, u):
    # Reference: the scalar uniform cubic B-spline in the usual (not cumulative) basis.
    b = ((1 - u) ** 3 / 6, (3 * u**3 - 6 * u**2 + 4) / 6, (-3 * u**3 + 3 * u**2 + 3 * u + 1) / 6, u**3 / 6)
    return sum(bk * c[j + k] for k, bk in enumerate(b))


def test_cumulative_basis_values():
    assert cumulative_basis(0.0) == pytest.approx((5 / 6, 1 / 6, 0.0))
    assert cumulative_basis(1.0) == pytest.approx((1.0, 5 / 6, 1 / 6))
    assert cumulative_basis(0.5) == pytest.approx((0.9791666666666666, 0.5, 0.020833333333333332))


def test_unit_norm(rng=random.Random(1)):
    c = CumulativeBSplineQuaternionCurve(random_keys(rng, 8))
    for k in range(200):
        q = c(rng.uniform(0.0, c.segments()))
        assert abs(anim.q_dot(q, q) - 1.0) < 1e-12


def test_one_axis_reduces_to_the_scalar_b_spline(rng=random.Random(2)):
    axis = anim.normalize((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
    angles = [0.0]
    for _ in range(7):
        angles.append(angles[-1] + rng.uniform(-2.5, 2.5))
    keys = [anim.q_from_axis_angle(axis, a) for a in angles]
    c = CumulativeBSplineQuaternionCurve(keys)
    for j in range(c.segments()):
        for u in (0.0, 0.3, 0.5, 0.77, 1.0):
            ref = anim.q_from_axis_angle(axis, uniform_cubic_bspline(angles, j, u))
            assert same_rotation(c.segment(j, u), ref, 1e-12)


def test_does_not_pass_through_the_keys():
    z = (0.0, 0.0, 1.0)
    keys = [anim.q_from_axis_angle(z, a) for a in (0.0, 1.0, 0.0, 1.0)]
    c = CumulativeBSplineQuaternionCurve(keys)
    # At u = 0 the angle is (0 + 4 * 1 + 0) / 6, not the key angle 1.
    assert same_rotation(c.segment(0, 0.0), anim.q_from_axis_angle(z, 4.0 / 6.0), 1e-14)


def one_sided(f, t, h, side):
    # Values, first and second derivatives with second order one-sided differences.
    s = 1.0 if side > 0 else -1.0
    v = [f(t + s * k * h) for k in range(4)]
    d1 = [s * (-3 * a + 4 * b - c) / (2 * h) for a, b, c in zip(v[0], v[1], v[2])]
    d2 = [(2 * a - 5 * b + 4 * c - d) / (h * h) for a, b, c, d in zip(*v)]
    return v[0], d1, d2


def test_c2_at_the_joints(rng=random.Random(3)):
    c = CumulativeBSplineQuaternionCurve(random_keys(rng, 7))
    h = 1e-3
    for j in range(1, c.segments()):
        left = one_sided(lambda u: c.segment(j - 1, u), 1.0, h, -1)
        right = one_sided(lambda u: c.segment(j, u), 0.0, h, +1)
        assert anim.norm(anim.sub(left[0], right[0])) < 1e-13
        assert anim.norm(anim.sub(left[1], right[1])) < 1e-4
        assert anim.norm(anim.sub(left[2], right[2])) < 1e-3


def test_body_angular_velocity_against_differences(rng=random.Random(4)):
    c = CumulativeBSplineQuaternionCurve(random_keys(rng, 6))
    h = 1e-6
    for _ in range(30):
        j = rng.randrange(c.segments())
        u = rng.uniform(0.01, 0.99)
        q = c.segment(j, u)
        dq = tuple((a - b) / (2 * h) for a, b in zip(c.segment(j, u + h), c.segment(j, u - h)))
        w = anim.q_mul(anim.q_conj(q), dq)
        num = (2 * w[1], 2 * w[2], 2 * w[3])
        assert anim.norm(anim.sub(num, c.body_angular_velocity(j, u))) < 1e-7


def test_local_control(rng=random.Random(5)):
    keys = random_keys(rng, 9)
    c = CumulativeBSplineQuaternionCurve(keys)
    k = 4
    moved = list(keys)
    moved[k] = anim.q_mul(keys[k], anim.q_from_axis_angle((1, 2, 3), 0.7))
    d = CumulativeBSplineQuaternionCurve(moved)
    for j in range(c.segments()):
        diff = max(anim.norm(anim.sub(c.segment(j, u), d.segment(j, u))) for u in (0.0, 0.4, 1.0))
        if j <= k <= j + 3:
            assert diff > 1e-3
        else:
            assert diff < 1e-15


def test_frame_independence(rng=random.Random(6)):
    keys = random_keys(rng, 6)
    a, b = random_unit(rng), random_unit(rng)
    c = CumulativeBSplineQuaternionCurve(keys)
    d = CumulativeBSplineQuaternionCurve([anim.q_mul(anim.q_mul(a, q), b) for q in keys])
    for _ in range(40):
        t = rng.uniform(0.0, c.segments())
        assert same_rotation(d(t), anim.q_mul(anim.q_mul(a, c(t)), b), 1e-12)


def test_sign_of_the_keys_does_not_matter(rng=random.Random(7)):
    keys = random_keys(rng, 6)
    flipped = [q if i % 2 == 0 else tuple(-x for x in q) for i, q in enumerate(keys)]
    c = CumulativeBSplineQuaternionCurve(keys)
    d = CumulativeBSplineQuaternionCurve(flipped)
    for k in range(25):
        t = c.segments() * k / 24
        assert same_rotation(c(t), d(t), 1e-12)


def test_reversed_keys_give_a_slightly_different_curve(rng=random.Random(9)):
    keys = random_keys(rng, 5)
    c = CumulativeBSplineQuaternionCurve(keys)
    d = CumulativeBSplineQuaternionCurve(keys[::-1])
    gaps = []
    for t in (0.3, 1.0, 1.6):
        a, b = c(t), d(c.segments() - t)
        gaps.append(min(anim.norm(anim.sub(a, b)), anim.norm(anim.add(a, b))))
    assert max(gaps) > 1e-3 and max(gaps) < 0.1


def test_needs_four_keys():
    with pytest.raises(ValueError):
        CumulativeBSplineQuaternionCurve([(1.0, 0.0, 0.0, 0.0)] * 3)
