# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whittle-likelihood/. The authors are listed in prov/F9TJBR.jsonl.

import cmath
import math
import random

import pytest

from whittle_likelihood import (
    arma_spectral_density,
    fft,
    pacf_to_ar,
    periodogram,
    whittle_fit_arma,
    whittle_neg2loglik,
)


def simulate_arma(phi, theta, n, rng, burn=300):
    e = [rng.gauss(0.0, 1.0) for _ in range(n + burn)]
    x = [0.0] * (n + burn)
    for t in range(n + burn):
        s = e[t] + sum(theta[j] * e[t - 1 - j] for j in range(len(theta)) if t - 1 - j >= 0)
        s += sum(phi[j] * x[t - 1 - j] for j in range(len(phi)) if t - 1 - j >= 0)
        x[t] = s
    return x[burn:]


def ar1_exact_neg2loglik(x, phi, sigma2):
    """Exact -2 log L of a zero-mean Gaussian AR(1) (the reference)."""
    n = len(x)
    s = (1 - phi * phi) * x[0] ** 2 + math.fsum((x[t] - phi * x[t - 1]) ** 2 for t in range(1, n))
    return n * math.log(2 * math.pi * sigma2) - math.log(1 - phi * phi) + s / sigma2


def ar1_exact_mle(x):
    """Exact Gaussian MLE of phi for a demeaned AR(1), by golden-section search."""
    n = len(x)
    m = math.fsum(x) / n
    d = [v - m for v in x]

    def obj(a):
        s = (1 - a * a) * d[0] ** 2 + math.fsum((d[t] - a * d[t - 1]) ** 2 for t in range(1, n))
        return n * math.log(s / n) - math.log(1 - a * a)

    lo, hi, gr = -0.9999, 0.9999, (math.sqrt(5) - 1) / 2
    for _ in range(80):
        c, e = hi - gr * (hi - lo), lo + gr * (hi - lo)
        if obj(c) < obj(e):
            hi = e
        else:
            lo = c
    return (lo + hi) / 2


def test_fft_matches_direct_dft():
    rng = random.Random(1)
    for n in list(range(1, 41)) + [64, 96, 128]:
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        direct = [sum(x[t] * cmath.exp(-2j * math.pi * t * k / n) for t in range(n)) for k in range(n)]
        assert max(abs(a - b) for a, b in zip(fft(x), direct)) < 1e-9 * n


def test_periodogram_parseval_and_symmetry():
    rng = random.Random(2)
    x = [rng.gauss(0, 1) for _ in range(50)]
    per = periodogram(x)
    assert math.fsum(per) == pytest.approx(math.fsum(v * v for v in x) / (2 * math.pi), rel=1e-12)
    assert all(per[j] == pytest.approx(per[50 - j], rel=1e-9, abs=1e-12) for j in range(1, 50))


def test_whittle_is_exact_for_white_noise():
    rng = random.Random(3)
    for n in (1, 7, 32, 45):
        x = [rng.gauss(0, 2) for _ in range(n)]
        s2 = 1.7
        exact = n * math.log(2 * math.pi * s2) + math.fsum(v * v for v in x) / s2
        assert whittle_neg2loglik(x, lambda lam: s2 / (2 * math.pi)) == pytest.approx(exact, rel=1e-12)


def test_spectral_density_integrates_to_the_autocovariance():
    phi, n = 0.6, 256
    for h in range(5):
        riemann = 2 * math.pi / n * math.fsum(
            arma_spectral_density([phi], [], 1.0, 2 * math.pi * j / n) * math.cos(h * 2 * math.pi * j / n)
            for j in range(n))
        assert riemann == pytest.approx(phi ** h / (1 - phi * phi), abs=1e-12)


def test_kolmogorov_formula_on_the_grid():
    # For a causal invertible ARMA, each factor (1 - a z) with |a| < 1 of phi or theta gives
    # prod_j (1 - a exp(-i omega_j)) = 1 - a^n, so the average of log(2 pi f / sigma^2) over the
    # n Fourier frequencies is a sum of terms (2 / n) log|1 - a^n|, which is tiny.
    for phi, theta in (([0.5], [0.4]), ([0.9], []), ([1.0, -0.5], [-0.3])):
        n = 512
        avg = math.fsum(math.log(2 * math.pi * arma_spectral_density(phi, theta, 1.0, 2 * math.pi * j / n))
                        for j in range(n)) / n
        assert abs(avg) < 1e-12


def test_pacf_to_ar_round_trip():
    rng = random.Random(4)
    for _ in range(50):
        p = rng.randint(1, 5)
        r = [rng.uniform(-0.95, 0.95) for _ in range(p)]
        a = pacf_to_ar(r)
        # step down: recover the partial autocorrelations
        back = []
        cur = a[:]
        for k in range(p, 0, -1):
            rk = cur[k - 1]
            back.append(rk)
            cur = [(cur[j] + rk * cur[k - 2 - j]) / (1 - rk * rk) for j in range(k - 1)]
        assert back[::-1] == pytest.approx(r, abs=1e-9)


def test_whittle_close_to_exact_likelihood_at_true_parameters():
    # Measured: the gap is O(1) while both values grow like n.
    rng = random.Random(5)
    for n in (128, 512):
        x = simulate_arma([0.6], [], n, rng)
        exact = ar1_exact_neg2loglik(x, 0.6, 1.0)
        wh = whittle_neg2loglik(x, lambda lam: arma_spectral_density([0.6], [], 1.0, lam))
        assert abs(wh - exact) / n < 0.02


def test_whittle_estimate_agrees_with_exact_mle():
    # Measured: r = 15 series of n = 256 from AR(1) with phi = 0.6, seed 6.
    rng = random.Random(6)
    diffs = []
    for _ in range(15):
        x = simulate_arma([0.6], [], 256, rng)
        phi_w = whittle_fit_arma(x, 1, 0)[0][0]
        diffs.append(abs(phi_w - ar1_exact_mle(x)))
    assert sum(diffs) / len(diffs) < 0.02


def test_arma11_fit_is_causal_invertible_and_near_truth():
    rng = random.Random(7)
    x = simulate_arma([0.5], [0.4], 1024, rng)
    phi, theta, s2 = whittle_fit_arma(x, 1, 1)
    assert abs(phi[0]) < 1 and abs(theta[0]) < 1
    # Asymptotic standard deviations are about 0.04 here; allow 4 of them.
    assert abs(phi[0] - 0.5) < 0.16 and abs(theta[0] - 0.4) < 0.16
    assert abs(s2 - 1.0) < 0.15
