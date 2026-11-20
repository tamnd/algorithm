# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/energy-detector/. The authors are listed in prov/T2T7RR.jsonl.

import cmath
import math
import random

import pytest

from cbb import cn, undb, wilson
from energy_detector import (
    clt_samples,
    energy_detect,
    gamma_tail,
    pd_deterministic,
    pd_gaussian,
    snr_wall,
    statistic,
    threshold,
)


def simpson(f, a: float, b: float, steps: int = 4000) -> float:
    h = (b - a) / steps
    s = f(a) + f(b)
    for i in range(1, steps):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def test_gamma_tail_small_cases() -> None:
    for x in (0.1, 1.0, 5.0, 30.0):
        assert gamma_tail(1, x) == pytest.approx(math.exp(-x), rel=1e-12)
        assert gamma_tail(2, x) == pytest.approx(math.exp(-x) * (1 + x), rel=1e-12)
    assert gamma_tail(4, 0.0) == 1.0
    # against the integral of the Gamma(5, 1) density x^4 e^(-x) / 24 from 7 to 80
    tail = simpson(lambda t: t ** 4 * math.exp(-t) / 24, 7.0, 80.0)
    assert gamma_tail(5, 7.0) == pytest.approx(tail, rel=1e-9)


def test_threshold() -> None:
    for n in (1, 4, 16, 200, 5000):
        for pfa in (0.5, 0.1, 0.01, 1e-4):
            lam = threshold(n, pfa)
            assert gamma_tail(n, lam) == pytest.approx(pfa, rel=1e-9)
    assert threshold(1, 0.05) == pytest.approx(-math.log(0.05), rel=1e-12)
    assert threshold(16, 0.05) == pytest.approx(23.0971, abs=1e-4)
    with pytest.raises(ValueError):
        threshold(4, 0.0)


def test_statistic_and_decision() -> None:
    y = [1 + 1j, 2 + 0j, 0 - 1j]
    assert statistic(y, 2.0) == pytest.approx((2 + 4 + 1) / 2)
    present, t, lam = energy_detect(y, 2.0, 0.05)
    assert t == pytest.approx(3.5)
    assert present == (t > lam)


def test_false_alarm_rate() -> None:
    rng = random.Random(1967)
    n, pfa, trials = 16, 0.05, 20000
    lam = threshold(n, pfa)
    hits = sum(statistic([cn(rng, 2.0) for _ in range(n)], 2.0) > lam for _ in range(trials))
    lo, hi = wilson(hits, trials)
    assert lo <= pfa <= hi


def test_detection_gaussian_signal() -> None:
    rng = random.Random(8)
    n, trials = 16, 4000
    lam = threshold(n, 0.05)
    snr = undb(0.0)
    p = pd_gaussian(n, snr, lam)
    assert p == pytest.approx(0.8752, abs=1e-4)
    hits = sum(statistic([cn(rng, snr) + cn(rng, 1.0) for _ in range(n)], 1.0) > lam for _ in range(trials))
    lo, hi = wilson(hits, trials)
    assert lo <= p <= hi


def test_detection_fixed_signal() -> None:
    rng = random.Random(9)
    n, trials = 16, 4000
    lam = threshold(n, 0.05)
    snr = undb(0.0)
    p = pd_deterministic(n, n * snr, lam)
    assert p == pytest.approx(0.9104, abs=1e-4)
    hits = 0
    for _ in range(trials):
        # QPSK symbols of power snr: the energy is fixed, the phases are random
        s = [math.sqrt(snr) * cmath.exp(1j * math.pi / 4 * (2 * rng.randrange(4) + 1)) for _ in range(n)]
        hits += statistic([v + cn(rng, 1.0) for v in s], 1.0) > lam
    lo, hi = wilson(hits, trials)
    assert lo <= p <= hi


def test_noncentral_mixture() -> None:
    lam = threshold(8, 0.1)
    assert pd_deterministic(8, 0.0, lam) == pytest.approx(0.1, rel=1e-9)
    prev = 0.1
    for mu in (0.5, 2.0, 8.0, 32.0):
        p = pd_deterministic(8, mu, lam)
        assert p > prev
        prev = p
    # one sample: 2T is noncentral chi-square with 2 degrees of freedom; check by integrating its density
    mu, x = 3.0, 4.0
    dens = lambda t: math.exp(-t - mu) * sum((mu * t) ** j / math.factorial(j) ** 2 for j in range(60))
    assert pd_deterministic(1, mu, x) == pytest.approx(simpson(dens, x, 60.0, 6000), rel=1e-8)


def test_sample_counts() -> None:
    table = {-5: 89, -10: 725, -15: 6779, -20: 66354}
    for snr_db, n_page in table.items():
        snr = undb(snr_db)
        n = math.ceil(clt_samples(snr, 0.1, 0.9))
        assert n == n_page
        lam = threshold(n, 0.1)
        assert pd_gaussian(n, snr, lam) == pytest.approx(0.9, abs=0.005)


def test_snr_wall() -> None:
    walls = {0.1: -13.367, 0.5: -6.368, 1.0: -3.329, 2.0: -0.205}
    for x, w in walls.items():
        assert 10 * math.log10(snr_wall(x)) == pytest.approx(w, abs=1e-3)
    # threshold set for the worst noise rho s2; the true noise is s2 / rho; Gaussian signal of power snr s2
    rho = undb(1.0)
    n = 100000
    lam = threshold(n, 0.1)
    below, above = undb(-4.0), undb(-2.5)
    assert gamma_tail(n, lam * rho / (1 / rho + below)) < 1e-6
    assert gamma_tail(n, lam * rho / (1 / rho + above)) > 0.999999
