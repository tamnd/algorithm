# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jakes-fading-simulator/. The authors are listed in prov/43NN0S.jsonl.

import math
import random

from jakes_fading_simulator import (
    aliasing_series,
    bessel_j,
    j0,
    jakes,
    jakes_coefficients,
    power_at_zero,
    quadrature_correlations,
    time_autocorrelation,
)

M = 8
FD = 1.0
STEP = 0.05
RECORD = 2000.0


def j0_series(x):
    """J0 by its power series, a second method for small x."""
    s, t, k = 0.0, 1.0, 0
    while abs(t) > 1e-18 or k < 5:
        s += t
        k += 1
        t *= -(x / 2.0) ** 2 / (k * k)
    return s


def record():
    times = [k * STEP for k in range(int(RECORD / STEP))]
    return jakes(M, FD, times)


def test_coefficients() -> None:
    n, nu, a, b = jakes_coefficients(M)
    assert n == 34
    assert len(nu) == len(a) == len(b) == M + 1
    assert abs(a[0] - 1.0) < 1e-12 and abs(b[0] - 1.0) < 1e-12
    # time-average powers of the two quadratures are equal: sum a^2 = sum b^2 = N / 2
    assert abs(sum(v * v for v in a) - n / 2) < 1e-12
    assert abs(sum(v * v for v in b) - n / 2) < 1e-12


def test_bessel_against_series() -> None:
    for x in (0.0, 0.5, 1.0, 2.404825557695773, 5.0, 10.0):
        assert abs(j0(x) - j0_series(x)) < 1e-10
    assert abs(j0(2 * math.pi * 0.38274)) < 1e-4  # the first zero of J0 at f_D tau = 0.38274


def test_mean_power() -> None:
    h = record()
    p = sum(abs(v) ** 2 for v in h) / len(h)
    assert abs(p - 1.0) < 0.02


def test_sample_autocorrelation_matches_closed_form() -> None:
    h = record()
    for lag in (2, 5, 8, 20, 40):  # f_D tau = 0.1, 0.25, 0.4, 1, 2
        r = sum(h[k + lag] * h[k].conjugate() for k in range(len(h) - lag)) / (len(h) - lag)
        x = 2 * math.pi * FD * lag * STEP
        assert abs(r - time_autocorrelation(M, x)) < 0.02
        assert abs(r - j0(x)) < 0.02


def test_closed_form_close_to_clarke_for_small_lags() -> None:
    for k in range(0, 301):
        x = 2 * math.pi * k * 0.01  # f_D tau up to 3
        assert abs(time_autocorrelation(M, x) - j0(x)) < 1e-3


def test_bias_at_large_lags() -> None:
    # f_D tau = 5 and 10: the autocorrelation departs from J0
    for ft, target in ((5.0, -0.00301), (10.0, -0.04948)):
        x = 2 * math.pi * ft
        r = time_autocorrelation(M, x)
        assert abs(r - target) < 1e-4
        assert abs(r - j0(x)) > 0.05
        assert abs(r - aliasing_series(M, x)) < 1e-9


def test_quadratures_are_not_clarke() -> None:
    x = 2 * math.pi * 0.38274  # J0 is zero here
    rcc, rss, rcs = quadrature_correlations(M, x)
    assert abs(rcc - 0.17328) < 1e-4
    assert abs(rcs - (-0.3462)) < 1e-4
    assert abs(rcc + rss - 2 * time_autocorrelation(M, x)) < 1e-12
    rcc0, rss0, rcs0 = quadrature_correlations(M, 0.0)
    assert abs(rcc0 - 1) < 1e-12 and abs(rss0 - 1) < 1e-12
    assert abs(rcs0 - 2 / 34) < 1e-12  # the quadratures are correlated at lag 0


def test_peak_at_time_zero() -> None:
    h0 = jakes(M, FD, [0.0])[0]
    expect = (2 / 34) * (1 + (1 + 2 / math.tan(math.pi / 16)) ** 2)
    assert abs(abs(h0) ** 2 - expect) < 1e-9
    assert abs(power_at_zero(M) - expect) < 1e-9
    assert 7.2 < expect < 7.3


def test_random_phases_give_unit_ensemble_power() -> None:
    rng = random.Random(4301)
    trials = 4000
    acc0 = 0.0
    acc1 = 0j
    x = 2 * math.pi * 0.25
    for _ in range(trials):
        ph = [rng.uniform(-math.pi, math.pi) for _ in range(M + 1)]
        a, b = jakes(M, FD, [0.0, 0.25], phases=ph)
        acc0 += abs(a) ** 2
        acc1 += b * a.conjugate()
    assert abs(acc0 / trials - 1.0) < 0.06
    assert abs(acc1 / trials - time_autocorrelation(M, x)) < 0.06


def test_bessel_order() -> None:
    # J1(1) = 0.44005058574493355
    assert abs(bessel_j(1, 1.0) - 0.44005058574493355) < 1e-12
