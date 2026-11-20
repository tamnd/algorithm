# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mmse-multiuser-detector/. The authors are listed in prov/1NBA15.jsonl.

import math
import random

import pytest

import cbb
import constel
from mmse_multiuser_detector import (
    crosscorrelation,
    linear_ber,
    matched_filter,
    mmse_detector,
    mmse_rows,
    mmse_sinr,
    output_sinr,
)

R8 = 1.0 / math.sqrt(8.0)
# The signatures of the page: s1 s2 = 0.5, s1 s3 = 0.25, s2 s3 = -0.25.
S_PAGE = [
    [R8 * c for c in (1, 1, 1, 1, 1, 1, 1, 1)],
    [R8 * c for c in (1, 1, 1, 1, 1, 1, -1, -1)],
    [R8 * c for c in (1, -1, 1, -1, 1, -1, 1, 1)],
]
AMPS = [1.0, 4.0, 2.0]


def chips(sigs, amps, b, sigma=0.0, rng=None):
    n = len(sigs[0])
    y = [math.fsum(amps[k] * b[k] * sigs[k][c] for k in range(len(sigs))) for c in range(n)]
    if rng is not None:
        y = [v + rng.gauss(0.0, sigma) for v in y]
    return y


def random_sigs(rng, k, n):
    s = 1.0 / math.sqrt(n)
    return [[s * rng.choice((1, -1)) for _ in range(n)] for _ in range(k)]


def test_page_example() -> None:
    b = [1, -1, 1]
    y = chips(S_PAGE, AMPS, b)
    assert [round(v, 12) for v in matched_filter(y, S_PAGE)] == [-0.5, -4.0, 3.25]
    assert mmse_detector(y, S_PAGE, AMPS, 0.5) == b
    m = mmse_rows(crosscorrelation(S_PAGE), AMPS, 0.5)
    assert [round(v, 4) for v in m[0]] == [1.1563, -0.6754, -0.431]


def test_small_noise_gives_the_decorrelator() -> None:
    r = crosscorrelation(S_PAGE)
    rinv = [[v.real for v in row] for row in cbb.inv(r)]
    m = mmse_rows(r, AMPS, 1e-5)
    for i in range(3):
        for j in range(3):
            assert m[i][j] == pytest.approx(rinv[i][j], abs=1e-8)


def test_large_noise_gives_matched_filter_decisions() -> None:
    rng = random.Random(4302)
    for _ in range(200):
        k = rng.randint(1, 5)
        sigs = random_sigs(rng, k, 8)
        amps = [rng.uniform(0.5, 2.0) for _ in range(k)]
        y = [rng.gauss(0.0, 1.0) for _ in range(8)]
        z = matched_filter(y, sigs)
        if min(abs(v) for v in z) < 1e-3:
            continue
        assert mmse_detector(y, sigs, amps, 1e4) == [1 if v >= 0 else -1 for v in z]


def test_works_when_correlation_is_singular() -> None:
    # Two users share one signature; R is singular but R + sigma^2 A^-2 is not.
    s = [R8] * 8
    y = chips([s, list(s)], [2.0, 1.0], [1, -1])
    assert mmse_detector(y, [s, list(s)], [2.0, 1.0], 0.3) == [1, 1]
    with pytest.raises(ValueError):
        mmse_detector(y, [s, list(s)], [2.0, 1.0], 0.0)


def test_sinr_closed_form_and_maximality() -> None:
    rng = random.Random(4303)
    for _ in range(40):
        k = rng.randint(1, 5)
        sigs = random_sigs(rng, k, 8)
        amps = [rng.uniform(0.3, 3.0) for _ in range(k)]
        sigma = rng.uniform(0.2, 1.5)
        r = crosscorrelation(sigs)
        m = mmse_rows(r, amps, sigma)
        for u in range(k):
            best = output_sinr(m[u], u, r, amps, sigma)
            assert best == pytest.approx(mmse_sinr(u, sigs, amps, sigma), rel=1e-9)
            mf = [1.0 if j == u else 0.0 for j in range(k)]
            assert output_sinr(mf, u, r, amps, sigma) <= best * (1 + 1e-12)
            for _ in range(20):
                w = [m[u][j] + rng.gauss(0.0, 0.3) for j in range(k)]
                assert output_sinr(w, u, r, amps, sigma) <= best * (1 + 1e-12)


def test_minimizes_mean_square_error() -> None:
    # E[(b_k - w^T z)^2] = 1 - 2 A_k w^T R e_k + w^T (R A^2 R + sigma^2 R) w.
    rng = random.Random(4304)
    sigs = random_sigs(rng, 4, 8)
    amps = [0.7, 1.5, 2.5, 1.0]
    sigma = 0.6
    r = crosscorrelation(sigs)
    k = len(r)
    cov = [[math.fsum(r[i][t] * amps[t] ** 2 * r[t][j] for t in range(k)) + sigma * sigma * r[i][j] for j in range(k)] for i in range(k)]

    def mse(w, u):
        quad = math.fsum(w[i] * cov[i][j] * w[j] for i in range(k) for j in range(k))
        return 1.0 - 2.0 * amps[u] * math.fsum(w[i] * r[i][u] for i in range(k)) + quad

    m = mmse_rows(r, amps, sigma)
    for u in range(k):
        w0 = [v / amps[u] for v in m[u]]
        for _ in range(50):
            w = [v + rng.gauss(0.0, 0.2) for v in w0]
            assert mse(w0, u) <= mse(w, u) + 1e-12


def test_agrees_with_ml_most_of_the_time() -> None:
    # Seed 4305: at sigma = 0.3 the MMSE and brute-force ML decisions agree on
    # at least 95 percent of the 300 vectors.
    rng = random.Random(4305)
    pts = constel.pam(2)
    same = 0
    trials = 300
    for _ in range(trials):
        k = rng.randint(2, 5)
        sigs = random_sigs(rng, k, 8)
        amps = [rng.uniform(0.5, 2.0) for _ in range(k)]
        b = [rng.choice((1, -1)) for _ in range(k)]
        y = chips(sigs, amps, b, 0.3, rng)
        h = [[amps[u] * sigs[u][c] for u in range(k)] for c in range(8)]
        ml = [1 if i == 0 else -1 for i in constel.ml_vector([complex(v) for v in y], h, pts)]
        same += mmse_detector(y, sigs, amps, 0.3) == ml
    assert same >= 0.95 * trials


def test_simulated_ber_matches_exact_value() -> None:
    # Seed 4301: 2000 symbol intervals at sigma = 0.8; the exact rate predicts about 319 errors for user 1.
    rng = random.Random(4301)
    sigma = 0.8
    r = crosscorrelation(S_PAGE)
    p = linear_ber(mmse_rows(r, AMPS, sigma)[0], 0, r, AMPS, sigma)
    trials = 2000
    assert p * trials >= 100
    errors = 0
    for _ in range(trials):
        b = [rng.choice((1, -1)) for _ in range(3)]
        y = chips(S_PAGE, AMPS, b, sigma, rng)
        errors += mmse_detector(y, S_PAGE, AMPS, sigma)[0] != b[0]
    lo, hi = cbb.wilson(errors, trials)
    assert lo <= p <= hi


def test_errors() -> None:
    with pytest.raises(ValueError):
        mmse_detector([0.0] * 8, S_PAGE, [1.0, 0.0, 1.0], 0.5)
    with pytest.raises(ValueError):
        mmse_detector([0.0] * 8, S_PAGE, AMPS, -1.0)
