# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloch-equations/. The authors are listed in prov/YQ1113.jsonl.

import math
import random

import pytest

from bloch_equations import bloch_rk4, free_precession, larmor_hz, rotate


def close(a, b, tol):
    return max(abs(x - y) for x, y in zip(a, b)) < tol


def test_larmor_check_values():
    assert larmor_hz(1.5) / 1e6 == pytest.approx(63.87, abs=0.005)
    assert larmor_hz(3.0) / 1e6 == pytest.approx(127.73, abs=0.005)


def test_free_precession_matches_closed_form():
    rng = random.Random(31)
    for _ in range(5):
        m = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))
        w0 = 2 * math.pi * rng.uniform(-50, 50)
        t1, t2 = rng.uniform(0.3, 1.5), rng.uniform(0.03, 0.2)
        h, steps = 1e-4, 500
        got = bloch_rk4(m, lambda t: (0.0, 0.0, w0), t1, t2, 1.0, h, steps)
        want = free_precession(m, w0, t1, t2, 1.0, h * steps)
        assert close(got, want, 1e-7)


def test_hard_pulse_is_a_rotation():
    # On resonance with B1 along x, dM/dt = M x (w1, 0, 0) turns M by -w1 t about x.
    w1 = 2 * math.pi * 250.0
    tau = 1e-3  # 90 degree pulse: w1 tau = pi / 2
    got = bloch_rk4((0.0, 0.0, 1.0), lambda t: (w1, 0.0, 0.0), math.inf, math.inf, 1.0, 1e-6, 1000)
    assert close(got, rotate((0.0, 0.0, 1.0), (1.0, 0.0, 0.0), -w1 * tau), 1e-10)
    assert close(got, (0.0, 1.0, 0.0), 1e-10)


def test_length_is_kept_without_relaxation():
    rng = random.Random(32)
    m = (0.3, -0.4, 0.5)
    w = (rng.uniform(-900, 900), rng.uniform(-900, 900), rng.uniform(-900, 900))
    got = bloch_rk4(m, lambda t: w, math.inf, math.inf, 1.0, 1e-5, 1000)
    assert math.sqrt(sum(v * v for v in got)) == pytest.approx(math.sqrt(0.5), rel=1e-9)
    # The same motion in closed form: a turn by -|w| t about w / |w|.
    nw = math.sqrt(sum(v * v for v in w))
    want = rotate(m, tuple(v / nw for v in w), -nw * 1e-2)
    assert close(got, want, 1e-9)


def test_t2_decay_and_inversion_null():
    got = bloch_rk4((1.0, 0.0, 0.0), lambda t: (0.0, 0.0, 0.0), 1.0, 0.1, 1.0, 1e-4, 500)
    assert math.hypot(got[0], got[1]) == pytest.approx(math.exp(-0.5), rel=1e-10)
    t1 = 0.8
    tnull = t1 * math.log(2.0)
    steps = 1000
    got = bloch_rk4((0.0, 0.0, -1.0), lambda t: (0.0, 0.0, 0.0), t1, 0.05, 1.0, tnull / steps, steps)
    assert abs(got[2]) < 1e-12
