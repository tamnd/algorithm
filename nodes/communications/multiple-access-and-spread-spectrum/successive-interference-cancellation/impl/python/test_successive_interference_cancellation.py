# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successive-interference-cancellation/. The authors are listed in prov/TZZ989.jsonl.

import itertools
import math
import random

import pytest

import cbb
import constel
from successive_interference_cancellation import (
    crosscorrelation,
    matched_filter,
    sic,
    sic_chip_domain,
    sic_detector,
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
    z = matched_filter(chips(S_PAGE, AMPS, b), S_PAGE)
    r = crosscorrelation(S_PAGE)
    assert [round(v, 12) for v in z] == [-0.5, -4.0, 3.25]
    dec, order = sic(z, r, AMPS)
    assert order == [1, 2, 0]
    assert dec == b
    # Without the amplitudes the order comes from |z| and the estimates are |x|.
    dec, order = sic(z, r)
    assert order == [1, 2, 0]
    assert dec == b


def test_chip_domain_and_matched_filter_domain_agree() -> None:
    rng = random.Random(4401)
    for _ in range(200):
        k = rng.randint(1, 6)
        sigs = random_sigs(rng, k, 8)
        amps = [rng.uniform(0.2, 5.0) for _ in range(k)]
        b = [rng.choice((1, -1)) for _ in range(k)]
        y = chips(sigs, amps, b, 0.7, rng)
        assert sic_detector(y, sigs, amps) == sic_chip_domain(y, sigs, amps)


def test_noiseless_correct_under_dominance() -> None:
    # If A_k > sum over the users j after k of A_j |R_kj| for every k, then SIC
    # with known amplitudes decides every bit right when there is no noise.
    rng = random.Random(4402)
    checked = 0
    while checked < 300:
        k = rng.randint(1, 6)
        sigs = random_sigs(rng, k, 8)
        r = crosscorrelation(sigs)
        amps = sorted((rng.uniform(0.1, 1.0) * 3.0 ** rng.randint(0, 4) for _ in range(k)), reverse=True)
        if any(amps[u] <= math.fsum(amps[j] * abs(r[u][j]) for j in range(u + 1, k)) for u in range(k)):
            continue
        checked += 1
        for b in itertools.product((1, -1), repeat=k):
            assert sic_detector(chips(sigs, amps, list(b)), sigs, amps) == list(b)


def test_equal_powers_can_fail_without_noise() -> None:
    s1 = [R8] * 8
    s2 = [R8] * 7 + [-R8]
    s3 = [-R8] + [R8] * 7
    sigs = [s1, s2, s3]
    r = crosscorrelation(sigs)
    assert [round(r[0][1], 12), round(r[0][2], 12)] == [0.75, 0.75]
    b = [1, -1, -1]
    y = chips(sigs, [1.0, 1.0, 1.0], b)
    assert sic_detector(y, sigs, [1.0, 1.0, 1.0])[0] == -1


def test_weak_user_first_fails_without_noise() -> None:
    s1 = S_PAGE[0]
    s2 = S_PAGE[1]
    amps = [1.0, 4.0]
    b = [1, -1]
    z = matched_filter(chips([s1, s2], amps, b), [s1, s2])
    r = crosscorrelation([s1, s2])
    assert sic(z, r, amps)[0] == b
    assert sic(z, r, amps, order=[0, 1])[0] == [-1, -1]


def test_first_user_has_the_matched_filter_error_rate() -> None:
    # Seed 4403: the strongest user is decided before any cancellation, so its
    # error rate is the exact matched filter rate; about 150 errors are expected.
    rng = random.Random(4403)
    amps = [1.0, 1.5, 0.8]
    sigma = 0.8
    r = crosscorrelation(S_PAGE)
    k = 1
    p = 0.0
    for b1, b3 in itertools.product((1, -1), repeat=2):
        p += cbb.qfunc((amps[1] + r[1][0] * amps[0] * b1 + r[1][2] * amps[2] * b3) / sigma) / 4
    trials = 2500
    assert p * trials >= 100
    errors = 0
    for _ in range(trials):
        b = [rng.choice((1, -1)) for _ in range(3)]
        errors += sic_detector(chips(S_PAGE, amps, b, sigma, rng), S_PAGE, amps)[k] != b[k]
    lo, hi = cbb.wilson(errors, trials)
    assert lo <= p <= hi


def test_agrees_with_ml_most_of_the_time_with_spread_powers() -> None:
    # Seed 4404: amplitudes 3 times apart and sigma = 0.2; SIC with known
    # amplitudes gives the ML decisions on at least 90 percent of 300 vectors.
    rng = random.Random(4404)
    pts = constel.pam(2)
    same = 0
    trials = 300
    for _ in range(trials):
        k = rng.randint(2, 5)
        sigs = random_sigs(rng, k, 8)
        amps = [3.0 ** u for u in range(k)]
        rng.shuffle(amps)
        b = [rng.choice((1, -1)) for _ in range(k)]
        y = chips(sigs, amps, b, 0.2, rng)
        h = [[amps[u] * sigs[u][c] for u in range(k)] for c in range(8)]
        ml = [1 if i == 0 else -1 for i in constel.ml_vector([complex(v) for v in y], h, pts)]
        same += sic_detector(y, sigs, amps) == ml
    assert same >= 0.90 * trials


def test_errors() -> None:
    with pytest.raises(ValueError):
        sic([1.0, 2.0], [[1.0, 0.0], [0.0, 1.0]], [1.0])
    with pytest.raises(ValueError):
        sic([1.0, 2.0], [[1.0, 0.0], [0.0, 1.0]], [1.0, -1.0])
    with pytest.raises(ValueError):
        sic([1.0, 2.0], [[1.0, 0.0], [0.0, 1.0]], order=[0, 0])
