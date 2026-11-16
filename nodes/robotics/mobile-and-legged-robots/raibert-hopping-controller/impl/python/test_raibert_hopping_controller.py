# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raibert-hopping-controller/. The authors are listed in prov/V4NCCQ.jsonl.
# Stance: RK4 with dt = 1e-3 s, lift-off located by bisection. Flight: closed form.

import math
import random

from raibert_hopping_controller import Gains, Hopper, foot_placement, run, vertical_stance_time

MAX_STEPS = 10000


def test_vertical_stance_time_matches_closed_form():
    # No thrust, no damping, leg vertical: the stance is a half-period of a
    # shifted harmonic oscillator, t_s = (2 pi - 2 alpha) / w.
    robot = Hopper()
    recs, _ = run(robot, Gains(), [0.0, 0.7, 0.0, 0.0, 0.0, 0.0], 3)
    v = math.sqrt(2 * robot.g * (0.7 - robot.l0))
    want = vertical_stance_time(robot, v)
    for rec in recs:
        assert abs(rec["ts"] - want) < 1e-8
        assert abs(rec["apex"] - 0.7) < 1e-8
    assert sum(r["steps"] for r in recs) < MAX_STEPS


def test_energy_is_conserved_without_thrust_and_damping():
    robot = Hopper()
    rng = random.Random(5)
    s = [0.0, 0.7, rng.uniform(-0.2, 0.2), rng.uniform(0.3, 0.8), 0.0, rng.uniform(-0.5, 0.5)]
    e0 = robot.energy(s)
    recs, s_end = run(robot, Gains(), s, 5)
    assert abs(robot.energy(s_end) - e0) < 1e-6 * e0
    assert sum(r["steps"] for r in recs) < MAX_STEPS


def test_thrust_and_damping_give_one_hop_height():
    robot = Hopper(b=40.0)
    gains = Gains(delta=0.03)
    finals = []
    total = 0
    for z in (0.6, 0.9):
        recs, _ = run(robot, gains, [0.0, z, 0.0, 0.0, 0.0, 0.0], 15)
        apex = [r["apex"] for r in recs]
        total += sum(r["steps"] for r in recs)
        # The change per hop shrinks, as for a stable fixed point.
        assert abs(apex[-1] - apex[-2]) < 0.5 * abs(apex[2] - apex[1])
        finals.append(apex[-1])
    assert abs(finals[0] - finals[1]) < 0.01
    assert total < MAX_STEPS


def test_foot_placement_sign():
    # A foot ahead of the neutral point slows the hopper; behind, it speeds up.
    robot = Hopper(b=20.0)
    out = []
    for k_x in (0.05, -0.05):
        gains = Gains(delta=0.02, k_x=k_x, k_p=800.0, k_v=60.0)
        _, s = run(robot, gains, [0.0, 0.7, 0.0, 0.5, 0.0, 0.0], 1)
        out.append(s[3])
    assert out[0] < 0.1 < 0.5 < out[1]
    assert foot_placement(0.5, 0.0, 0.17, 0.05, 0.5) > foot_placement(0.5, 0.0, 0.17, 0.0, 0.5) > 0


def test_stops_in_place_and_levels_the_body():
    robot = Hopper(b=20.0)
    gains = Gains(delta=0.02, k_x=0.03, k_p=800.0, k_v=60.0, vx_d=0.0)
    recs, _ = run(robot, gains, [0.0, 0.7, 0.2, 0.5, 0.0, 0.0], 20)
    assert abs(recs[-1]["vx"]) < 1e-3
    assert abs(recs[-1]["phi_td"]) < 1e-3
    assert abs(recs[1]["phi_td"]) < 0.1
    assert sum(r["steps"] for r in recs) < MAX_STEPS


def test_speed_settles_below_the_target():
    # The neutral point vx Ts / 2 is an estimate. On this model it is too far
    # forward, so the speed settles below vx_d, closer for a larger k_x.
    robot = Hopper(b=20.0)
    finals = []
    total = 0
    for k_x in (0.02, 0.05):
        gains = Gains(delta=0.02, k_x=k_x, k_p=800.0, k_v=60.0, vx_d=0.5)
        recs, _ = run(robot, gains, [0.0, 0.7, 0.0, 0.0, 0.0, 0.0], 16)
        total += sum(r["steps"] for r in recs)
        v = [r["vx"] for r in recs]
        assert abs(v[-1] - v[-2]) < 2e-3
        finals.append(v[-1])
    assert 0.25 < finals[0] < finals[1] < 0.5
    assert total < MAX_STEPS
