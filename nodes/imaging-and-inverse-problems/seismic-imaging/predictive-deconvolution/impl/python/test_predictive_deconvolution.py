# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/predictive-deconvolution/. The authors are listed in prov/R3R43H.jsonl.

import math
import random
from fractions import Fraction as F

import imgla as la
from predictive_deconvolution import (
    apply_filter,
    autocorrelation,
    levinson,
    prediction_error_filter,
    prediction_filter,
    predictive_deconvolution,
)


def toeplitz(r, n):
    return [[r[abs(i - j)] for j in range(n)] for i in range(n)]


def ar1_autocorrelation(n):
    """Exact autocorrelation of the infinite wavelet w_k = (1/2)^k: r_k = (4/3) (1/2)^k."""
    return [F(4, 3) * F(1, 2) ** k for k in range(n)]


def test_levinson_matches_dense_solve():
    rng = random.Random(1)
    for n in (1, 2, 5, 12):
        d = [rng.gauss(0.0, 1.0) for _ in range(60)]
        r = autocorrelation(d, n)
        g = [rng.gauss(0.0, 1.0) for _ in range(n)]
        x = levinson(r, g)
        y = la.solve(toeplitz(r, n), g)
        assert max(abs(a - b) for a, b in zip(x, y)) < 1e-9


def test_levinson_is_exact_with_fractions():
    rng = random.Random(2)
    d = [F(rng.randint(-5, 5)) for _ in range(20)]
    d[0] = F(7)
    r = autocorrelation(d, 6)
    g = [F(rng.randint(-9, 9)) for _ in range(6)]
    assert levinson(r, g) == la.solve(toeplitz(r, 6), g)


def test_spiking_filter_of_ar1_wavelet():
    r = ar1_autocorrelation(8)
    a = prediction_filter(r, 5, 1)
    assert a == [F(1, 2), 0, 0, 0, 0]
    f = prediction_error_filter(a, 1)
    w = [F(1, 2) ** k for k in range(30)]
    e = apply_filter(f, w)
    assert e == [1] + [0] * 29


def test_gapped_filter_keeps_the_first_alpha_samples():
    for gap in (2, 3, 5):
        r = ar1_autocorrelation(4 + gap + 1)
        a = prediction_filter(r, 4, gap)
        assert a == [F(1, 2) ** gap, 0, 0, 0]
        f = prediction_error_filter(a, gap)
        assert len(f) == gap + 4
        w = [F(1, 2) ** k for k in range(30)]
        e = apply_filter(f, w)
        assert e[:gap] == w[:gap]
        assert e[gap:] == [0] * (30 - gap)


def test_gap_equal_to_reverberation_period_removes_it():
    # d has (-c)^m at t = m tau: a spike under a water-layer reverberation.
    c, tau = F(1, 2), 6
    n = 8
    r = [F(0)] * (n + tau + 1)
    for k in range(len(r)):
        if k % tau == 0:
            r[k] = (-c) ** (k // tau) / (1 - c * c)
    a = prediction_filter(r, n, tau)
    assert a == [-c] + [0] * (n - 1)
    d = [(-c) ** (t // tau) if t % tau == 0 else F(0) for t in range(60)]
    e = apply_filter(prediction_error_filter(a, tau), d)
    assert e == [1] + [0] * 59


def test_prewhitening_adds_to_the_diagonal():
    rng = random.Random(3)
    d = [rng.gauss(0.0, 1.0) for _ in range(80)]
    n, gap, eps = 6, 2, 0.05
    r = autocorrelation(d, n + gap)
    a = prediction_filter(r, n, gap, eps)
    mat = toeplitz(r, n)
    for i in range(n):
        mat[i][i] += eps * r[0]
    b = la.solve(mat, [r[gap + i] for i in range(n)])
    assert max(abs(p - q) for p, q in zip(a, b)) < 1e-10


def test_filter_is_least_squares_prediction():
    # Perturbing the taps never lowers the prediction error energy on the design data.
    rng = random.Random(4)
    d = [rng.gauss(0.0, 1.0) for _ in range(150)]
    d = apply_filter([1.0, 0.9, 0.4], d)
    n, gap = 4, 2

    def energy(a):
        pad = [0.0] * len(d) + d + [0.0] * (n + gap)
        e = apply_filter(prediction_error_filter(a, gap), pad)
        return sum(v * v for v in e)

    r = autocorrelation(d, n + gap)
    a = prediction_filter(r, n, gap)
    base = energy(a)
    for _ in range(20):
        b = [v + rng.gauss(0.0, 0.05) for v in a]
        assert energy(b) >= base - 1e-9


def test_spiking_deconvolution_recovers_sparse_reflectivity():
    rng = random.Random(5)
    nt = 1500
    refl = [rng.gauss(0.0, 1.0) if rng.random() < 0.1 else 0.0 for _ in range(nt)]
    w = [0.8 ** k for k in range(60)]
    d = apply_filter(w, refl)
    e, f = predictive_deconvolution(d, 12, gap=1, prewhitening=0.001)
    assert abs(f[1] + 0.8) < 0.08
    num = sum(p * q for p, q in zip(e, refl))
    den = math.sqrt(sum(p * p for p in e) * sum(q * q for q in refl))
    assert num / den > 0.95


def test_spiking_filter_is_minimum_phase():
    # The inverse of the prediction error filter, run as a recursion, decays.
    rng = random.Random(6)
    d = apply_filter([1.0, -1.2, 0.6, 0.3], [rng.gauss(0.0, 1.0) for _ in range(400)])
    _, f = predictive_deconvolution(d, 10, gap=1, prewhitening=0.01)
    y = []
    for t in range(600):
        v = (1.0 if t == 0 else 0.0) - sum(f[k] * y[t - k] for k in range(1, min(len(f), t + 1)))
        y.append(v)
    assert max(abs(v) for v in y[500:]) < 1e-6
