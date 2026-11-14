# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/log-rank-test/. The authors are listed in prov/W9TSMC.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from log_rank_test import log_rank, log_rank_permutation
from stdist import chi2_sf

# Freireich et al. (1963) leukemia trial, as listed by Gehan (1965). Group 1 is 6-MP, group 0 placebo.
MP_T = [6, 6, 6, 6, 7, 9, 10, 10, 11, 13, 16, 17, 19, 20, 22, 23, 25, 32, 32, 34, 35]
MP_D = [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
PL_T = [1, 1, 2, 2, 3, 4, 4, 5, 5, 8, 8, 8, 8, 11, 11, 12, 12, 15, 17, 22, 23]
TIMES = MP_T + PL_T
EVENTS = MP_D + [1] * 21
GROUPS = [1] * 21 + [0] * 21


def random_two_sample(rng, n, tmax, pcens):
    times = [rng.randint(1, tmax) for _ in range(n)]
    events = [0 if rng.random() < pcens else 1 for _ in range(n)]
    groups = [rng.randint(0, 1) for _ in range(n)]
    groups[0], groups[-1] = 0, 1
    return times, events, groups


def test_leukemia_data() -> None:
    res = log_rank(TIMES, EVENTS, GROUPS, exact=True)
    assert res.observed1 == 9
    assert len(res.rows) == 17
    assert math.isclose(float(res.expected1), 19.2505, abs_tol=5e-5)
    assert math.isclose(float(res.score), -10.2505, abs_tol=5e-5)
    assert math.isclose(float(res.variance), 6.25696, abs_tol=5e-6)
    assert math.isclose(float(res.statistic), 16.7929, abs_tol=5e-5)
    assert math.isclose(res.p_value, 4.169e-5, rel_tol=1e-3)
    flt = log_rank(TIMES, EVENTS, GROUPS)
    assert math.isclose(flt.statistic, float(res.statistic), rel_tol=1e-12)
    # The first row: t = 1, 42 at risk, 21 in each group, 2 placebo events.
    first = res.rows[0]
    assert (first.time, first.at_risk, first.at_risk1, first.events, first.events1) == (1, 42, 21, 2, 0)
    assert first.expected1 == 1 and first.variance == Fraction(21 * 21 * 2 * 40, 42 * 42 * 41)


def test_rows_are_hypergeometric_moments() -> None:
    # At each event time, choose which d_j of the n_j at risk have the event, uniformly over
    # all C(n_j, d_j) subsets. The count from group 1 then has the mean E_1j and variance V_j.
    rng = random.Random(1966)
    for _ in range(150):
        times, events, groups = random_two_sample(rng, rng.randint(2, 14), rng.randint(1, 6), 0.3)
        try:
            res = log_rank(times, events, groups, exact=True)
        except ValueError:
            continue
        for row in res.rows:
            at_risk = [g for y, g in zip(times, groups) if y >= row.time]
            assert len(at_risk) == row.at_risk and sum(at_risk) == row.at_risk1
            counts = [sum(at_risk[k] for k in sub) for sub in itertools.combinations(range(row.at_risk), row.events)]
            mean = Fraction(sum(counts), len(counts))
            var = Fraction(sum(c * c for c in counts), len(counts)) - mean * mean
            assert row.expected1 == mean and row.variance == var


def test_gehan_weight_is_a_pair_count() -> None:
    def beats(a, b, y, d):
        # a has an observed event, and b is known to outlast a.
        return d[a] == 1 and (y[b] > y[a] or (y[b] == y[a] and d[b] == 0))

    rng = random.Random(1965)
    for _ in range(200):
        y, d, g = random_two_sample(rng, rng.randint(2, 20), rng.randint(1, 8), 0.4)
        try:
            res = log_rank(y, d, g, weights="gehan", exact=True)
        except ValueError:
            continue
        ones = [i for i in range(len(y)) if g[i] == 1]
        zeros = [k for k in range(len(y)) if g[k] == 0]
        pairs = sum(beats(i, k, y, d) - beats(k, i, y, d) for i in ones for k in zeros)
        assert res.score == pairs


def test_gehan_without_censoring_is_mann_whitney() -> None:
    rng = random.Random(1947)
    for _ in range(100):
        n = rng.randint(4, 16)
        y = rng.sample(range(100), n)
        g = [0, 1] + [rng.randint(0, 1) for _ in range(n - 2)]
        res = log_rank(y, [1] * n, g, weights="gehan", exact=True)
        n1 = sum(g)
        smaller = sum(1 for i in range(n) for k in range(n) if g[i] == 1 and g[k] == 0 and y[i] < y[k])
        assert res.score == 2 * smaller - n1 * (n - n1)


def test_score_test_of_the_cox_model() -> None:
    # Without ties U and V are the score and the information of the Cox partial likelihood at beta = 0.
    def partial_loglik(beta, y, d, g):
        total = 0.0
        for i in range(len(y)):
            if d[i]:
                risk = sum(math.exp(beta * g[k]) for k in range(len(y)) if y[k] >= y[i])
                total += beta * g[i] - math.log(risk)
        return total

    rng = random.Random(1972)
    for _ in range(50):
        n = rng.randint(4, 25)
        y = rng.sample(range(1, 200), n)
        d = [rng.randint(0, 1) for _ in range(n)]
        g = [0, 1] + [rng.randint(0, 1) for _ in range(n - 2)]
        try:
            res = log_rank(y, d, g)
        except ValueError:
            continue
        h = 1e-4
        score = (partial_loglik(h, y, d, g) - partial_loglik(-h, y, d, g)) / (2 * h)
        info = -(partial_loglik(h, y, d, g) - 2 * partial_loglik(0, y, d, g) + partial_loglik(-h, y, d, g)) / h**2
        assert math.isclose(score, res.score, abs_tol=1e-6)
        assert math.isclose(info, res.variance, rel_tol=1e-5, abs_tol=1e-6)


def test_permutation_matches_brute_force() -> None:
    def direct_score(y, d, g):
        u = Fraction(0)
        for t in sorted({y[i] for i in range(len(y)) if d[i]}):
            n = sum(1 for x in y if x >= t)
            n1 = sum(1 for x, h in zip(y, g) if x >= t and h)
            dt = sum(1 for x, e in zip(y, d) if x == t and e)
            d1 = sum(1 for x, e, h in zip(y, d, g) if x == t and e and h)
            u += d1 - Fraction(dt * n1, n)
        return u

    rng = random.Random(1972)
    for _ in range(12):
        n = rng.randint(4, 9)
        y, d, g = random_two_sample(rng, n, 6, 0.3)
        n1 = sum(g)
        obs = abs(direct_score(y, d, g))
        hits = total = 0
        for chosen in itertools.combinations(range(n), n1):
            lab = [1 if k in chosen else 0 for k in range(n)]
            total += 1
            hits += abs(direct_score(y, d, lab)) >= obs
        assert math.isclose(log_rank_permutation(y, d, g), hits / total, abs_tol=1e-12)


def test_monte_carlo_size() -> None:
    # H0: both groups Exp(1), censoring Exp(0.5) in both, 30 per group. r = 2000, seed 1966.
    rng = random.Random(1966)
    r, rejections = 2000, 0
    for _ in range(r):
        y, d = [], []
        for _ in range(60):
            a, b = rng.expovariate(1.0), rng.expovariate(0.5)
            y.append(min(a, b))
            d.append(1 if a <= b else 0)
        rejections += log_rank(y, d, [1] * 30 + [0] * 30).p_value < 0.05
    size = rejections / r
    assert abs(size - 0.05) < 4 * math.sqrt(0.05 * 0.95 / r) + 0.01


def test_symmetry_and_p_value() -> None:
    rng = random.Random(5)
    for _ in range(50):
        y, d, g = random_two_sample(rng, 30, 10, 0.3)
        try:
            a = log_rank(y, d, g, exact=True)
        except ValueError:
            continue
        b = log_rank(y, d, [1 - x for x in g], exact=True)
        assert a.score == -b.score and a.variance == b.variance and a.statistic == b.statistic
        assert math.isclose(a.p_value, chi2_sf(float(a.statistic), 1), rel_tol=1e-15)
        for w in ("tarone-ware", "peto-peto", "fleming-harrington"):
            assert 0 <= log_rank(y, d, g, weights=w, rho=1.0, gamma=1.0).p_value <= 1


def test_single_subject_at_risk_has_zero_variance() -> None:
    res = log_rank([1, 2, 3], [1, 1, 1], [0, 1, 0], exact=True)
    assert res.rows[-1].at_risk == 1 and res.rows[-1].variance == 0


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        log_rank([1, 2], [1, 1], [1, 1])
    with pytest.raises(ValueError):
        log_rank([1, 2], [1, 1], [0, 2])
    with pytest.raises(ValueError):
        log_rank([1, 2], [1, 1], [0, 1], weights="wilcoxon")
    with pytest.raises(ValueError):
        log_rank([1, 2], [1, 1], [0, 1], weights="tarone-ware", exact=True)
    with pytest.raises(ValueError):
        log_rank([1, 2], [0, 0], [0, 1])
