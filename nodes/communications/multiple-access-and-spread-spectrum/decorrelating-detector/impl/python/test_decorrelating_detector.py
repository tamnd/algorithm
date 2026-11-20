# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decorrelating-detector/. The authors are listed in prov/X81J9E.jsonl.

import math
import random

import pytest

import cbb
import constel
from decorrelating_detector import (
    crosscorrelation,
    decorrelate,
    decorrelating_detector,
    decorrelator_ber,
    linear_ber,
    matched_filter,
    near_far_resistance,
)

R8 = 1.0 / math.sqrt(8.0)
# The signatures of the page: s1 s2 = 0.5, s1 s3 = 0.25, s2 s3 = -0.25.
S_PAGE = [
    [R8 * c for c in (1, 1, 1, 1, 1, 1, 1, 1)],
    [R8 * c for c in (1, 1, 1, 1, 1, 1, -1, -1)],
    [R8 * c for c in (1, -1, 1, -1, 1, -1, 1, 1)],
]


def chips(sigs, amps, b, sigma=0.0, rng=None):
    n = len(sigs[0])
    y = [math.fsum(amps[k] * b[k] * sigs[k][c] for k in range(len(sigs))) for c in range(n)]
    if rng is not None:
        y = [v + rng.gauss(0.0, sigma) for v in y]
    return y


def random_sigs(rng, k, n):
    s = 1.0 / math.sqrt(n)
    while True:
        sigs = [[s * rng.choice((1, -1)) for _ in range(n)] for _ in range(k)]
        if abs(cbb.det(crosscorrelation(sigs))) > 1e-6:
            return sigs


def test_page_example() -> None:
    amps = [1.0, 4.0, 2.0]
    b = [1, -1, 1]
    y = chips(S_PAGE, amps, b)
    r = crosscorrelation(S_PAGE)
    assert [[round(v, 12) for v in row] for row in r] == [[1.0, 0.5, 0.25], [0.5, 1.0, -0.25], [0.25, -0.25, 1.0]]
    z = matched_filter(y, S_PAGE)
    assert [round(v, 12) for v in z] == [-0.5, -4.0, 3.25]
    # The matched filter alone gets user 1 wrong with no noise at all.
    assert [1 if v >= 0 else -1 for v in z] == [-1, -1, 1]
    assert [round(v, 12) for v in decorrelate(z, r)] == [1.0, -4.0, 2.0]
    assert decorrelating_detector(y, S_PAGE) == b


def test_noiseless_recovery_for_any_amplitudes() -> None:
    rng = random.Random(4201)
    for _ in range(200):
        k = rng.randint(1, 6)
        sigs = random_sigs(rng, k, 8)
        amps = [10 ** rng.uniform(-2, 2) for _ in range(k)]
        b = [rng.choice((1, -1)) for _ in range(k)]
        assert decorrelating_detector(chips(sigs, amps, b), sigs) == b


def test_output_is_least_squares_fit() -> None:
    # x = R^-1 S^T y minimizes ||y - S x||^2: the residual is orthogonal to every signature.
    rng = random.Random(4202)
    for _ in range(50):
        k = rng.randint(1, 5)
        sigs = random_sigs(rng, k, 9)
        y = [rng.gauss(0.0, 1.0) for _ in range(9)]
        x = decorrelate(matched_filter(y, sigs), crosscorrelation(sigs))
        res = [y[c] - math.fsum(x[u] * sigs[u][c] for u in range(k)) for c in range(9)]
        for s in sigs:
            assert abs(math.fsum(a * e for a, e in zip(s, res))) < 1e-9


def test_agrees_with_ml_most_of_the_time_at_high_snr() -> None:
    # Seed 4203: at sigma = 0.15 the decorrelator and the brute-force ML detector
    # give the same decisions on at least 97 percent of the 300 vectors.
    rng = random.Random(4203)
    pts = constel.pam(2)
    same = 0
    trials = 300
    for _ in range(trials):
        k = rng.randint(2, 5)
        sigs = random_sigs(rng, k, 8)
        amps = [rng.uniform(0.5, 2.0) for _ in range(k)]
        b = [rng.choice((1, -1)) for _ in range(k)]
        y = chips(sigs, amps, b, 0.15, rng)
        h = [[amps[u] * sigs[u][c] for u in range(k)] for c in range(8)]
        ml = [1 if i == 0 else -1 for i in constel.ml_vector([complex(v) for v in y], h, pts)]
        same += decorrelating_detector(y, sigs) == ml
    assert same >= 0.97 * trials


def test_closed_form_equals_exact_linear_ber() -> None:
    r = crosscorrelation(S_PAGE)
    rinv = [[v.real for v in row] for row in cbb.inv(r)]
    amps = [1.0, 4.0, 2.0]
    for sigma in (0.3, 0.5, 1.0):
        for k in range(3):
            assert linear_ber(rinv[k], k, r, amps, sigma) == pytest.approx(decorrelator_ber(k, r, amps, sigma), rel=1e-12)


def test_ber_does_not_depend_on_interferer_amplitudes() -> None:
    r = crosscorrelation(S_PAGE)
    rinv = [[v.real for v in row] for row in cbb.inv(r)]
    base = linear_ber(rinv[0], 0, r, [1.0, 1.0, 1.0], 0.5)
    for a2, a3 in ((4.0, 2.0), (100.0, 0.01), (1e4, 1e4)):
        assert linear_ber(rinv[0], 0, r, [1.0, a2, a3], 0.5) == pytest.approx(base, rel=1e-12)
    # The matched filter row e_1 does depend on them.
    mf = [1.0, 0.0, 0.0]
    assert linear_ber(mf, 0, r, [1.0, 4.0, 2.0], 0.5) > 0.4
    assert linear_ber(mf, 0, r, [1.0, 0.1, 0.1], 0.5) < 0.04


def test_near_far_resistance_two_users() -> None:
    for rho in (0.0, 0.3, -0.7, 0.95):
        r = [[1.0, rho], [rho, 1.0]]
        assert near_far_resistance(r, 0) == pytest.approx(1.0 - rho * rho, rel=1e-12)


def test_simulated_ber_matches_closed_form() -> None:
    # Seed 4204: 2000 symbol intervals at sigma = 0.8, where the closed form
    # predicts about 333 errors for user 1.
    rng = random.Random(4204)
    amps = [1.0, 4.0, 2.0]
    sigma = 0.8
    r = crosscorrelation(S_PAGE)
    p = decorrelator_ber(0, r, amps, sigma)
    trials = 2000
    assert p * trials >= 100
    errors = 0
    for _ in range(trials):
        b = [rng.choice((1, -1)) for _ in range(3)]
        y = chips(S_PAGE, amps, b, sigma, rng)
        errors += decorrelating_detector(y, S_PAGE)[0] != b[0]
    lo, hi = cbb.wilson(errors, trials)
    assert lo <= p <= hi


def test_singular_correlation_raises() -> None:
    s = [R8] * 8
    with pytest.raises(ValueError):
        decorrelating_detector([0.1] * 8, [s, list(s)])
    # Three users on two chips cannot have independent signatures.
    sigs = [[1.0, 0.0], [0.0, 1.0], [math.sqrt(0.5), math.sqrt(0.5)]]
    with pytest.raises(ValueError):
        decorrelating_detector([0.3, -0.2], sigs)
