# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smith-predictor/. The authors are listed in prov/R7T7GR.jsonl.

import math
import random

from ctlsim import lti, simulate
from smith_predictor import PI, DelayedPlant, SmithPredictor, run_loop, zoh

# Example: P0 = 1/(s + 1), theta = 2 s, h = 0.1 s (20 samples of delay),
# PI with K = 2 and Ti = 1, so that C P0 = 2/s and T0 = 2/(s + 2).
H = 0.1
AD, BD = zoh([[-1.0]], [[1.0]], H)
D = 20


def smith(Am=AD, Bm=BD, dm=D, K=2.0, Ti=1.0, h=H):
    return SmithPredictor(Am, Bm, [1.0], dm, PI(K, Ti, h))


def settling(ys, h, r=1.0, band=0.02):
    for k in range(len(ys) - 1, -1, -1):
        if abs(ys[k] - r) > band * abs(r):
            return (k + 1) * h
    return 0.0


def test_zoh_matches_simulation():
    A = [[0.0, 1.0], [-2.0, -3.0]]
    B = [[0.0], [1.0]]
    Ad, Bd = zoh(A, B, 0.5)
    _, xs, _ = simulate(lti(A, B), [1.0, -1.0], 0.0, 0.5, 0.005, control=lambda t, x: 0.7, hold=0.5)
    want = [sum(a * v for a, v in zip(row, [1.0, -1.0])) + b[0] * 0.7 for row, b in zip(Ad, Bd)]
    assert max(abs(p - q) for p, q in zip(xs[-1], want)) < 1e-10
    ad, bd = zoh([[-1.0]], [[1.0]], H)
    assert abs(ad[0][0] - math.exp(-H)) < 1e-15 and abs(bd[0][0] - (1 - math.exp(-H))) < 1e-15


def test_exact_model_gives_shifted_delay_free_response():
    free, ufree = run_loop(DelayedPlant(AD, BD, [1.0], 0), PI(2.0, 1.0, H), 300)
    ys, us = run_loop(DelayedPlant(AD, BD, [1.0], D), smith(), 300 + D)
    assert ys[:D] == [0.0] * D
    assert ys[D:] == free          # exact, not only close
    assert us[:300] == ufree


def test_shift_holds_for_random_plants():
    rng = random.Random(21)
    for _ in range(5):
        p1, p2 = rng.uniform(0.2, 3.0), rng.uniform(0.2, 3.0)
        A = [[0.0, 1.0], [-p1 * p2, -(p1 + p2)]]
        B = [[0.0], [p1 * p2]]
        C = [1.0, 0.0]
        h, d = 0.05, rng.randint(1, 40)
        K, Ti, r = rng.uniform(0.2, 3.0), rng.uniform(0.5, 5.0), rng.uniform(-2.0, 2.0)
        Ad, Bd = zoh(A, B, h)
        free, _ = run_loop(DelayedPlant(Ad, Bd, C, 0), PI(K, Ti, h), 200, r=r)
        sp = SmithPredictor(Ad, Bd, C, d, PI(K, Ti, h))
        ys, _ = run_loop(DelayedPlant(Ad, Bd, C, d), sp, 200 + d, r=r)
        assert ys[d:] == free


def test_settling_time_grows_by_the_delay_only():
    free, _ = run_loop(DelayedPlant(AD, BD, [1.0], 0), PI(2.0, 1.0, H), 400)
    ys, _ = run_loop(DelayedPlant(AD, BD, [1.0], D), smith(), 400)
    assert abs(settling(ys, H) - settling(free, H) - D * H) < 1e-9
    # Measured: overshoot 0.0021, settling time 3.7 s.
    assert max(ys) - 1 < 0.003 and abs(settling(ys, H) - 3.7) < 1e-9


def test_same_pi_without_predictor_diverges():
    ys, _ = run_loop(DelayedPlant(AD, BD, [1.0], D), PI(2.0, 1.0, H), 200)
    assert max(abs(y) for y in ys) > 100


def test_load_response_integral():
    # Continuous value: the integral of y for a unit load step is
    # theta - T0'(0) = 2 + 1/2 = 2.5. Measured on the sampled loop: 2.5.
    ys, _ = run_loop(DelayedPlant(AD, BD, [1.0], D), smith(), 1000, r=0.0, w=lambda k: 1.0)
    assert min(ys) > -1e-12
    assert abs(sum(ys) * H - 2.5) < 1e-6
    assert abs(ys[-1]) < 1e-9
    # General PI value Ti/K + P0(0) theta, here with the plant gain 3: 6.5.
    A3, B3 = zoh([[-1.0]], [[3.0]], H)
    sp = SmithPredictor(A3, B3, [1.0], D, PI(2.0, 1.0, H))
    ys, _ = run_loop(DelayedPlant(A3, B3, [1.0], D), sp, 1500, r=0.0, w=lambda k: 1.0)
    assert abs(sum(ys) * H - 6.5) < 1e-6


def test_model_mismatch():
    # Integral action removes the steady-state error whenever the loop
    # converges. Measured: delay errors of 10 percent converge, a model
    # delay of 3 s for a plant delay of 2 s does not.
    cases = [(22, 1.0, 1.0), (18, 1.0, 1.0), (20, 1.2, 1.0), (20, 0.8, 1.0), (20, 1.0, 1.5)]
    for dm, g, T in cases:
        Am, Bm = zoh([[-1.0 / T]], [[g / T]], H)
        ys, _ = run_loop(DelayedPlant(AD, BD, [1.0], D), smith(Am, Bm, dm), 1500)
        assert abs(ys[-1] - 1) < 1e-6
    ys, _ = run_loop(DelayedPlant(AD, BD, [1.0], D), smith(dm=30), 1500)
    assert max(abs(y) for y in ys) > 100


def small_gain_bound(delta, w_max=200.0, grid=20000):
    # max over w of |T0(jw)| |e^(-j w delta) - 1| with T0 = 2/(s + 2).
    best = 0.0
    for i in range(1, grid + 1):
        w = w_max * i / grid
        best = max(best, 2 / abs(2 + 1j * w) * abs(complex(math.cos(w * delta), -math.sin(w * delta)) - 1))
    return best


def test_small_gain_bound_for_delay_errors():
    # Measured: 0.3573 for |delta| = 0.2 s and 1.1990 for |delta| = 1 s. The
    # bound reaches 1 at |delta| = 0.7387 s.
    assert small_gain_bound(0.2) < 0.5
    assert small_gain_bound(-0.2) < 0.5
    assert small_gain_bound(0.73) < 1 < small_gain_bound(0.75)
    assert small_gain_bound(1.0) > 1


def test_unstable_plant_is_not_internally_stable():
    # P0 = 1/(s - 1), theta = 0.5 s, h = 0.05 s. The set-point response
    # converges, but a load step makes y grow like e^t.
    h, d = 0.05, 10
    Au, Bu = zoh([[1.0]], [[1.0]], h)
    sp = lambda: SmithPredictor(Au, Bu, [1.0], d, PI(3.0, 1.0, h))
    ys, _ = run_loop(DelayedPlant(Au, Bu, [1.0], d), sp(), 400)
    assert abs(ys[-1] - 1) < 1e-6
    ys, _ = run_loop(DelayedPlant(Au, Bu, [1.0], d), sp(), 400, r=0.0, w=lambda k: 0.01)
    assert ys[-1] > 1e5
    assert abs(ys[-1] / ys[-21] - math.e) < 1e-6
