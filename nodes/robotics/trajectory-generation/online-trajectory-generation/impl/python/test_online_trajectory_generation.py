# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-trajectory-generation/. The authors are listed in prov/T2ZEJ5.jsonl.
"""Tests: the profile reaches the target, respects the limits, is time-optimal, and the online loop reacts."""

import random

from online_trajectory_generation import envelope_reachable, evaluate, min_time_profile, otg_step


def check_profile(p0, v0, pT, vT, V, A):
    T, pieces = min_time_profile(p0, v0, pT, vT, V, A)
    assert abs(sum(d for d, _ in pieces) - T) < 1e-12
    assert all(d >= -1e-12 and abs(a) <= A + 1e-12 for d, a in pieces)
    p, v, _ = evaluate(p0, v0, pieces, T + 1)
    assert abs(p - pT) < 1e-9 and abs(v - vT) < 1e-9
    # The velocity stays within the limit at every piece boundary, and so inside each piece.
    t = 0.0
    for d, _ in pieces:
        t += d
        assert abs(evaluate(p0, v0, pieces, t)[1]) <= V + 1e-9
    return T


def test_worked_example():
    T = check_profile(0.0, 0.5, 1.0, 0.0, 1.0, 2.0)
    assert abs(T - 1.3125) < 1e-12


def test_rest_to_rest_matches_trapezoid():
    # D = 1, V = 1, A = 2: acceleration time 0.5, total 1.5. A short move gives a triangle.
    assert abs(check_profile(0.0, 0.0, 1.0, 0.0, 1.0, 2.0) - 1.5) < 1e-12
    assert abs(check_profile(0.0, 0.0, 0.25, 0.0, 1.0, 2.0) - 2 * (0.25 / 2) ** 0.5) < 1e-12
    assert abs(check_profile(3.0, 0.0, 2.0, 0.0, 1.0, 2.0) - 1.5) < 1e-12


def test_overshoot_case():
    # Fast toward a target that is close: the motion must pass it and come back.
    T, pieces = min_time_profile(0.0, 1.0, 0.1, 0.0, 1.0, 1.0)
    assert pieces[0][1] < 0
    check_profile(0.0, 1.0, 0.1, 0.0, 1.0, 1.0)


def test_random_states_against_brute_force():
    rng = random.Random(7)
    for _ in range(150):
        V = rng.uniform(0.5, 2.0)
        A = rng.uniform(0.5, 3.0)
        p0, pT = rng.uniform(-2, 2), rng.uniform(-2, 2)
        v0, vT = rng.uniform(-V, V), rng.uniform(-V, V)
        T = check_profile(p0, v0, pT, vT, V, A)
        # Reachable at T, and not reachable at any sampled earlier time.
        assert envelope_reachable(p0, v0, pT, vT, V, A, T, steps=400)
        for k in range(1, 40):
            t = T * k / 40 * 0.999
            assert not envelope_reachable(p0, v0, pT, vT, V, A, t, steps=400)


def test_online_loop_follows_the_one_shot_profile():
    p0, v0, pT, vT, V, A, dt = 0.0, 0.0, 2.0, 0.0, 1.0, 2.0, 0.01
    T, pieces = min_time_profile(p0, v0, pT, vT, V, A)
    p, v, t = p0, v0, 0.0
    for _ in range(1000):
        p, v, left = otg_step(p, v, pT, vT, V, A, dt)
        t += dt
        if left <= dt:
            break
        q, w, _ = evaluate(p0, v0, pieces, t)
        assert abs(p - q) < 1e-6 and abs(w - v) < 1e-6
    assert (p, v) == (pT, vT)
    assert abs(t - T) <= dt + 1e-9


def test_online_loop_reacts_to_new_target():
    V, A, dt = 1.0, 2.0, 0.005
    p, v = 0.0, 0.0
    target = 2.0
    steps = 0
    while (p, v) != (target, 0.0) and steps < 2000:
        if steps == 100:
            target = -1.0  # the target jumps while the axis moves at full speed
        prev = v
        p, v, _ = otg_step(p, v, target, 0.0, V, A, dt)
        assert abs(v) <= V + 1e-12
        assert abs(v - prev) <= A * dt + 1e-9
        steps += 1
    assert (p, v) == (-1.0, 0.0)


def test_bad_input():
    for args in ((0.0, 2.0, 1.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 0.0, 0.0, 1.0)):
        try:
            min_time_profile(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("bad input must fail")
