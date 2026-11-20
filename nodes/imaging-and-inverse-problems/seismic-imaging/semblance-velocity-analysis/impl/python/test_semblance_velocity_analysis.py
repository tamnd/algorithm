# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semblance-velocity-analysis/. The authors are listed in prov/8B18AH.jsonl.

import math
import random

from semblance_velocity_analysis import (
    pick_velocity,
    semblance,
    semblance_of_window,
    velocity_spectrum,
)


def ricker(t, f=25.0):
    a = (math.pi * f * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)


def gather_with_events(events, offsets, dt, n, rng=None, sigma=0.0):
    out = []
    for x in offsets:
        tr = [0.0] * n
        for t0, v, amp in events:
            tx = math.sqrt(t0 * t0 + (x / v) ** 2)
            for k in range(n):
                tr[k] += amp * ricker(k * dt - tx)
        if rng is not None:
            tr = [a + rng.gauss(0.0, sigma) for a in tr]
        out.append(tr)
    return out


def test_bounds_on_random_windows():
    rng = random.Random(1)
    for _ in range(200):
        n_tr = rng.randint(1, 10)
        rows = [[rng.gauss(0.0, 1.0) for _ in range(n_tr)] for _ in range(rng.randint(1, 8))]
        s = semblance_of_window(rows)
        assert -1e-15 <= s <= 1.0 + 1e-12


def test_equal_traces_give_one():
    rng = random.Random(2)
    row_vals = [rng.gauss(0.0, 1.0) for _ in range(9)]
    rows = [[v] * 6 for v in row_vals]
    assert abs(semblance_of_window(rows) - 1.0) < 1e-12


def test_one_live_trace_gives_one_over_n():
    rng = random.Random(3)
    rows = [[rng.gauss(0.0, 1.0)] + [0.0] * 4 for _ in range(7)]
    assert abs(semblance_of_window(rows) - 0.2) < 1e-12


def test_opposite_polarity_gives_zero():
    rows = [[v, -v] for v in (0.3, -1.2, 2.0)]
    assert semblance_of_window(rows) == 0.0
    assert semblance_of_window([[0.0, 0.0]]) == 0.0


def test_scale_invariance():
    rng = random.Random(4)
    rows = [[rng.gauss(0.0, 1.0) for _ in range(5)] for _ in range(4)]
    s1 = semblance_of_window(rows)
    s2 = semblance_of_window([[-3.5 * a for a in r] for r in rows])
    assert abs(s1 - s2) < 1e-12


def test_matches_the_definition_by_brute_force():
    rng = random.Random(5)
    dt, n = 0.004, 120
    offsets = [0.0, 150.0, 300.0, 450.0, 600.0]
    gather = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in offsets]
    j, v, w = 60, 2100.0, 4
    rows = []
    for k in range(j - w, j + w + 1):
        row = []
        for tr, x in zip(gather, offsets):
            t = math.sqrt((k * dt) ** 2 + (x / v) ** 2)
            u = t / dt
            i0 = int(math.floor(u))
            f = u - i0
            row.append((1 - f) * tr[i0] + f * tr[i0 + 1])
        rows.append(row)
    assert abs(semblance(gather, offsets, dt, j, v, w) - semblance_of_window(rows)) < 1e-12


def test_flat_event_at_the_right_velocity_gives_one():
    dt, n = 0.004, 250
    offsets = [0.0] * 6
    gather = gather_with_events([(0.5, 2000.0, 1.0)], offsets, dt, n)
    assert abs(semblance(gather, offsets, dt, 125, 2000.0, 5) - 1.0) < 1e-12


def test_picks_the_true_velocity_in_noise():
    rng = random.Random(6)
    dt, n = 0.004, 300
    offsets = [100.0 * i for i in range(16)]
    events = [(0.4, 1900.0, 1.0), (0.9, 2600.0, -1.0)]
    gather = gather_with_events(events, offsets, dt, n, rng, sigma=0.4)
    vels = [1500.0 + 50.0 * m for m in range(33)]
    spec = velocity_spectrum(gather, offsets, dt, vels, 5, times=[100, 225])
    assert abs(pick_velocity(spec[0], vels) - 1900.0) <= 50.0
    assert abs(pick_velocity(spec[1], vels) - 2600.0) <= 100.0
    assert max(spec[0]) > 0.5


def test_pure_noise_gives_about_one_over_n():
    rng = random.Random(7)
    n_tr, n = 8, 600
    offsets = [0.0] * n_tr
    gather = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(n_tr)]
    vals = [semblance(gather, offsets, 0.004, j, 2000.0, 5) for j in range(10, n - 10, 11)]
    mean = sum(vals) / len(vals)
    assert abs(mean - 1.0 / n_tr) < 0.03
