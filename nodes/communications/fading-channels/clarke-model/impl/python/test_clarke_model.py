# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clarke-model/. The authors are listed in prov/2J0WV7.jsonl.

import cmath
import math
import random

from clarke_model import (
    bessel_j0,
    clarke_correlation,
    doppler_spectrum,
    max_doppler,
    rms_doppler_spread,
)


def j0_series(x: float) -> float:
    """The power series sum_k (-x^2/4)^k / (k!)^2, accurate for |x| <= 20."""
    s, t, k = 0.0, 1.0, 0
    while k < 120:
        s += t
        k += 1
        t *= -(x * x / 4) / (k * k)
    return s


def bisect(f, a: float, b: float) -> float:
    for _ in range(80):
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


def test_against_series() -> None:
    for i in range(0, 401):
        x = i * 0.05
        # The series loses digits to cancellation as x grows; the midpoint rule does not.
        assert abs(bessel_j0(x) - j0_series(x)) < (1e-12 if x <= 10 else 1e-9)
        assert bessel_j0(-x) == bessel_j0(x)
    assert abs(bessel_j0(1.0) - 0.7651976865579666) < 1e-14


def test_zeros_and_large_arguments() -> None:
    for z in (2.404825557695773, 5.520078110286311, 8.653727912911013, 30.634606468431976):
        assert abs(bessel_j0(z)) < 1e-13
    # Asymptotic form sqrt(2/(pi x)) cos(x - pi/4) at a large argument.
    x = 1000.0
    assert abs(bessel_j0(x) - math.sqrt(2 / (math.pi * x)) * math.cos(x - math.pi / 4)) < 1e-5


def test_check_values() -> None:
    corr = lambda u: clarke_correlation(u, 1.0)
    assert abs(bisect(corr, 0.3, 0.45) - 0.38274) < 5e-6
    assert abs(bisect(lambda u: corr(u) - 0.5, 0.1, 0.3) - 0.2421) < 5e-5
    assert abs(bisect(lambda u: corr(u) - 0.9, 0.05, 0.2) - 0.1020) < 5e-5
    assert abs(bisect(lambda u: corr(u) ** 2 - 0.5, 0.1, 0.25) - 0.1793) < 5e-5
    # Coherence time rules: 0.423/f_D is past the first zero.
    assert abs(corr(0.423) - (-0.1235)) < 5e-4
    assert abs(bessel_j0(math.pi) - (-0.3042)) < 5e-5
    # The worked example: 30 m/s at 900 MHz, tau = 1 ms.
    fd = max_doppler(30.0, 900e6)
    assert abs(fd - 90.062) < 1e-3
    assert abs(clarke_correlation(1e-3, fd) - 0.9215) < 5e-5
    assert abs(clarke_correlation(1e-3, fd, 2.0) - 2 * clarke_correlation(1e-3, fd)) < 1e-15
    # Fleury's bound with sigma_nu = f_D / sqrt(2).
    for i in range(1, 100):
        u = i / 100 / (2 * math.sqrt(2))
        assert abs(corr(u)) >= math.cos(math.sqrt(2) * math.pi * u) - 1e-12


def test_spectrum_integrals() -> None:
    fd, omega = 50.0, 3.0
    n = 4000
    us = [-math.pi / 2 + math.pi * (k + 0.5) / n for k in range(n)]
    du = math.pi / n
    # f = f_D sin u removes the singularities at the band edges.
    w = [doppler_spectrum(fd * math.sin(u), fd, omega) * fd * math.cos(u) * du for u in us]
    fs = [fd * math.sin(u) for u in us]
    assert abs(sum(w) - omega) < 1e-9
    assert abs(sum(wi * f for wi, f in zip(w, fs))) < 1e-9
    var = sum(wi * f * f for wi, f in zip(w, fs)) / omega
    assert abs(math.sqrt(var) - rms_doppler_spread(fd)) < 1e-9
    for tau in (0.0, 0.001, 0.004, 0.01, 0.03):
        r = sum(wi * math.cos(2 * math.pi * f * tau) for wi, f in zip(w, fs))
        assert abs(r - omega * j0_series(2 * math.pi * fd * tau)) < 1e-9
    # Power within |f| < f_D / 2 is (2/pi) arcsin(1/2) = 1/3 of the total.
    m = 20000
    inner = sum(doppler_spectrum(-fd / 2 + fd * (k + 0.5) / m, fd) for k in range(m)) * fd / m
    assert abs(inner - 1 / 3) < 1e-6
    assert doppler_spectrum(fd, fd) == 0.0 and doppler_spectrum(-2 * fd, fd) == 0.0


def test_monte_carlo_sum_of_paths() -> None:
    # Random angles and phases, M paths of power omega/M each: the mean of
    # h(tau) h*(0) over draws estimates omega J0(2 pi f_D tau).
    rng = random.Random(2024)
    fd, omega, m, draws = 100.0, 1.0, 8, 4000
    taus = (0.0, 0.001, 0.0024, 0.005)
    acc = [0j] * len(taus)
    power = 0.0
    for _ in range(draws):
        th = [rng.uniform(0, 2 * math.pi) for _ in range(m)]
        ph = [rng.uniform(0, 2 * math.pi) for _ in range(m)]
        amp = math.sqrt(omega / m)
        h0 = sum(amp * cmath.exp(1j * p) for p in ph)
        power += abs(h0) ** 2
        for i, tau in enumerate(taus):
            ht = sum(amp * cmath.exp(1j * (2 * math.pi * fd * math.cos(t) * tau + p)) for t, p in zip(th, ph))
            acc[i] += ht * h0.conjugate()
    assert abs(power / draws - omega) < 0.08
    for a, tau in zip(acc, taus):
        assert abs(a / draws - clarke_correlation(tau, fd, omega)) < 0.08


def test_bad_input() -> None:
    try:
        doppler_spectrum(0.0, 0.0)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
