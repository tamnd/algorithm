# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dk-iteration/. The authors are listed in prov/QSHHP3.jsonl.

import math
import random

import ctlmat as cm
from dk_iteration import (
    central_controller,
    closed_loop,
    d_step,
    dk_iteration,
    is_hurwitz,
    optimal_gamma,
    responses,
    scale_plant,
    scaled_peak,
)

# x' = x + w1 + w2 + u. The uncertainty block maps z1 = 0.5 x to w1. The
# performance block maps w2 (load) and w3 (sensor noise) to z2 = x and z3 = u.
PLANT = {"A": [[1]], "B1": [[1, 1, 0]], "B2": [[1]], "C1": [[0.5], [1], [0]],
         "C2": [[1]], "D12": [[0], [0], [1]], "D21": [[0, 0, 1]]}

# A two-state plant with the same block structure.
PLANT2 = {"A": [[0, 1], [2, -1]], "B1": [[0.3, 1, 0], [1, 0, 0]], "B2": [[0], [1]],
          "C1": [[2, 0], [1, 0], [0, 1], [0, 0]], "C2": [[1, 0]],
          "D12": [[0], [0], [0], [1]], "D21": [[0, 0, 1]]}

# A coarse grid keeps the test fast. For both plants the peak of the final
# loop is at w = 0, which the grid contains.
FREQS = [10 ** (e / 4) for e in range(-8, 9)] + [0.0]
BACKOFF = 1.02

_CACHE = {}


def run(p):
    if id(p) not in _CACHE:
        _CACHE[id(p)] = dk_iteration(p, 1, 1, FREQS, iters=3, backoff=BACKOFF)
    return _CACHE[id(p)]


def plain(p):
    # The H-infinity controller with no scaling, d = 1.
    key = ("plain", id(p))
    if key not in _CACHE:
        g = BACKOFF * optimal_gamma(p)
        _CACHE[key] = central_controller(p, g)
    return _CACHE[key]


def test_ctlmat_self_test():
    assert cm._self_test()


def test_scaled_plant_is_the_scaled_closed_loop():
    # A controller for the scaled plant gives the closed loop D M D^-1.
    rng = random.Random(5)
    k = plain(PLANT)
    for d in (0.3, 1.7, 4.0):
        ms = responses(closed_loop(PLANT, k), [0.0, 0.7, 3.0])
        ss = responses(closed_loop(scale_plant(PLANT, d, 1, 1), k), [0.0, 0.7, 3.0])
        for m, s in zip(ms, ss):
            for i in range(3):
                for j in range(3):
                    want = m[i][j] * (d if i == 0 else 1) / (d if j == 0 else 1)
                    assert abs(s[i][j] - want) < 1e-12 * (1 + abs(want))
        # The scaled plant keeps the normalized form.
        q = scale_plant(PLANT, d * rng.uniform(0.5, 2), 1, 1)
        assert cm.mul(cm.transpose(q["D12"]), q["C1"]) == [[0.0]]
        assert cm.mul(q["B1"], cm.transpose(q["D21"])) == [[0.0]]


def test_k_step_closed_form_at_the_best_scale():
    # With d = sqrt(2) both Riccati equations equal X^2 (5/6) - 2 X - 3/2 = 0
    # at gamma = 3, so X = Y = 3 and rho(XY) = gamma^2: gamma_opt = 3.
    g = optimal_gamma(scale_plant(PLANT, math.sqrt(2), 1, 1), 1e-9)
    assert abs(g - 3.0) < 1e-8
    # The plant is symmetric under d -> 2 / d.
    for d in (0.7, 1.0, 1.9):
        g1 = optimal_gamma(scale_plant(PLANT, d, 1, 1), 1e-9)
        g2 = optimal_gamma(scale_plant(PLANT, 2 / d, 1, 1), 1e-9)
        assert abs(g1 - g2) < 1e-7 * g1 and g1 > 3.0


def test_d_step_matches_a_brute_force_grid():
    for p in (PLANT, PLANT2):
        ms = responses(closed_loop(p, plain(p)), FREQS)
        d, v = d_step(ms, 1, 1)
        ts = [i / 5 for i in range(-15, 16)]
        vals = [scaled_peak(ms, math.exp(t), 1, 1) for t in ts]
        # Golden section is at least as good as every grid point, up to the tolerance.
        assert v <= min(vals) * (1 + 1e-9)
        assert abs(v - scaled_peak(ms, d, 1, 1)) < 1e-12
        # The sampled function is convex in log d (Sezginer and Overton).
        for i in range(1, len(vals) - 1):
            assert vals[i] <= 0.5 * (vals[i - 1] + vals[i + 1]) + 1e-12


def test_iteration_is_monotone_up_to_the_backoff():
    for p in (PLANT, PLANT2):
        _, _, hist = run(p)
        for (g0, v0, _), (g1, v1, _) in zip(hist, hist[1:]):
            # gamma_opt of the next K-step is at most the last scaled peak,
            # and the next peak exceeds gamma_opt by at most the backoff.
            assert g1 <= v0 * (1 + 1e-3)
            assert v1 <= BACKOFF * v0 * (1 + 1e-3)
        for g, v, _ in hist:
            assert g * (1 - 1e-3) <= v <= BACKOFF * g * (1 + 1e-3)


def test_result_is_stabilizing_and_beats_plain_h_infinity():
    for p in (PLANT, PLANT2):
        k, d, hist = run(p)
        cl = closed_loop(p, k)
        assert is_hurwitz(cl[0])
        best = scaled_peak(responses(cl, FREQS), d, 1, 1)
        unscaled = scaled_peak(responses(closed_loop(p, plain(p)), FREQS), 1.0, 1, 1)
        assert best <= unscaled
        assert abs(best - min(v for _, v, _ in hist)) < 1e-9 * best


def test_example_values():
    k, d, hist = run(PLANT)
    assert abs(d - math.sqrt(2)) < 1e-5
    assert abs(hist[0][0] - 3.0615528) < 1e-4
    assert abs(hist[-1][0] - 3.0) < 1e-4
    assert hist[-1][1] < BACKOFF * 3.0 * (1 + 1e-4)
