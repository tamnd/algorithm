# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fabrik/. The authors are listed in prov/W25J11.jsonl.
"""Tests of FABRIK: the link lengths and the base after every pass, the
example of the page, the result turned into joint angles and checked by
forward kinematics, the 2R result against the closed form solutions, random
3D chains with targets in reach, the stretched chain for a target out of
reach, and the stall of a collinear start."""

import math
import random

from fabrik import backward_pass, chain_from_angles, dist, fabrik, forward_pass, planar_angles


def lengths_of(points):
    return [dist(a, b) for a, b in zip(points, points[1:])]


def test_passes_keep_lengths_and_base():
    rng = random.Random(1)
    for _ in range(30):
        n = rng.randint(2, 7)
        pts = [[0.0, 0.0, 0.0]]
        for _ in range(n):
            pts.append([c + rng.uniform(-1.0, 1.0) for c in pts[-1]])
        lengths = lengths_of(pts)
        target = [rng.uniform(-2.0, 2.0) for _ in range(3)]
        p = [list(x) for x in pts]
        for _ in range(5):
            backward_pass(p, lengths, target)
            assert p[-1] == target
            assert max(abs(a - b) for a, b in zip(lengths_of(p), lengths)) < 1e-12
            forward_pass(p, lengths, pts[0])
            assert p[0] == pts[0]
            assert max(abs(a - b) for a, b in zip(lengths_of(p), lengths)) < 1e-12


def test_example_of_the_page():
    lengths = [1.0, 0.8, 0.5]
    pts = chain_from_angles(lengths, [0.3, 0.4, 0.5])
    target = [1.2, 0.6]
    assert abs(dist(pts[3], target) - 0.871173) < 1e-6
    p = [list(x) for x in pts]
    backward_pass(p, lengths, target)
    assert max(abs(a - b) for a, b in zip(p[0], [0.066581, 0.022541])) < 1e-6
    forward_pass(p, lengths, [0.0, 0.0])
    assert max(abs(a - b) for a, b in zip(p[3], [1.142549, 0.568550])) < 1e-6
    p, errors, ok = fabrik(pts, lengths, target)
    assert ok and len(errors) - 1 == 232
    assert abs(errors[1] - 0.065496) < 1e-6
    assert all(b <= a for a, b in zip(errors, errors[1:]))
    assert abs(errors[200] / errors[199] - 0.9007) < 1e-4
    q = planar_angles(p)
    assert max(abs(a - b) for a, b in zip(q, [0.377886, -0.104655, 2.838020])) < 1e-6
    # Forward kinematics of the angles gives back the points.
    for a, b in zip(chain_from_angles(lengths, q), p):
        assert dist(a, b) < 1e-12
    assert dist(chain_from_angles(lengths, q)[3], target) < 1e-10


def test_two_link_against_the_closed_form():
    rng = random.Random(2)
    for _ in range(40):
        l1, l2 = rng.uniform(0.5, 1.5), rng.uniform(0.5, 1.5)
        q_star = [rng.uniform(-math.pi, math.pi), rng.uniform(0.2, 2.9) * rng.choice((-1, 1))]
        target = chain_from_angles([l1, l2], q_star)[2]
        start = chain_from_angles([l1, l2], [rng.uniform(-math.pi, math.pi), rng.uniform(0.2, 2.9)])
        p, errors, ok = fabrik(start, [l1, l2], target)
        assert ok
        q = planar_angles(p)
        # The closed form: the two elbow solutions.
        x, y = target
        c2 = (x * x + y * y - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
        sols = []
        for s in (1.0, -1.0):
            q2 = s * math.acos(max(-1.0, min(1.0, c2)))
            q1 = math.atan2(y, x) - math.atan2(l2 * math.sin(q2), l1 + l2 * math.cos(q2))
            sols.append([q1, q2])
        assert min(max(abs(math.remainder(a - b, 2.0 * math.pi)) for a, b in zip(q, sol)) for sol in sols) < 1e-6


def test_random_chains_with_targets_in_reach():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(3, 8)
        pts = [[0.0, 0.0, 0.0]]
        for _ in range(n):
            pts.append([c + rng.uniform(-1.0, 1.0) for c in pts[-1]])
        lengths = lengths_of(pts)
        # A target in reach: the end of the same chain in another pose.
        other = [[0.0, 0.0, 0.0]]
        for d in lengths:
            v = [rng.gauss(0.0, 1.0) for _ in range(3)]
            nv = math.sqrt(sum(x * x for x in v))
            other.append([c + d * x / nv for c, x in zip(other[-1], v)])
        target = other[-1]
        p, errors, ok = fabrik(pts, lengths, target, eps=1e-9, max_iter=20000)
        assert ok
        # The error never increases (Claim 4 of the proof page).
        assert all(b <= a + 1e-15 for a, b in zip(errors, errors[1:]))
        assert dist(p[-1], target) <= 1e-9 and p[0] == pts[0]
        assert max(abs(a - b) for a, b in zip(lengths_of(p), lengths)) < 1e-9


def test_target_out_of_reach():
    lengths = [1.0, 0.7, 0.4]
    start = chain_from_angles(lengths, [0.4, 0.4, 0.4])
    for target in ([3.0, 1.0], [-2.5, -0.5], [0.2, 2.4]):
        p, errors, ok = fabrik(start, lengths, target)
        assert not ok
        d = math.hypot(*target)
        assert abs(errors[-1] - (d - sum(lengths))) < 1e-12
        q = planar_angles(p)
        assert abs(math.remainder(q[0] - math.atan2(target[1], target[0]), 2.0 * math.pi)) < 1e-12
        assert abs(q[1]) < 1e-12 and abs(q[2]) < 1e-12


def test_collinear_start_stalls():
    # Every point stays on the x axis, where the end can only be at odd integers.
    lengths = [1.0, 1.0, 1.0]
    start = chain_from_angles(lengths, [0.0, 0.0, 0.0])
    p, errors, ok = fabrik(start, lengths, [0.1, 0.0], max_iter=200)
    assert not ok
    assert all(abs(pt[1]) == 0.0 for pt in p)
    assert abs(errors[-1] - 0.9) < 1e-12
    # A small bend of the start removes the stall.
    start = chain_from_angles(lengths, [0.0, 0.01, 0.0])
    p, errors, ok = fabrik(start, lengths, [0.1, 0.0], max_iter=20000)
    assert ok
