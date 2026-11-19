# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rapt-pitch-tracker/. The authors are listed in prov/D01A4J.jsonl.

import itertools
import math
import random

from nlsdsp import all_pole, pulse_train, white_noise
from rapt_pitch_tracker import PARAMS, dp, itakura_ratio, nccf, peaks, rapt, transition_cost

FS = 8000
BETA = 0.3 / 160  # LAG_WT / L_max with F0min = 50 Hz at 8 kHz


def test_nccf_matches_the_definition_and_is_bounded():
    rng = random.Random(1)
    x = [rng.uniform(-1, 1) for _ in range(300)]
    m, n, lo, hi = 17, 40, 5, 120
    phi = nccf(x, m, n, lo, hi)
    for k in range(lo, hi + 1):
        num = sum(x[m + j] * x[m + j + k] for j in range(n))
        e0 = sum(x[m + j] ** 2 for j in range(n))
        ek = sum(x[m + k + j] ** 2 for j in range(n))
        assert abs(phi[k - lo] - num / math.sqrt(e0 * ek)) < 1e-12
        assert abs(phi[k - lo]) <= 1 + 1e-12


def test_nccf_is_one_at_the_period_of_a_periodic_signal():
    x = all_pole(pulse_train(200, FS, 400), [1.2, -0.5])  # period 40
    x = x[100:]  # past the start, the signal repeats every 40 samples to rounding
    phi = nccf(x, 0, 60, 15, 161)
    for k in (40, 80, 120, 160):
        assert abs(phi[k - 15] - 1) < 1e-9
    assert max(phi[k - 15] for k in range(15, 39)) < 0.99


def test_peaks_are_the_local_maxima_above_the_relative_threshold():
    rng = random.Random(2)
    for _ in range(200):
        phi = [rng.uniform(-0.5, 1.0) for _ in range(30)]  # lags 10 .. 39
        got = peaks(phi, 10, 11, 38, 0.3, 50)
        top = max(phi[1:29])
        want = [
            k for k in range(11, 39) if phi[k - 10] >= phi[k - 11] and phi[k - 10] > phi[k - 9] and phi[k - 10] >= 0.3 * top
        ]
        if top <= 0:
            want = []
        assert sorted(round(c[0]) for c in got) == sorted(want)
        for lag, value in got:
            assert abs(lag - round(lag)) <= 0.5  # the vertex stays within half a lag
            assert value >= phi[round(lag) - 10] - 1e-12


def brute_force(local, trans):
    best = math.inf
    for path in itertools.product(*[range(len(c)) for c in local]):
        cost = local[0][path[0]] + sum(local[i][path[i]] + trans(i, path[i - 1], path[i]) for i in range(1, len(local)))
        best = min(best, cost)
    return best


def test_dp_matches_brute_force():
    rng = random.Random(3)
    for _ in range(30):
        frames = rng.randint(1, 5)
        local = [[rng.random() for _ in range(rng.randint(1, 4))] for _ in range(frames)]
        table = {}

        def trans(i, k, j):
            if (i, k, j) not in table:
                table[(i, k, j)] = rng.random()
            return table[(i, k, j)]

        path, total = dp(local, trans)
        assert abs(total - brute_force(local, trans)) < 1e-12
        again = local[0][path[0]] + sum(local[i][path[i]] + trans(i, path[i - 1], path[i]) for i in range(1, frames))
        assert abs(again - total) < 1e-12


def test_transition_costs():
    p = PARAMS
    assert transition_cost((40.0, 0.9), (40.0, 0.8), 1.0, 1.0) == 0.0
    assert abs(transition_cost((40.0, 0.9), (80.0, 0.8), 1.0, 1.0) - p["freq_wt"] * p["doubl_c"]) < 1e-15
    up = transition_cost((40.0, 0.9), (53.0, 0.8), 1.0, 1.0)
    assert abs(up - transition_cost((53.0, 0.9), (40.0, 0.8), 1.0, 1.0)) < 1e-15
    assert abs(up - p["freq_wt"] * math.log(53 / 40)) < 1e-15
    assert transition_cost((0.0, 0.0), (0.0, 0.0), 0.3, 0.4) == 0.0
    onset = transition_cost((0.0, 0.0), (40.0, 0.9), 4.0, 0.2)
    offset = transition_cost((40.0, 0.9), (0.0, 0.0), 0.25, 0.2)
    assert abs(onset - (0.005 + 0.5 * 0.2 + 0.5 / 4.0)) < 1e-15
    assert abs(offset - (0.005 + 0.5 * 0.2 + 0.5 * 0.25)) < 1e-15


def test_itakura_ratio_is_at_least_one():
    rng = random.Random(4)
    for _ in range(20):
        a = [rng.gauss(0, 1) for _ in range(120)]
        b = all_pole([rng.gauss(0, 1) for _ in range(120)], [rng.uniform(-0.6, 0.6)])
        assert itakura_ratio(a, b, 6) >= 1 - 1e-9
        assert abs(itakura_ratio(a, a, 6) - 1) < 1e-9


def test_example_of_the_page():
    frames = [[(40.0, 0.95), (80.0, 0.90)], [(40.0, 0.45), (120.0, 0.40)], [(40.0, 0.94), (80.0, 0.88)], [(97.0, 0.30)]]
    rr, s = [1.0, 1.0, 1.0, 0.1], [1.0, 1.0, 1.0, 0.2]
    cands = [f + [(0.0, 0.0)] for f in frames]
    local = [[1 - c * (1 - BETA * lag) for lag, c in f] + [max(c for _, c in f)] for f in frames]
    assert [round(v, 5) for v in local[1]] == [0.58375, 0.69, 0.45]  # alone, frame 2 looks unvoiced

    def trans(i, k, j):
        return transition_cost(cands[i - 1][k], cands[i][j], rr[i], s[i])

    path, total = dp(local, trans)
    assert path == [0, 0, 0, 1]
    assert abs(total - 1.2905) < 1e-12


def test_track_of_a_voiced_segment_then_noise():
    rng = random.Random(5)
    v = all_pole(pulse_train(160, FS, 1200), [1.662983, -0.81])
    peak = max(abs(t) for t in v)
    x = [t / peak for t in v] + white_noise(rng, 800, 0.02)
    track = rapt(x, FS)
    assert len(track) == 23
    assert all(f is not None and abs(f - 160) < 0.5 for f in track[:14])
    assert all(f is None for f in track[14:])
