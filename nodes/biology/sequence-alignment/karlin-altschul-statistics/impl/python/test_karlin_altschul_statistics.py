# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karlin-altschul-statistics/. The authors are listed in prov/TJVQ07.jsonl.

import math
import random

import pytest

from karlin_altschul_statistics import (
    bit_score,
    count_hsps,
    evalue,
    evalue_from_bits,
    expected_score,
    karlin_k,
    pvalue,
    relative_entropy,
    score_distribution,
    solve_lambda,
)

DNA = {c: 0.25 for c in "ACGT"}


def dna_scheme(match: int, mismatch: int):
    return lambda a, b: match if a == b else mismatch


def test_distribution_of_uniform_dna() -> None:
    d = score_distribution(DNA, DNA, dna_scheme(1, -2))
    assert d == {1: 0.25, -2: 0.75}
    assert expected_score(d) == pytest.approx(-1.25)


def test_lambda_solves_the_equation() -> None:
    rng = random.Random(7)
    for _ in range(200):
        r = rng.randint(2, 6)
        scores = rng.sample(range(-8, 9), r)
        if not any(s > 0 for s in scores) or not any(s < 0 for s in scores):
            continue
        w = [rng.random() + 0.01 for _ in scores]
        dist = {s: x / sum(w) for s, x in zip(scores, w)}
        if expected_score(dist) >= -1e-9:
            continue
        lam = solve_lambda(dist)
        assert lam > 0
        assert sum(p * math.exp(lam * s) for s, p in dist.items()) == pytest.approx(1.0, abs=1e-10)
        # f < 0 just left of lambda: lambda is the positive root, not another one
        assert sum(p * math.exp(0.999 * lam * s) for s, p in dist.items()) < 1.0


def test_closed_forms_for_plus_minus_one() -> None:
    # The series converges slowly when the expected score is close to 0,
    # so the test stays away from p = 1/2.
    for p in (0.1, 0.25, 0.3, 0.35):
        q = 1 - p
        dist = {1: p, -1: q}
        lam = solve_lambda(dist)
        assert lam == pytest.approx(math.log(q / p), rel=1e-12)
        assert karlin_k(dist) == pytest.approx((q - p) ** 2 / q, rel=1e-9)


def test_uniform_dna_plus1_minus2() -> None:
    dist = {1: 0.25, -2: 0.75}
    lam = solve_lambda(dist)
    # e^lam is the root x > 1 of x^3 - 4x^2 + 3 = 0 (multiply 0.25x + 0.75/x^2 = 1 by 4x^2)
    x = (3 + math.sqrt(21)) / 2
    assert lam == pytest.approx(math.log(x), rel=1e-12)
    assert round(lam, 4) == 1.3327
    assert round(karlin_k(dist), 3) == 0.621
    assert round(relative_entropy(dist, lam), 3) == 1.124


def test_k_does_not_change_when_scores_are_scaled() -> None:
    a = {1: 0.25, -2: 0.75}
    b = {5: 0.25, -10: 0.75}
    assert karlin_k(a) == pytest.approx(karlin_k(b), rel=1e-12)
    assert solve_lambda(b) == pytest.approx(solve_lambda(a) / 5, rel=1e-10)


def test_conditions_are_checked() -> None:
    with pytest.raises(ValueError):
        solve_lambda({1: 0.5, -1: 0.5})  # expected score 0
    with pytest.raises(ValueError):
        solve_lambda({0: 0.5, -1: 0.5})  # no positive score


def test_bits_and_evalues_agree() -> None:
    lam, k = solve_lambda({1: 0.25, -2: 0.75}), karlin_k({1: 0.25, -2: 0.75})
    for s in (10, 20, 30, 45):
        e1 = evalue(s, 1000, 10**6, lam, k)
        e2 = evalue_from_bits(bit_score(s, lam, k), 1000, 10**6)
        assert e1 == pytest.approx(e2, rel=1e-12)
    assert pvalue(1.0) == pytest.approx(1 - math.exp(-1))
    assert pvalue(1e-9) == pytest.approx(1e-9, rel=1e-6)


def _excursions(n: int, p: float, up: int, down: int, cutoff: int, rng: random.Random) -> int:
    h = peak = count = 0
    r = rng.random
    for _ in range(n):
        h += up if r() < p else down
        if h <= 0:
            if peak >= cutoff:
                count += 1
            h = peak = 0
        elif h > peak:
            peak = h
    return count


def test_count_on_a_long_random_walk() -> None:
    # One long walk of N steps stands for N cells of a comparison. The count
    # of excursions with peak >= S should be close to K N exp(-lam S).
    # Tolerance: 20 percent, about three Poisson standard deviations here.
    rng = random.Random(1)
    for p, up, down, cutoff in ((0.25, 1, -1, 8), (0.25, 1, -2, 7)):
        dist = {up: p, down: 1 - p}
        lam, k = solve_lambda(dist), karlin_k(dist)
        n = 2_000_000
        got = _excursions(n, p, up, down, cutoff, rng)
        want = k * n * math.exp(-lam * cutoff)
        assert abs(got - want) <= 0.20 * want, (got, want)


def test_evalue_on_random_dna_pairs() -> None:
    # Four pairs of random DNA sequences of length 600, scores +1/-2.
    # Edge effects make the count a little lower than K m n e^(-lam S);
    # the tolerance is 35 percent of the prediction.
    rng = random.Random(11)
    dist = {1: 0.25, -2: 0.75}
    lam, k = solve_lambda(dist), karlin_k(dist)
    score = dna_scheme(1, -2)
    m = n = 600
    cutoff = 7
    got = 0
    for _ in range(4):
        x = [rng.choice("ACGT") for _ in range(m)]
        y = [rng.choice("ACGT") for _ in range(n)]
        got += count_hsps(x, y, score, cutoff)
    want = 4 * evalue(cutoff, m, n, lam, k)
    assert abs(got - want) <= 0.35 * want, (got, want)
