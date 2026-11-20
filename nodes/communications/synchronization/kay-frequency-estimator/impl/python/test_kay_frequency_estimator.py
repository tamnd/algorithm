# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kay-frequency-estimator/. The authors are listed in prov/9RD1BP.jsonl.

import cmath
import math
import random

from kay_frequency_estimator import crb, kay_estimate, kay_weights


def tone(rng, n, omega, snr=None, phi=0.0):
    sd = math.sqrt(0.5 / snr) if snr else 0.0
    return [cmath.exp(1j * (omega * t + phi)) + (complex(rng.gauss(0, sd), rng.gauss(0, sd)) if sd else 0j) for t in range(n)]


def blue_weights(n):
    """Reference: C^-1 1 / (1' C^-1 1) for the tridiagonal covariance (2, -1) of the phase differences."""
    m = n - 1
    a = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(m)] + [1.0] for i in range(m)]
    for c in range(m):  # Gaussian elimination, no pivoting needed: C is positive definite
        for i in range(c + 1, m):
            f = a[i][c] / a[c][c]
            for j in range(c, m + 1):
                a[i][j] -= f * a[c][j]
    x = [0.0] * m
    for i in range(m - 1, -1, -1):
        x[i] = (a[i][m] - sum(a[i][j] * x[j] for j in range(i + 1, m))) / a[i][i]
    s = sum(x)
    return [v / s for v in x]


def test_weights_are_the_blue_weights() -> None:
    for n in (2, 3, 5, 8, 17, 32, 64):
        w = kay_weights(n)
        assert abs(sum(w) - 1.0) < 1e-12
        assert max(abs(a - b) for a, b in zip(w, blue_weights(n))) < 1e-12
    # The high-SNR variance of the weighted sum, (N0/2) w' C w, is the CRB.
    for n in (4, 16, 32):
        w = kay_weights(n)
        q = sum(2 * x * x for x in w) - 2 * sum(w[i] * w[i + 1] for i in range(n - 2))
        snr = 10.0
        assert abs(q * 0.5 / snr - crb(n, snr)) < 1e-15
    assert abs(crb(32, 10.0) - 1.833e-5) < 1e-8


def test_exact_without_noise() -> None:
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randrange(2, 40)
        om = rng.uniform(-math.pi, math.pi) * 0.999
        assert abs(kay_estimate(tone(rng, n, om, phi=rng.uniform(-3, 3))) - om) < 1e-9


def test_reaches_the_crb_above_threshold() -> None:
    # N = 32, 500 trials (16000 samples per SNR). Measured MSE / CRB.
    n, trials = 32, 500
    ratio = {}
    for snr_db in (3, 10, 20):
        snr = 10 ** (snr_db / 10)
        rng = random.Random(1)
        se = 0.0
        for _ in range(trials):
            om = rng.uniform(-0.5, 0.5)
            e = kay_estimate(tone(rng, n, om, snr, rng.uniform(-3, 3))) - om
            se += e * e
        ratio[snr_db] = se / trials / crb(n, snr)
    assert 0.85 < ratio[10] < 1.3
    assert 0.85 < ratio[20] < 1.3
    assert ratio[3] > 10  # below the threshold: phase wraps of single differences dominate


def test_better_than_the_unweighted_mean() -> None:
    # Equal weights telescope to (arg-sum of differences)/(N-1): variance about N/6 times worse.
    n, trials, snr = 32, 400, 100.0
    rng = random.Random(2)
    se_k = se_u = 0.0
    for _ in range(trials):
        om = rng.uniform(-0.5, 0.5)
        r = tone(rng, n, om, snr)
        d = [cmath.phase(r[t + 1] * r[t].conjugate()) for t in range(n - 1)]
        se_k += (kay_estimate(r) - om) ** 2
        se_u += (sum(d) / (n - 1) - om) ** 2
    assert se_u > 3 * se_k
