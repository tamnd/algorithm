# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pwm-score-p-value/. The authors are listed in prov/YNZJ2F.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from bioseq import DNA
from pwm_score_p_value import (log_odds_matrix, pvalue_round, pwm_score_p_value, score, score_distribution)

BA2F_SITES = ["TCTCGGGG", "CCAAGGTG", "TACAGGCG", "TTCAGGTG", "TCCACGTG"]
UNIFORM = [Fraction(1, 4)] * 4


def brute_force(M, p, alpha):
    """P(score >= alpha) by listing all words, in exact arithmetic."""
    alpha = Fraction(alpha)
    total = 0
    for w in itertools.product(range(4), repeat=len(M)):
        if sum(Fraction(M[j][a]) for j, a in enumerate(w)) >= alpha:
            pr = 1
            for a in w:
                pr *= p[a]
            total += pr
    return total


def random_matrix(rng, L, integer=False):
    if integer:
        return [[rng.randint(-3, 3) for _ in range(4)] for _ in range(L)]
    return [[rng.uniform(-3, 2) for _ in range(4)] for _ in range(L)]


def random_background(rng):
    w = [Fraction(rng.randint(1, 9)) for _ in range(4)]
    return [x / sum(w) for x in w]


def test_small_example():
    M = [[2, -1, -1, 0], [-1, 3, 0, -1]]
    dist = score_distribution(M, UNIFORM)
    assert dist == {-2: Fraction(1, 4), -1: Fraction(1, 4), 0: Fraction(1, 16), 1: Fraction(1, 8),
                    2: Fraction(3, 16), 3: Fraction(1, 16), 5: Fraction(1, 16)}
    r = pwm_score_p_value(M, UNIFORM, 3)
    assert r.exact and r.lo == r.hi == Fraction(1, 8) and r.rounds == 1 and r.error == 0


def test_against_brute_force():
    # Real matrices, exact backgrounds, thresholds at random and at word scores.
    rng = random.Random(1)
    for _ in range(40):
        L = rng.randint(1, 5)
        M = random_matrix(rng, L)
        p = random_background(rng)
        words = ["".join(rng.choice(DNA) for _ in range(L)) for _ in range(2)]
        for alpha in [rng.uniform(-3 * L, 2 * L)] + [score(M, w) for w in words]:
            truth = brute_force(M, p, alpha)
            r = pwm_score_p_value(M, p, alpha, max_rounds=12)
            assert r.lo <= truth <= r.hi
            if r.exact:
                assert r.lo == r.hi == truth


def test_every_round_brackets_the_truth():
    rng = random.Random(2)
    for _ in range(25):
        L = rng.randint(2, 5)
        M = random_matrix(rng, L)
        alpha = rng.uniform(-L, 2 * L)
        truth = brute_force(M, UNIFORM, alpha)
        last_lo = 0
        for k in range(1, 5):
            r = pwm_score_p_value(M, UNIFORM, alpha, max_rounds=k)
            assert r.lo <= truth <= r.hi
            assert r.error < L * r.eps
            # The finer grid rounds each entry down by less, so lo cannot fall.
            assert r.lo >= last_lo
            last_lo = r.lo
            if r.exact:
                break


def test_integer_matrix_is_exact_in_one_round():
    rng = random.Random(3)
    for _ in range(20):
        M = random_matrix(rng, rng.randint(1, 5), integer=True)
        alpha = rng.randint(-6, 8)
        r = pwm_score_p_value(M, UNIFORM, alpha)
        assert r.exact and r.rounds == 1 and r.error == 0
        assert r.lo == brute_force(M, UNIFORM, alpha)


def test_pruned_round_equals_full_distribution():
    # pvalue_round drops and lumps partial scores; the result must match the full table.
    rng = random.Random(4)
    for _ in range(30):
        N = random_matrix(rng, rng.randint(1, 6), integer=True)
        p = random_background(rng)
        B = rng.randint(-8, 6)
        A = B + rng.randint(0, 4)
        sure, middle = pvalue_round(N, p, A, B)
        dist = score_distribution(N, p)
        assert sure == sum(q for s, q in dist.items() if s >= A)
        assert middle == {int(s): q for s, q in dist.items() if B <= s < A}


def test_distribution_sums_to_one_and_p_value_falls():
    rng = random.Random(5)
    M = random_matrix(rng, 4)
    p = random_background(rng)
    dist = score_distribution(M, p)
    assert sum(dist.values()) == 1
    scores = sorted(dist)
    tail = 1
    for s in scores:
        # P(score >= s) from the table, and the algorithm at the same threshold.
        # A word scores exactly s and its entries are off the grid, so the
        # bracket cannot close; two rounds are enough to check it.
        r = pwm_score_p_value(M, p, s, max_rounds=2)
        assert r.lo <= tail <= r.hi
        assert not r.exact
        tail -= dist[s]
    assert tail == 0
    values = [pwm_score_p_value(M, p, a / 4).hi for a in range(-48, 32)]
    assert all(x >= y for x, y in zip(values, values[1:]))


def test_ba2f_log_odds():
    M = log_odds_matrix(BA2F_SITES, [0.25] * 4)
    assert abs(M[0][DNA.index("T")] - math.log2((4.25 / 6) / 0.25)) < 1e-12
    truth = {4.0: Fraction(586, 65536), 6.0: Fraction(178, 65536), 8.0: Fraction(40, 65536)}
    rounds = {4.0: 2, 6.0: 4, 8.0: 2}
    for alpha, value in truth.items():
        r = pwm_score_p_value(M, UNIFORM, alpha)
        assert r.exact and r.lo == value and r.rounds == rounds[alpha]
    count = sum(1 for w in itertools.product(DNA, repeat=8) if score(M, "".join(w)) >= 6.0)
    assert count == 178


def test_zero_background_letter():
    M = [[1, 5, 0, 0], [2, 0, 7, 0]]
    p = [Fraction(1, 2), 0, Fraction(1, 2), 0]
    r = pwm_score_p_value(M, p, 4)
    assert r.exact and r.lo == brute_force(M, p, 4) == Fraction(1, 2)


def test_float_background():
    rng = random.Random(6)
    M = random_matrix(rng, 4)
    p = [0.1, 0.4, 0.3, 0.2]
    r = pwm_score_p_value(M, p, 0.5, max_rounds=12)
    truth = brute_force(M, [Fraction(x) for x in p], 0.5)
    assert r.exact and abs(r.lo - truth) < 1e-12


def test_errors():
    with pytest.raises(ValueError):
        pwm_score_p_value([], UNIFORM, 0)
    with pytest.raises(ValueError):
        pwm_score_p_value([[1, 2, 3]], UNIFORM, 0)
    with pytest.raises(ValueError):
        pwm_score_p_value([[1, 2, 3, 4]], [0.5, 0.5, 0.5, 0.5], 0)
    with pytest.raises(ValueError):
        pwm_score_p_value([[1, 2, 3, 4]], UNIFORM, 0, eps0=0)
    with pytest.raises(ValueError):
        pwm_score_p_value([[1, 2, 3, 4]], UNIFORM, 0, max_rounds=0)
    with pytest.raises(ValueError):
        pwm_score_p_value([[1, 2, float("inf"), 4]], UNIFORM, 0)
    with pytest.raises(ValueError):
        log_odds_matrix(["ACG", "AC"], [0.25] * 4)
