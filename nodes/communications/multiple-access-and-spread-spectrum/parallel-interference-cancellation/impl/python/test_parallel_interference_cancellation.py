# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-interference-cancellation/. The authors are listed in prov/9G0E22.jsonl.

import itertools
import math
import random

import pytest

import cbb
import constel
from parallel_interference_cancellation import (
    crosscorrelation,
    linear_pic,
    matched_filter,
    pic,
    pic_detector,
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
    while True:
        sigs = [[s * rng.choice((1, -1)) for _ in range(n)] for _ in range(k)]
        if abs(cbb.det(crosscorrelation(sigs))) > 1e-6:
            return sigs


def test_page_example() -> None:
    b = [1, -1, 1]
    z = matched_filter(chips(S_PAGE, AMPS, b), S_PAGE)
    r = crosscorrelation(S_PAGE)
    assert [round(v, 12) for v in z] == [-0.5, -4.0, 3.25]
    assert pic(z, r, AMPS, 3) == [[-1, -1, 1], b, b, b]


def test_right_decisions_are_a_fixed_point_without_noise() -> None:
    rng = random.Random(4501)
    for _ in range(200):
        k = rng.randint(1, 6)
        sigs = random_sigs(rng, k, 8)
        amps = [rng.uniform(0.1, 5.0) for _ in range(k)]
        b = [rng.choice((1, -1)) for _ in range(k)]
        z = matched_filter(chips(sigs, amps, b), sigs)
        assert pic(z, crosscorrelation(sigs), amps, 4, start=b)[1:] == [b] * 4


def test_decorrelator_start_is_right_without_noise() -> None:
    rng = random.Random(4502)
    for _ in range(200):
        k = rng.randint(1, 6)
        sigs = random_sigs(rng, k, 8)
        amps = [rng.uniform(0.1, 5.0) for _ in range(k)]
        b = [rng.choice((1, -1)) for _ in range(k)]
        assert pic_detector(chips(sigs, amps, b), sigs, amps, 3, start="decorrelator") == b


def test_hard_decisions_can_oscillate() -> None:
    # Two equal users with correlation 0.9 and z = (0.5, 0.5): the stages
    # swing between (+1, +1) and (-1, -1) and never settle.
    r = [[1.0, 0.9], [0.9, 1.0]]
    hist = pic([0.5, 0.5], r, [1.0, 1.0], 6)
    assert hist == [[1, 1], [-1, -1]] * 3 + [[1, 1]]


def test_linear_pic_is_jacobi_and_tends_to_the_decorrelator() -> None:
    r = crosscorrelation(S_PAGE)
    z = [-0.5, -4.0, 3.25]
    assert [round(v, 12) for v in linear_pic(z, r, 1)] == [0.6875, -2.9375, 2.375]
    # The eigenvalues of R - I are 0.5 and (-1 +- sqrt 3) / 4, so the spectral radius is about 0.683 < 1.
    x = linear_pic(z, r, 80)
    assert x == pytest.approx([1.0, -4.0, 2.0], abs=1e-10)


def test_linear_pic_diverges_when_spectral_radius_exceeds_one() -> None:
    # R - I with all off-diagonal entries 0.6 has the eigenvalue 1.2.
    r = [[1.0, 0.6, 0.6], [0.6, 1.0, 0.6], [0.6, 0.6, 1.0]]
    z = [1.0, -0.5, 0.25]
    norms = [max(abs(v) for v in linear_pic(z, r, m)) for m in (10, 20, 40)]
    assert norms[0] < norms[1] < norms[2]
    assert norms[2] > 100.0


def test_noiseless_oscillation_with_two_users() -> None:
    # A = (1, 0.8), correlation 0.9, b = (+1, -1), no noise. The stages swing
    # between (+1, +1) and (-1, -1) and never reach the sent bits.
    r = [[1.0, 0.9], [0.9, 1.0]]
    amps = [1.0, 0.8]
    z = [1.0 - 0.9 * 0.8, -0.8 + 0.9 * 1.0]
    assert pic(z, r, amps, 5) == [[1, 1], [-1, -1], [1, 1], [-1, -1], [1, 1], [-1, -1]]


def test_two_users_converge_in_one_stage_without_noise() -> None:
    # For K = 2 without noise, if the stronger amplitude exceeds 2 |rho| times
    # the weaker one, stage 1 is right for both users and stays right.
    rng = random.Random(4503)
    checked = 0
    while checked < 200:
        rho = rng.uniform(-0.95, 0.95)
        r = [[1.0, rho], [rho, 1.0]]
        amps = [rng.uniform(0.1, 3.0), rng.uniform(0.1, 3.0)]
        if max(amps) <= 2.0 * abs(rho) * min(amps):
            continue
        checked += 1
        for b in itertools.product((1, -1), repeat=2):
            z = [amps[0] * b[0] + rho * amps[1] * b[1], amps[1] * b[1] + rho * amps[0] * b[0]]
            assert pic(z, r, amps, 3)[1:] == [list(b)] * 3


def test_agrees_with_ml_most_of_the_time() -> None:
    # Seed 4504: two stages from the decorrelator at sigma = 0.3 give the ML
    # decisions on at least 90 percent of 300 vectors.
    rng = random.Random(4504)
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
        same += pic_detector(y, sigs, amps, 2, start="decorrelator") == ml
    assert same >= 0.90 * trials


def test_errors() -> None:
    r = [[1.0, 0.0], [0.0, 1.0]]
    with pytest.raises(ValueError):
        pic([1.0, 1.0], r, [1.0], 1)
    with pytest.raises(ValueError):
        pic([1.0, 1.0], r, [1.0, 1.0], -1)
    with pytest.raises(ValueError):
        pic_detector([0.0] * 8, S_PAGE[:2], [1.0, 1.0], 1, start="sic")
