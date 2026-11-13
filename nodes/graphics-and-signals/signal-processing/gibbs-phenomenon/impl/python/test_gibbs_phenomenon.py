# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gibbs-phenomenon/. The authors are listed in prov/NNCRSC.jsonl.

import math

from gibbs_phenomenon import (
    gibbs_fraction,
    lowpass_partial_response,
    peak_of_partial_sum,
    sine_integral,
    square_wave_fejer_mean,
    square_wave_partial_sum,
)


def simpson(g, a: float, b: float, n: int = 4000) -> float:
    h = (b - a) / n
    total = 0.0
    for j in range(n + 1):
        w = 1 if j in (0, n) else (4 if j % 2 else 2)
        total += w * g(a + j * h)
    return total * h / 3


def test_sine_integral_against_simpson() -> None:
    for x in (0.1, 1.0, 2.0, math.pi, 5.0):
        ref = simpson(lambda u: 1.0 if u == 0 else math.sin(u) / u, 0.0, x)
        assert abs(sine_integral(x) - ref) <= 1e-11


def test_gibbs_constant() -> None:
    assert abs(sine_integral(math.pi) - 1.8519370519824662) <= 1e-12
    assert abs(gibbs_fraction() - 0.0894898722) <= 1e-10


def test_first_peak_is_at_pi_over_2m_and_is_the_maximum() -> None:
    for m in (3, 5, 20, 50):
        t_star = math.pi / (2 * m)
        v_star = square_wave_partial_sum(t_star, m)
        _, best = peak_of_partial_sum(m, points=40 * m)
        assert best <= v_star + 1e-12
        assert v_star - best <= 1e-3


def test_overshoot_tends_to_8_95_percent_of_the_jump() -> None:
    # Jump 2, so the overshoot fraction is (S_m(pi/(2m)) - 1) / 2.
    measured = {}
    for m in (5, 50, 500):
        measured[m] = (square_wave_partial_sum(math.pi / (2 * m), m) - 1) / 2
    assert abs(measured[5] - 0.0911641) <= 1e-6
    assert abs(measured[50] - 0.0895065) <= 1e-6
    assert abs(measured[500] - 0.0894900) <= 1e-6
    g = gibbs_fraction()
    for m, frac in measured.items():
        assert 0 < frac - g <= 0.05 / m**2  # never below the limit: it does not go away


def test_mean_square_error_goes_to_zero_while_the_overshoot_stays() -> None:
    previous = math.inf
    for m in (5, 20, 80):
        # (1/pi) * integral over (0, pi) of (1 - S_m)^2, against Parseval's tail sum
        numeric = simpson(lambda t: (1 - square_wave_partial_sum(t, m)) ** 2, 0.0, math.pi, n=40 * m) / math.pi
        tail = 8 / math.pi**2 * sum(1 / (2 * j - 1) ** 2 for j in range(m + 1, 200000))
        assert abs(numeric - tail) <= 1e-5
        assert numeric < previous
        previous = numeric
        assert square_wave_partial_sum(math.pi / (2 * m), m) > 1.178


def test_fejer_means_do_not_overshoot() -> None:
    for m in (5, 50):
        worst = max(square_wave_fejer_mean(j * math.pi / (40 * m), m) for j in range(1, 40 * m))
        assert worst < 1
    assert abs(max(square_wave_fejer_mean(j * math.pi / 200, 5) for j in range(1, 200)) - 0.93573) <= 1e-4


def test_truncated_ideal_lowpass_overshoots_the_same_fraction() -> None:
    # The response jumps from 1 to 0 at the cutoff; the largest value is about 1 + 0.0895.
    cutoff = math.pi / 2
    n_max = 200
    peak = max(lowpass_partial_response(cutoff - j * 0.0005, cutoff, n_max) for j in range(1, 200))
    assert abs(peak - 1 - gibbs_fraction()) <= 2e-3
