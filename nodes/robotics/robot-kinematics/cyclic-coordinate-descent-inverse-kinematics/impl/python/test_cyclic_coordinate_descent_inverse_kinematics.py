# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclic-coordinate-descent-inverse-kinematics/. The authors are listed in prov/JXW2FC.jsonl.
"""Tests of CCD inverse kinematics: the closed form angle of one joint against
a brute force grid over the angle, the in-place update of the end effector
against forward kinematics, the monotone error, the 2R example of the page
against the closed form solution, random 3D chains with reachable targets,
and the stretched chain for a target out of reach."""

import math
import random

from cyclic_coordinate_descent_inverse_kinematics import (
    add, best_angle, ccd_sweep, ik_ccd, joint_frames, norm, planar_chain, rotate, scale, sub)


def rand_unit(rng):
    while True:
        v = [rng.gauss(0.0, 1.0) for _ in range(3)]
        n = norm(v)
        if n > 1e-3:
            return scale(1.0 / n, v)


def rand_chain(rng, n):
    axes = [rand_unit(rng) for _ in range(n)]
    links = [[rng.uniform(-0.6, 0.6) for _ in range(3)] for _ in range(n)]
    return axes, links


def test_best_angle_against_a_grid():
    rng = random.Random(1)
    steps = 3600
    for _ in range(20):
        w = rand_unit(rng)
        p, e, t = ([rng.uniform(-1.0, 1.0) for _ in range(3)] for _ in range(3))

        def dist(phi):
            return norm(sub(add(p, rotate(w, phi, sub(e, p))), t))

        phi = best_angle(w, p, e, t)
        grid = min(dist(2.0 * math.pi * k / steps) for k in range(steps))
        assert dist(phi) <= grid + 1e-12
        # The grid point next to the optimum is within the grid error.
        assert grid - dist(phi) < 1e-4


def test_best_angle_reaches_a_point_on_the_circle():
    # If t lies on the circle that e sweeps, the distance becomes zero.
    rng = random.Random(2)
    for _ in range(20):
        w = rand_unit(rng)
        p, e = [rng.uniform(-1.0, 1.0) for _ in range(3)], [rng.uniform(-1.0, 1.0) for _ in range(3)]
        angle = rng.uniform(-3.0, 3.0)
        t = add(p, rotate(w, angle, sub(e, p)))
        phi = best_angle(w, p, e, t)
        assert norm(sub(add(p, rotate(w, phi, sub(e, p))), t)) < 1e-12
        assert abs(math.remainder(phi - angle, 2.0 * math.pi)) < 1e-9


def test_sweep_matches_forward_kinematics_and_error_never_increases():
    rng = random.Random(3)
    for _ in range(20):
        axes, links = rand_chain(rng, 6)
        q = [rng.uniform(-math.pi, math.pi) for _ in range(6)]
        target = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        err = norm(sub(joint_frames(axes, links, q)[2], target))
        for _ in range(5):
            # One joint at a time, by full forward kinematics, from the tip to the base.
            qq = list(q)
            for i in range(5, -1, -1):
                pos, wax, e = joint_frames(axes, links, qq)
                qq[i] += best_angle(wax[i], pos[i], e, target)
                new = norm(sub(joint_frames(axes, links, qq)[2], target))
                assert new <= err + 1e-12
                err = new
            q, e = ccd_sweep(axes, links, q, target)
            assert max(abs(a - b) for a, b in zip(q, qq)) < 1e-9
            assert norm(sub(e, joint_frames(axes, links, q)[2])) < 1e-12


def test_example_of_the_page():
    axes, links = planar_chain([1.0, 1.0])
    target = [1.0, 1.0, 0.0]
    q, e = ccd_sweep(axes, links, [0.3, 1.2], target)
    assert max(abs(a - b) for a, b in zip(q, [0.181657, 1.207482])) < 1e-6
    assert abs(norm(sub(e, target)) - 0.232222) < 1e-6
    q, errors, ok = ik_ccd(axes, links, target, [0.3, 1.2])
    assert ok and len(errors) - 1 == 33
    # The closed form solution with the elbow at 90 degrees.
    assert abs(q[0]) < 1e-9 and abs(q[1] - math.pi / 2.0) < 1e-9
    assert max(abs(a - b) for a, b in zip(errors[:5], [0.294173, 0.232222, 0.135220, 0.073280, 0.038185])) < 1e-6
    for a, b in zip(errors[10:30], errors[11:31]):
        assert abs(b / a - 0.5) < 1e-3
    assert all(b <= a for a, b in zip(errors, errors[1:]))


def test_reachable_targets_on_random_chains():
    rng = random.Random(4)
    solved = 0
    runs = 20
    for _ in range(runs):
        axes, links = rand_chain(rng, 6)
        q_star = [rng.uniform(-math.pi, math.pi) for _ in range(6)]
        target = joint_frames(axes, links, q_star)[2]
        q0 = [rng.uniform(-math.pi, math.pi) for _ in range(6)]
        q, errors, ok = ik_ccd(axes, links, target, q0, eps=1e-9, max_sweeps=3000)
        assert all(b <= a + 1e-12 for a, b in zip(errors, errors[1:]))
        assert abs(norm(sub(joint_frames(axes, links, q)[2], target)) - errors[-1]) < 1e-9
        if ok:
            solved += 1
            assert norm(sub(joint_frames(axes, links, q)[2], target)) <= 1e-9
    # CCD has no general guarantee, but with these seeds every run reaches its target.
    assert solved == runs


def test_target_out_of_reach_stretches_the_chain():
    lengths = [1.0, 0.7, 0.4]
    axes, links = planar_chain(lengths)
    for target in ([3.0, 1.0, 0.0], [-2.5, -0.5, 0.0], [0.2, 2.4, 0.0]):
        q, errors, ok = ik_ccd(axes, links, target, [0.4, 0.4, 0.4], max_sweeps=2000)
        assert not ok
        d = norm(target)
        assert abs(errors[-1] - (d - sum(lengths))) < 1e-6
        # The chain points straight at the target.
        assert abs(math.remainder(q[0] - math.atan2(target[1], target[0]), 2.0 * math.pi)) < 1e-3
        assert abs(math.remainder(q[1], 2.0 * math.pi)) < 1e-3 and abs(math.remainder(q[2], 2.0 * math.pi)) < 1e-3
