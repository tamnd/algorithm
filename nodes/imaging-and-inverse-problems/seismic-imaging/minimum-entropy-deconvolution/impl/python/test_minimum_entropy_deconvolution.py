# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-entropy-deconvolution/. The authors are listed in prov/FDWZTR.jsonl.

import math
import random

from minimum_entropy_deconvolution import (
    autocorrelation_matrix,
    convolve_full,
    cross_term,
    gradient,
    med,
    total_varimax,
    varimax,
)


def sparse(rng, n, p=0.05):
    return [rng.gauss(0.0, 1.0) if rng.random() < p else 0.0 for _ in range(n)]


def best_match(y, r, shifts=range(-20, 40)):
    """The largest normalized cross-correlation of y with r over the shifts (sign ignored)."""
    den = math.sqrt(sum(v * v for v in y) * sum(v * v for v in r))
    best = 0.0
    for s in shifts:
        num = sum(y[t + s] * r[t] for t in range(len(r)) if 0 <= t + s < len(y))
        best = max(best, abs(num) / den)
    return best


def test_varimax_bounds_and_extremes():
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randint(1, 40)
        y = [rng.gauss(0.0, 1.0) for _ in range(n)]
        v = varimax(y)
        assert 1.0 / n - 1e-12 <= v <= 1.0 + 1e-12
    assert varimax([0.0, 0.0, -2.5, 0.0]) == 1.0
    assert abs(varimax([0.7] * 25) - 1.0 / 25) < 1e-15
    assert varimax([0.0] * 5) == 0.0


def test_varimax_is_scale_invariant():
    rng = random.Random(2)
    x = [rng.gauss(0.0, 1.0) for _ in range(50)]
    f = [rng.gauss(0.0, 1.0) for _ in range(6)]
    a = total_varimax(f, [x])
    b = total_varimax([-4.0 * v for v in f], [x])
    assert abs(a - b) < 1e-12


def test_autocorrelation_matrix_matches_the_definition():
    rng = random.Random(3)
    x = [rng.gauss(0.0, 1.0) for _ in range(20)]
    length = 5
    r = autocorrelation_matrix(x, length)
    for k in range(length):
        for j in range(length):
            direct = sum(x[t - j] * x[t - k] for t in range(len(x) + length)
                         if 0 <= t - j < len(x) and 0 <= t - k < len(x))
            assert abs(r[k][j] - direct) < 1e-12


def test_gradient_matches_finite_differences():
    rng = random.Random(4)
    traces = [[rng.gauss(0.0, 1.0) for _ in range(40)] for _ in range(2)]
    f = [rng.gauss(0.0, 1.0) for _ in range(5)]
    g = gradient(f, traces)
    h = 1e-6
    for k in range(len(f)):
        fp = list(f)
        fm = list(f)
        fp[k] += h
        fm[k] -= h
        fd = (total_varimax(fp, traces) - total_varimax(fm, traces)) / (2 * h)
        assert abs(fd - g[k]) < 1e-6 * max(1.0, abs(g[k]))


def test_fixed_point_is_a_stationary_point():
    rng = random.Random(5)
    refl = sparse(rng, 300)
    x = convolve_full([1.0, -0.6, 0.2], refl)
    f, hist = med([x], 15, iters=60)
    g = gradient(f, [x])
    assert max(abs(v) for v in g) < 1e-8
    assert hist[-1] > hist[0]


def test_recovers_a_mixed_phase_wavelet():
    # The wavelet (0.3, -0.8, 1.0, -0.4) is not minimum phase; MED needs no phase assumption.
    rng = random.Random(6)
    refl = sparse(rng, 300)
    x = convolve_full([0.3, -0.8, 1.0, -0.4], refl)
    f, _ = med([x], 15, iters=40)
    y = convolve_full(f, x)
    assert varimax(y) > 2.0 * varimax(x)
    assert best_match(y, refl) > 0.95


def test_one_filter_for_several_traces():
    rng = random.Random(7)
    w = [0.4, 1.0, -0.5]
    refls = [sparse(rng, 200) for _ in range(3)]
    traces = [convolve_full(w, r) for r in refls]
    f, hist = med(traces, 13, iters=40)
    for x, r in zip(traces, refls):
        assert best_match(convolve_full(f, x), r) > 0.95
    assert hist[-1] > hist[0]


def test_cross_term_definition():
    rng = random.Random(8)
    x = [rng.gauss(0.0, 1.0) for _ in range(15)]
    f = [rng.gauss(0.0, 1.0) for _ in range(4)]
    y = convolve_full(f, x)
    b = cross_term(y, x, 4)
    for k in range(4):
        direct = sum(y[t] ** 3 * x[t - k] for t in range(len(y)) if 0 <= t - k < len(x))
        assert abs(b[k] - direct) < 1e-12
