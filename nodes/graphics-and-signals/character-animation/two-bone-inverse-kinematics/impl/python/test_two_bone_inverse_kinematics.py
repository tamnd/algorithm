# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-bone-inverse-kinematics/. The authors are listed in prov/9Q6NF0.jsonl.
"""Tests of analytic two-bone IK.

They check the 2R check values, that forward kinematics of the result
reaches a reachable target within 1e-9 and keeps the bone lengths, that an
unreachable far target gives the straight limb pointing at it, that a near
target gives the folded limb, that the pole selects the plane and the side,
and that the 3D solution equals the planar closed form.
"""

import math
import random

import pytest

import anim
from two_bone_inverse_kinematics import (
    bend_angle,
    planar_fk,
    planar_two_bone,
    two_bone_ik,
)


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def rand_vec(rng, s=1.0):
    return tuple(rng.uniform(-s, s) for _ in range(3))


def test_check_values():
    th = planar_two_bone(1.0, 1.0, 1.0, 1.0, elbow=1)
    assert close(th, (0.0, math.pi / 2), 1e-12)
    th = planar_two_bone(1.0, 1.0, 1.0, 1.0, elbow=-1)
    assert close(th, (math.pi / 2, -math.pi / 2), 1e-12)
    assert abs(bend_angle(1.0, 1.0, math.sqrt(2.0)) - math.pi / 2) <= 1e-12
    # the 3D solver with the pole on the side of +x - y gives the elbow (1, 0, 0)
    e, f = two_bone_ik((0.0, 0.0, 0.0), (1.0, 1.0, 0.0), 1.0, 1.0, (2.0, -1.0, 0.0))
    assert close(e, (1.0, 0.0, 0.0), 1e-12) and close(f, (1.0, 1.0, 0.0), 1e-12)
    e, f = two_bone_ik((0.0, 0.0, 0.0), (1.0, 1.0, 0.0), 1.0, 1.0, (-1.0, 2.0, 0.0))
    assert close(e, (0.0, 1.0, 0.0), 1e-12)


def test_reachable_targets_and_lengths():
    rng = random.Random(1)
    for _ in range(500):
        a = rand_vec(rng, 2.0)
        l1, l2 = rng.uniform(0.2, 2.0), rng.uniform(0.2, 2.0)
        lo, hi = abs(l1 - l2), l1 + l2
        d = rng.uniform(lo + 1e-6, hi - 1e-6)
        t = anim.add(a, anim.scale(anim.normalize(rand_vec(rng)), d))
        e, f = two_bone_ik(a, t, l1, l2, anim.add(a, rand_vec(rng, 3.0)))
        assert close(f, t, 1e-9)
        assert abs(anim.norm(anim.sub(e, a)) - l1) <= 1e-9
        assert abs(anim.norm(anim.sub(f, e)) - l2) <= 1e-9


def test_planar_fk_of_ik():
    rng = random.Random(2)
    for _ in range(500):
        l1, l2 = rng.uniform(0.2, 2.0), rng.uniform(0.2, 2.0)
        d = rng.uniform(abs(l1 - l2) + 1e-6, l1 + l2 - 1e-6)
        phi = rng.uniform(-math.pi, math.pi)
        x, y = d * math.cos(phi), d * math.sin(phi)
        for elbow in (1, -1):
            th1, th2 = planar_two_bone(x, y, l1, l2, elbow)
            _, f = planar_fk(th1, th2, l1, l2)
            assert close(f, (x, y), 1e-9)


def test_unreachable_far_target_gives_straight_limb():
    rng = random.Random(3)
    for _ in range(200):
        a = rand_vec(rng)
        l1, l2 = rng.uniform(0.2, 2.0), rng.uniform(0.2, 2.0)
        u = anim.normalize(rand_vec(rng))
        t = anim.add(a, anim.scale(u, (l1 + l2) * rng.uniform(1.01, 3.0)))
        e, f = two_bone_ik(a, t, l1, l2, anim.add(a, rand_vec(rng, 3.0)))
        assert close(e, anim.add(a, anim.scale(u, l1)), 1e-9)
        assert close(f, anim.add(a, anim.scale(u, l1 + l2)), 1e-9)


def test_near_target_gives_folded_limb():
    a, t = (0.0, 0.0, 0.0), (0.1, 0.0, 0.0)
    e, f = two_bone_ik(a, t, 2.0, 1.0, (0.0, 1.0, 0.0))
    assert close(e, (2.0, 0.0, 0.0), 1e-12) and close(f, (1.0, 0.0, 0.0), 1e-12)
    e, f = two_bone_ik(a, t, 1.0, 2.0, (0.0, 1.0, 0.0))
    assert close(e, (-1.0, 0.0, 0.0), 1e-12) and close(f, (1.0, 0.0, 0.0), 1e-12)


def test_pole_selects_plane_and_side():
    rng = random.Random(4)
    for _ in range(300):
        a = rand_vec(rng)
        l1, l2 = rng.uniform(0.5, 1.5), rng.uniform(0.5, 1.5)
        d = rng.uniform(abs(l1 - l2) + 0.05, l1 + l2 - 0.05)
        x = anim.normalize(rand_vec(rng))
        t = anim.add(a, anim.scale(x, d))
        p = anim.add(a, rand_vec(rng, 3.0))
        e, _ = two_bone_ik(a, t, l1, l2, p)
        nrm = anim.cross(x, anim.sub(p, a))
        if anim.norm(nrm) < 1e-3:
            continue
        assert abs(anim.dot(anim.sub(e, a), anim.normalize(nrm))) <= 1e-9
        w = anim.sub(anim.sub(p, a), anim.scale(x, anim.dot(anim.sub(p, a), x)))
        assert anim.dot(anim.sub(e, a), w) >= 0.0


def test_3d_equals_planar_closed_form():
    rng = random.Random(5)
    for _ in range(300):
        l1, l2 = rng.uniform(0.2, 2.0), rng.uniform(0.2, 2.0)
        d = rng.uniform(abs(l1 - l2) + 1e-6, l1 + l2 - 1e-6)
        phi = rng.uniform(-math.pi, math.pi)
        x, y = d * math.cos(phi), d * math.sin(phi)
        th1, th2 = planar_two_bone(x, y, l1, l2, elbow=-1)
        e2, _ = planar_fk(th1, th2, l1, l2)
        # elbow = -1 bends clockwise, so the elbow is on the left of the target ray
        pole = (-math.sin(phi), math.cos(phi), 0.0)
        e, f = two_bone_ik((0.0, 0.0, 0.0), (x, y, 0.0), l1, l2, pole)
        assert close(e, (e2[0], e2[1], 0.0), 1e-9)
        assert abs(e[2]) <= 1e-12


def test_degenerate_inputs():
    with pytest.raises(ValueError):
        two_bone_ik((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 1.0, 1.0, (0.0, 1.0, 0.0))
    # a pole on the line through the root and the target still gives a valid limb
    e, f = two_bone_ik((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), 1.0, 1.0, (5.0, 0.0, 0.0))
    assert close(f, (1.0, 0.0, 0.0), 1e-12)
    assert abs(anim.norm(e) - 1.0) <= 1e-12 and abs(anim.norm(anim.sub(f, e)) - 1.0) <= 1e-12
    with pytest.raises(ValueError):
        planar_two_bone(3.0, 0.0, 1.0, 1.0)
