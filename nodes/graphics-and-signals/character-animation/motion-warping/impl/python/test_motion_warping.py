# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-warping/. The authors are listed in prov/7QR9V6.jsonl.
"""Tests of motion warping.

The warped channel passes through every key, keys at the original values
change nothing, a linear offset is reproduced exactly, the offset spline is
C2 at the keys, the time warp is monotone and maps its pairs exactly, and
the scale curve is honored at the keys. Motion data is made in code.
"""

import math
import random

import motion_warping as mw


def channel(f, seed):
    rng = random.Random(seed)
    a, w, p = rng.uniform(0.2, 1.0), rng.uniform(0.1, 0.3), rng.uniform(0, 6)
    return [a * math.sin(w * i + p) + 0.1 * math.cos(0.05 * i) for i in range(f)]


def test_keys_are_met():
    rng = random.Random(1)
    th = channel(120, 2)
    keys = sorted((rng.uniform(0, 119), rng.uniform(-1, 1)) for _ in range(6))
    fn = mw.warp_channel(th, keys)
    for t, v in keys:
        assert abs(fn(t) - v) < 1e-12


def test_keys_on_the_curve_change_nothing():
    th = channel(80, 3)
    keys = [(10.0, th[10]), (40.0, th[40]), (70.0, th[70])]
    fn = mw.warp_channel(th, keys)
    assert max(abs(fn(t) - th[t]) for t in range(80)) < 1e-12


def test_linear_offset_is_exact():
    s = mw.NaturalSpline([0.0, 3.0, 7.0, 12.0, 20.0], [1.0 + 0.5 * x for x in (0.0, 3.0, 7.0, 12.0, 20.0)])
    for k in range(201):
        x = k / 10.0
        assert abs(s(x) - (1.0 + 0.5 * x)) < 1e-12


def test_spline_is_c2_at_the_keys():
    rng = random.Random(5)
    xs = [0.0, 2.0, 5.0, 6.0, 10.0, 13.0]
    ys = [rng.uniform(-1, 1) for _ in xs]
    s = mw.NaturalSpline(xs, ys)
    h = 1e-4
    for x in xs[1:-1]:
        left = (s(x) - 2 * s(x - h) + s(x - 2 * h)) / (h * h)
        right = (s(x + 2 * h) - 2 * s(x + h) + s(x)) / (h * h)
        d1l = (s(x) - s(x - h)) / h
        d1r = (s(x + h) - s(x)) / h
        assert abs(left - right) < 1e-2
        assert abs(d1l - d1r) < 1e-2
    # natural end conditions: zero second derivative at both ends
    for x, sgn in ((xs[0], 1), (xs[-1], -1)):
        d2 = (s(x) - 2 * s(x + sgn * h) + s(x + 2 * sgn * h)) / (h * h)
        assert abs(d2) < 1e-2


def test_timewarp_is_monotone_and_maps_pairs():
    tw = mw.TimeWarp([(0.0, 0.0), (30.0, 20.0), (90.0, 80.0), (100.0, 119.0)])
    vals = [tw(t / 4.0) for t in range(-40, 440)]
    assert all(b > a for a, b in zip(vals, vals[1:]))
    for n, o in [(0.0, 0.0), (30.0, 20.0), (90.0, 80.0), (100.0, 119.0)]:
        assert tw(n) == o
    try:
        mw.TimeWarp([(0.0, 0.0), (10.0, 5.0), (20.0, 4.0)])
        raised = False
    except ValueError:
        raised = True
    assert raised


def test_warp_motion_with_timewarp_and_keys():
    f = 120
    motion = [[a, b] for a, b in zip(channel(f, 7), channel(f, 8))]
    tw = mw.TimeWarp([(0.0, 0.0), (50.0, 30.0), (100.0, 119.0)])
    keys = {0: [(20.0, 0.5), (60.0, -0.2)]}
    out = mw.warp_motion(motion, keys, timewarp=tw)
    assert len(out) == 101
    assert abs(out[20][0] - 0.5) < 1e-12 and abs(out[60][0] + 0.2) < 1e-12
    # channel 1 has no keys: it is the original at the warped time
    ch1 = [m[1] for m in motion]
    for t in (0, 50, 100):
        assert abs(out[t][1] - mw.sample(ch1, tw(t))) < 1e-12


def test_scale_curve_at_keys():
    th = channel(60, 9)
    keys = [(5.0, 0.3), (30.0, 0.9), (55.0, -0.4)]
    scale = [(0.0, 1.0), (30.0, 2.0), (59.0, 1.0)]
    fn = mw.warp_channel(th, keys, scale_keys=scale)
    for t, v in keys:
        assert abs(fn(t) - v) < 1e-12
