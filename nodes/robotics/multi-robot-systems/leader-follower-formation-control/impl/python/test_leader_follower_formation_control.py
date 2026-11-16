# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leader-follower-formation-control/. The authors are listed in prov/P77YSV.jsonl.

import math
import random

import pytest

from leader_follower_formation_control import (
    follower_input,
    separation_bearing,
    simulate,
    unicycle_rate,
    wrap,
)


def test_kinematics_match_finite_differences() -> None:
    # l' and psi' from the formulas against central differences of the geometry
    rng = random.Random(1)
    d, h = 0.2, 1e-6
    for _ in range(50):
        sl = (rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-3, 3))
        sf = (sl[0] + rng.uniform(-3, 3), sl[1] + rng.uniform(-3, 3), rng.uniform(-3, 3))
        vl, wl, vf, wf = (rng.uniform(-1, 1) for _ in range(4))
        l, psi, g = separation_bearing(sl, sf, d)
        if l < 0.3 or abs(abs(psi) - math.pi) < 0.1:
            continue

        def at(c):
            a = [p + c * q for p, q in zip(sl, unicycle_rate(sl, vl, wl))]
            b = [p + c * q for p, q in zip(sf, unicycle_rate(sf, vf, wf))]
            return separation_bearing(a, b, d)

        lp, pp, _ = at(h)
        lm, pm, _ = at(-h)
        dl = (lp - lm) / (2 * h)
        dpsi = wrap(pp - pm) / (2 * h)
        assert abs(dl - (vf * math.cos(g) + d * wf * math.sin(g) - vl * math.cos(psi))) < 1e-6
        want = (vl * math.sin(psi) - vf * math.sin(g) + d * wf * math.cos(g)) / l - wl
        assert abs(dpsi - want) < 1e-5


def test_hand_value() -> None:
    # leader at the origin heading +x; follower at (-1, 0) heading +x; d = 0.5
    # P_F = (-0.5, 0), so l = 0.5, psi = pi wrapped to -pi, gamma = -pi
    l, psi, g = separation_bearing((0, 0, 0), (-1, 0, 0), 0.5)
    assert abs(l - 0.5) < 1e-15 and abs(psi + math.pi) < 1e-15 and abs(g + math.pi) < 1e-15
    v, w = follower_input((0, 0, 0), 1.0, 0.0, (-1, 0, 0), 0.5, -math.pi, 0.5, 2.0, 1.0)
    # a = 2 (0.5 - 0.5) + cos(-pi) = -1, b = 0 - sin(-pi) = 0, v = a cos(-pi) = 1, w = 0
    assert abs(v - 1.0) < 1e-12 and abs(w) < 1e-12


def test_errors_decay_like_exponentials() -> None:
    rng = random.Random(2)
    d, a1, a2 = 0.1, 1.5, 0.8
    for _ in range(4):
        leader = (0.0, 0.0, rng.uniform(-1, 1))
        follower = (rng.uniform(-3, -1), rng.uniform(-1, 1), rng.uniform(-0.5, 0.5))
        ld, psid = 1.0, 2.5
        l0, psi0, _ = separation_bearing(leader, follower, d)

        def root(t):
            return 0.5, 0.2 * math.sin(t)

        for t in (0.5, 2.0):
            s = simulate([leader, follower], [-1, 0], [None, (ld, psid)], root, t, 0.002, d, a1, a2)
            l, psi, _ = separation_bearing(s[0], s[1], d)
            assert abs(l - (ld + (l0 - ld) * math.exp(-a1 * t))) < 1e-6
            assert abs(wrap(psi - psid) - wrap(psi0 - psid) * math.exp(-a2 * t)) < 1e-6


def test_internal_dynamics_closed_form() -> None:
    # Start at the target l and psi with a heading error e0, leader straight at v_L.
    # Then theta_L - theta_F = e obeys e' = -(v_L / d) sin e, so tan(e/2) = tan(e0/2) exp(-v_L t / d).
    d, vl, ld, psid = 0.25, 0.4, 1.0, math.pi * 0.8
    for e0 in (0.5, 2.0, -2.8):
        tf = -e0
        px, py = ld * math.cos(psid), ld * math.sin(psid)
        follower = (px - d * math.cos(tf), py - d * math.sin(tf), tf)
        for t in (1.0, 3.0):
            s = simulate([(0.0, 0.0, 0.0), follower], [-1, 0], [None, (ld, psid)],
                         lambda _t: (vl, 0.0), t, 0.002, d, 1.0, 1.0)
            e = wrap(s[0][2] - s[1][2])
            want = 2 * math.atan(math.tan(e0 / 2) * math.exp(-vl * t / d))
            assert abs(e - want) < 1e-6


def test_chain_of_three_reaches_formation() -> None:
    # a column: robot 1 behind robot 0, robot 2 behind robot 1, leader drives straight
    d = 0.1
    targets = [None, (1.0, math.pi), (1.0, math.pi)]
    s0 = [(0.0, 0.0, 0.0), (-2.0, 0.7, 0.4), (-3.5, -0.6, -0.3)]
    s = simulate(s0, [-1, 0, 1], targets, lambda _t: (0.5, 0.0), 30.0, 0.01, d, 1.0, 1.0)
    for i in (1, 2):
        l, psi, _ = separation_bearing(s[i - 1], s[i], d)
        assert abs(l - 1.0) < 1e-6 and abs(wrap(psi - math.pi)) < 1e-6
        assert abs(wrap(s[i][2] - s[0][2])) < 1e-3
    # in a straight column with equal headings the axles are 1 m apart on the line y = 0
    assert abs(s[1][1]) < 1e-3 and abs(s[2][1]) < 1e-3
    assert abs((s[0][0] - s[1][0]) - (1.0 + d)) < 1e-3


def test_rejects_bad_offset() -> None:
    with pytest.raises(ValueError):
        follower_input((0, 0, 0), 1.0, 0.0, (-1, 0, 0), 1.0, math.pi, 0.0, 1.0, 1.0)
