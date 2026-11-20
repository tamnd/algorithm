# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/common-midpoint-stacking/. The authors are listed in prov/RJJQ5H.jsonl.

import math
import random

from common_midpoint_stacking import (
    cmp_stack,
    midpoint_bin,
    nominal_fold,
    sort_by_midpoint,
    stack_gather,
)


def ricker(t, f=25.0):
    a = (math.pi * f * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)


def event_trace(x, t0, v, dt, n, amp=1.0):
    tx = math.sqrt(t0 * t0 + (x / v) ** 2)
    return [amp * ricker(k * dt - tx) for k in range(n)]


def test_nominal_fold_value():
    assert nominal_fold(48, 25.0, 50.0) == 12.0


def test_fold_of_a_rolled_spread():
    # End-on spread: 48 receivers every 25 m from 100 m behind each shot; shots every 50 m.
    counts = {}
    for i in range(60):
        s = 50.0 * i
        for k in range(48):
            g = s + 100.0 + 25.0 * k
            b = midpoint_bin(s, g, 12.5)
            counts[b] = counts.get(b, 0) + 1
    assert max(counts.values()) == 12
    full = [b for b, c in counts.items() if c == 12]
    assert len(full) > 100
    assert sum(counts.values()) == 60 * 48


def test_sort_by_midpoint_groups_and_offsets():
    traces = [(0.0, 100.0, [1.0]), (25.0, 75.0, [2.0]), (50.0, 50.0, [3.0]), (0.0, 50.0, [4.0])]
    bins = sort_by_midpoint(traces, 25.0)
    assert sorted(bins) == [1, 2]
    assert sorted(x for x, _ in bins[2]) == [0.0, 50.0, 100.0]
    assert bins[1] == [(50.0, [4.0])]


def test_stack_recovers_the_zero_offset_event():
    dt, n = 0.004, 300
    offsets = [100.0 * i for i in range(12)]
    gather = [(x, event_trace(x, 0.6, 2200.0, dt, n)) for x in offsets]
    stack, fold = stack_gather(gather, dt, 2200.0)
    assert fold[:250] == [12] * 250
    assert stack[150] > 0.9
    wrong, _ = stack_gather(gather, dt, 1700.0)
    assert max(wrong) < 0.8


def test_noise_falls_like_one_over_root_fold():
    rng = random.Random(7)
    n, sigma = 4000, 1.0
    for nf in (4, 16):
        gather = [(0.0, [rng.gauss(0.0, sigma) for _ in range(n)]) for _ in range(nf)]
        stack, _ = stack_gather(gather, 0.004, 2000.0)
        var = sum(v * v for v in stack) / n
        assert abs(var * nf - sigma * sigma) < 0.12


def test_snr_gain_with_signal():
    rng = random.Random(8)
    nf, n, sigma = 9, 3000, 0.5
    signal = [math.sin(0.05 * k) for k in range(n)]
    gather = [(0.0, [s + rng.gauss(0.0, sigma) for s in signal]) for _ in range(nf)]
    stack, _ = stack_gather(gather, 0.004, 2000.0)
    noise_in = math.sqrt(sum((a - s) ** 2 for a, s in zip(gather[0][1], signal)) / n)
    noise_out = math.sqrt(sum((a - s) ** 2 for a, s in zip(stack, signal)) / n)
    assert abs(noise_in / noise_out - math.sqrt(nf)) < 0.3


def test_interpolation_does_not_raise_the_noise():
    rng = random.Random(9)
    n, nf = 1500, 10
    gather = [(150.0 * i, [rng.gauss(0.0, 1.0) for _ in range(n)]) for i in range(nf)]
    stack, _ = stack_gather(gather, 0.004, 2000.0)
    var = sum(v * v for v in stack[500:]) / (n - 500)
    assert var < 1.1 / nf


def test_live_fold_normalization_keeps_the_amplitude():
    dt, n = 0.004, 400
    offsets = [100.0 * i for i in range(10)]
    gather = [(x, [1.0] * n) for x in offsets]
    stack, fold = stack_gather(gather, dt, 2000.0, stretch_max=0.25)
    assert fold[10] < 10 and fold[300] == 10 and fold[-1] == 1
    for j in range(n):
        if fold[j] > 0:
            assert abs(stack[j] - 1.0) < 1e-12
        else:
            assert stack[j] == 0.0
    # Dividing by the nominal fold instead would dim the shallow part.
    assert fold[20] * stack[20] / 10 < 0.9


def test_cmp_stack_of_a_line():
    dt, n, v = 0.004, 250, 2000.0
    traces = []
    for i in range(8):
        s = 50.0 * i
        for k in range(8):
            g = s + 25.0 * k
            x = g - s
            traces.append((s, g, event_trace(x, 0.5, v, dt, n)))
    out = cmp_stack(traces, dt, v, 12.5)
    assert sum(len(fold) and max(fold) for _, fold in out.values()) == 64
    for b, (stack, fold) in out.items():
        assert stack[125] > 0.9
