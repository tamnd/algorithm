# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-interference-cancellation-equalizer/. The authors are listed in prov/G8QTJ4.jsonl.

import itertools
import math
import random

import pytest

import cbb
from soft_interference_cancellation_equalizer import siso_equalize, soft_symbols, window_matrix

PROAKIS_B = [0.407, 0.815, 0.407]


def received(rng, x, h, sigma):
    return [v.real + rng.gauss(0.0, sigma) for v in cbb.conv(x, h)]


def test_no_priors_give_the_mmse_linear_equalizer():
    rng = random.Random(3)
    h, s2, n1, n2, k = [1.0, 0.5], 0.2, 2, 2, 12
    x = [rng.choice((-1, 1)) for _ in range(k)]
    y = received(rng, x, h, math.sqrt(s2))
    le = siso_equalize(y, h, [0.0] * k, s2, n1, n2)
    w = n1 + n2 + 1
    hm = window_matrix(h, w)
    s = [row[n2 + len(h) - 1] for row in hm]
    r = [[sum(a * b for a, b in zip(hm[i], hm[q])) + (s2 if i == q else 0.0) for q in range(w)] for i in range(w)]
    f = [v.real for v in cbb.solve(r, s)]
    mu = sum(a * b for a, b in zip(f, s))
    for n in range(n2 + len(h) - 1, k - n1):
        z = sum(f[i] * y[n - n2 + i] for i in range(w))
        assert abs(le[n] - 2 * z / (1 - mu)) < 1e-9


def test_perfect_priors_give_the_matched_filter_after_cancellation():
    rng = random.Random(4)
    h, s2, n1, n2, k = PROAKIS_B, 0.3, 3, 2, 10
    x = [rng.choice((-1, 1)) for _ in range(k)]
    y = received(rng, x, h, math.sqrt(s2))
    le = siso_equalize(y, h, [50.0 * v for v in x], s2, n1, n2)
    for n in range(k):
        clean = cbb.conv([v if t != n else 0 for t, v in enumerate(x)], h)
        mf = sum(h[l] * (y[n + l] - clean[n + l].real) for l in range(len(h)))
        assert abs(le[n] - 2 * mf / s2) < 1e-9


def test_lmmse_by_enumeration_and_the_gaussian_moments():
    h, s2, n1, n2 = [0.9, -0.5], 0.4, 1, 1
    la = [0.7, -1.3, 2.1, 0.4, -0.2]
    y = [0.3, -1.1, 0.8, 0.5, -0.4, 0.2]
    n = 2
    le = siso_equalize(y, h, la, s2, n1, n2)
    xbar, _ = soft_symbols(la)
    rows = range(n - n2, n + n1 + 1)
    p1 = [(1 + m) / 2 for m in xbar]
    p1[n] = 0.5
    my = [0.0] * len(rows)
    cyy = [[0.0] * len(rows) for _ in rows]
    cxy = [0.0] * len(rows)
    for xs in itertools.product((1, -1), repeat=len(la)):
        p = math.prod(p1[t] if xs[t] == 1 else 1 - p1[t] for t in range(len(la)))
        clean = [v.real for v in cbb.conv(list(xs), h)]
        vals = [clean[m] for m in rows]
        for i, a in enumerate(vals):
            my[i] += p * a
            cxy[i] += p * xs[n] * a
            for q, b in enumerate(vals):
                cyy[i][q] += p * a * b
    cyy = [[cyy[i][q] - my[i] * my[q] + (s2 if i == q else 0.0) for q in range(len(rows))] for i in range(len(rows))]
    g = [v.real for v in cbb.solve(cyy, cxy)]
    xhat = sum(gi * (y[m] - mi) for gi, m, mi in zip(g, rows, my))
    mu = sum(gi * ci for gi, ci in zip(g, cxy))
    assert abs(le[n] - 2 * xhat / (1 - mu)) < 1e-9
    for sign in (1, -1):
        mean = 0.0
        second = 0.0
        for xs in itertools.product((1, -1), repeat=len(la)):
            if xs[n] != sign:
                continue
            p = 2 * math.prod(p1[t] if xs[t] == 1 else 1 - p1[t] for t in range(len(la)))
            clean = [v.real for v in cbb.conv(list(xs), h)]
            z = sum(gi * (clean[m] - mi) for gi, m, mi in zip(g, rows, my))
            mean += p * z
            second += p * z * z
        var = second - mean * mean + s2 * sum(gi * gi for gi in g)
        assert abs(mean - sign * mu) < 1e-9
        assert abs(var - (mu - mu * mu)) < 1e-9


def test_extrinsic_output_ignores_its_own_prior():
    rng = random.Random(5)
    h, s2, k = PROAKIS_B, 0.25, 9
    la = [rng.uniform(-3, 3) for _ in range(k)]
    y = [rng.gauss(0, 1) for _ in range(k + len(h) - 1)]
    base = siso_equalize(y, h, la, s2, 3, 3)
    for n in range(k):
        changed = list(la)
        changed[n] = -changed[n] + 4.0
        assert abs(siso_equalize(y, h, changed, s2, 3, 3)[n] - base[n]) < 1e-9


def test_approximate_form_is_exact_when_all_variances_are_equal():
    rng = random.Random(6)
    h, s2, n1, n2, k = PROAKIS_B, 0.25, 3, 3, 14
    la = [rng.choice((-1.5, 1.5)) for _ in range(k)]
    y = [rng.gauss(0, 1) for _ in range(k + len(h) - 1)]
    exact = siso_equalize(y, h, la, s2, n1, n2)
    approx = siso_equalize(y, h, la, s2, n1, n2, approx=True)
    for n in range(n2 + len(h) - 1, k - n1):
        assert abs(exact[n] - approx[n]) < 1e-9


def test_bit_error_rate_with_perfect_priors_matches_the_matched_filter_bound():
    rng = random.Random(1)
    k, sigma = 10000, 0.5
    x = [rng.choice((-1, 1)) for _ in range(k)]
    y = received(rng, x, PROAKIS_B, sigma)
    le = siso_equalize(y, PROAKIS_B, [50.0 * v for v in x], sigma * sigma, 2, 2, approx=True)
    errors = sum((l < 0) != (v < 0) for l, v in zip(le, x))
    p = cbb.qfunc(math.sqrt(sum(v * v for v in PROAKIS_B)) / sigma)
    assert k * p >= 100
    lo, hi = cbb.wilson(errors, k)
    assert lo <= p <= hi


def test_bad_input():
    with pytest.raises(ValueError):
        siso_equalize([0.0] * 4, [1.0, 0.5], [0.0] * 3, 0.0, 1, 1)
    with pytest.raises(ValueError):
        siso_equalize([0.0] * 4, [1.0, 0.5], [0.0] * 3, 0.1, 0, 1)
    with pytest.raises(ValueError):
        siso_equalize([0.0] * 3, [1.0, 0.5], [0.0] * 3, 0.1, 1, 1)
