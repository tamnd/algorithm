# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-window-approach/. The authors are listed in prov/0PW0PJ.jsonl.

import math
import random

from dynamic_window_approach import (
    INF,
    Robot,
    arc_distance,
    brake_pair,
    move,
    run,
    stopping_distance,
)


def sampled_distance(pose, v, w, obstacles, inflate, step, limit):
    """Walk along the path in small steps; return the first arc length inside an obstacle."""
    s = 0.0
    while s < limit:
        p = move(pose, v, w, s / v)
        if any(math.hypot(p[0] - ox, p[1] - oy) < r + inflate for ox, oy, r in obstacles):
            return s
        s += step
        if abs(w) > 1e-9 and s > 2 * math.pi * v / abs(w) + step:
            break
    return INF


def test_arc_distance_matches_dense_sampling():
    rng = random.Random(11)
    checked = 0
    limit = 6.0
    for _ in range(80):
        obs = [(rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(0.05, 0.4)) for _ in range(4)]
        pose = (0.0, 0.0, rng.uniform(-math.pi, math.pi))
        if any(math.hypot(ox, oy) <= r + 0.3 for ox, oy, r in obs):
            continue
        v = rng.uniform(0.1, 1.0)
        w = rng.choice([0.0, rng.uniform(-1.5, 1.5)])
        d = arc_distance(pose, v, w, obs, 0.3)
        ds = sampled_distance(pose, v, w, obs, 0.3, 2e-3, limit)
        if ds == INF:
            # The sampled walk found nothing: the exact distance is beyond the walk.
            assert d > limit - 1e-6 or abs(w) > 1e-9 and d > 2 * math.pi * v / abs(w) - 1e-6
            continue
        assert d <= ds + 1e-9 and ds - d < 2.5e-3
        checked += 1
    assert checked > 15


def test_stopping_distance_and_braking_stay_on_the_arc():
    rob = Robot()
    rng = random.Random(12)
    for _ in range(200):
        v = rng.uniform(0.0, rob.v_max)
        w = rng.uniform(-rob.w_max, rob.w_max)
        s = stopping_distance(v, w, rob)
        # Follow the braking sequence; each change respects the accelerations and keeps w / v.
        total, cv, cw = 0.0, v, w
        for _ in range(100):
            total += cv * rob.dt
            nv, nw = brake_pair(cv, cw, rob)
            assert cv - nv <= rob.a_v * rob.dt + 1e-12
            assert abs(cw - nw) <= rob.a_w * rob.dt + 1e-12
            if nv > 1e-12:
                assert abs(nw / nv - w / v) < 1e-9
            cv, cw = nv, nw
            if cv <= 1e-12:
                break
        assert abs(total - s) < 1e-9
        # The stopping distance shrinks by exactly v dt after one interval on the arc.
        bv, bw = brake_pair(v, w, rob)
        assert abs(stopping_distance(bv, bw, rob) - (s - v * rob.dt)) < 1e-9


def check_no_collision(obs, rob, log):
    for pose, vel, cmd in log:
        v, w = cmd
        if v > 0:
            free = arc_distance(pose, v, w, obs, rob.radius)
            assert v * rob.dt <= free + 1e-9
        assert vel[0] - rob.a_v * rob.dt - 1e-12 <= v <= vel[0] + rob.a_v * rob.dt + 1e-12
        assert abs(w - vel[1]) <= rob.a_w * rob.dt + 1e-12
        for ox, oy, r in obs:
            assert math.hypot(pose[0] - ox, pose[1] - oy) >= r + rob.radius - 1e-9


def test_random_fields_are_safe_and_reached():
    rob = Robot()
    rng = random.Random(13)
    for _ in range(4):
        obs = []
        while len(obs) < 14:
            o = (rng.uniform(1, 9), rng.uniform(-3, 3), rng.uniform(0.1, 0.5))
            if math.hypot(o[0], o[1]) > o[2] + 1.0 and math.hypot(o[0] - 10, o[1]) > o[2] + 1.0:
                obs.append(o)
        log = []
        _, steps, reached = run((0.0, 0.0, rng.uniform(-1, 1)), (10.0, 0.0), obs, rob, max_steps=300,
                                record=lambda p, vl, c: log.append((p, vl, c)),
                                nv=6, nw=11, alpha=1.0, beta=1.0, gamma=0.3)
        check_no_collision(obs, rob, log)
        assert reached and steps < 200


def test_brakes_in_front_of_a_wall():
    # A wall of discs across the path and the goal behind it: the robot must stop, not touch.
    rob = Robot()
    wall = [(3.0, y / 10.0, 0.06) for y in range(-60, 61)]
    log = []
    pose, _, reached = run((0.0, 0.0, 0.0), (6.0, 0.0), wall, rob, max_steps=120,
                           record=lambda p, vl, c: log.append((p, vl, c)), nv=6, nw=11)
    assert not reached
    check_no_collision(wall, rob, log)
    assert pose[0] < 3.0 - 0.36 + 1e-9


def test_passes_a_disc_beside_the_line():
    rob = Robot()
    obs = [(3.0, 0.6, 0.5)]
    log = []
    _, steps, reached = run((0.0, 0.0, 0.0), (6.0, 0.0), obs, rob, max_steps=200,
                            record=lambda p, vl, c: log.append((p, vl, c)))
    assert reached
    check_no_collision(obs, rob, log)
    assert steps < 60


def test_a_disc_on_the_line_is_a_local_minimum():
    # The heading term keeps the robot pointed at the goal; it stops in front of the disc.
    rob = Robot()
    obs = [(3.0, 0.0, 0.5)]
    log = []
    pose, _, reached = run((0.0, 0.0, 0.0), (6.0, 0.0), obs, rob, max_steps=200,
                           record=lambda p, vl, c: log.append((p, vl, c)), nv=6, nw=11)
    assert not reached
    check_no_collision(obs, rob, log)
    assert pose[0] < 3.0
