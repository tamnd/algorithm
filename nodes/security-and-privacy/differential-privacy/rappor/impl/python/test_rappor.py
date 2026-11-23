# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rappor/. The authors are listed in prov/WNQFZC.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

import dpkit
from rappor import (
    RapporClient,
    RapporParams,
    bit_counts,
    bloom_filter,
    bloom_positions,
    debiased_counts,
    epsilon_one_report,
    epsilon_permanent,
    first_report_pmf,
    fit_candidates,
    one_probabilities,
    permanent_pmf,
    rappor_estimate,
)

F = Fraction
BASE = RapporParams(k=4, h=2, f=F(1, 2), p=F(1, 2), q=F(3, 4))


def filters_with_at_most(k, h):
    """All k-bit vectors with between 1 and h ones: the possible Bloom filters."""
    return [b for b in itertools.product((0, 1), repeat=k) if 1 <= sum(b) <= h]


def instantaneous_pmf(bp, params):
    """Exact pmf of S given the memoized bits B'."""
    out = {}
    for s in itertools.product((0, 1), repeat=len(bp)):
        pr = F(1)
        for bit, rep in zip(bp, s):
            one = params.q if bit else params.p
            pr *= one if rep else 1 - one
        out[s] = pr
    return out


def two_report_pmf(b, params):
    """Exact pmf of two reports of the same value: both reuse one draw of B'."""
    out = {}
    for bp, pb in permanent_pmf(b, params.f).items():
        inst = instantaneous_pmf(bp, params)
        for s1, p1 in inst.items():
            for s2, p2 in inst.items():
                out[(s1, s2)] = out.get((s1, s2), 0) + pb * p1 * p2
    return out


def test_check_values():
    params = RapporParams(k=8, h=2, f=F(1, 2), p=F(1, 2), q=F(3, 4))
    assert one_probabilities(params) == (F(11, 16), F(9, 16))
    assert abs(epsilon_permanent(params) - math.log(81)) < 1e-12
    assert abs(epsilon_one_report(params) - 1.0743) < 1e-4
    four = RapporParams(k=8, h=4, f=F(1, 2), p=F(1, 2), q=F(3, 4))
    assert abs(epsilon_permanent(four) - 8.7889) < 1e-4
    assert abs(epsilon_one_report(four) - 2.1486) < 1e-4
    assert bloom_positions("apple", 0, params) == [2, 3]
    assert bloom_filter("fig", 0, params) == (0, 1, 0, 0, 1, 0, 0, 0)


def test_bad_parameters():
    with pytest.raises(ValueError):
        RapporParams(k=4, h=2, f=F(1), p=F(1, 2), q=F(3, 4))
    with pytest.raises(ValueError):
        RapporParams(k=4, h=2, f=F(1, 2), p=F(3, 4), q=F(1, 2))
    with pytest.raises(ValueError):
        RapporClient(cohort=1, params=BASE).report("a", random.Random(0))


def test_permanent_bits_meet_epsilon_infinity_and_are_tight():
    pairs = [(b1, b2) for b1 in filters_with_at_most(4, 2) for b2 in filters_with_at_most(4, 2)]
    eps = epsilon_permanent(BASE)
    assert dpkit.is_pure_dp(lambda b: permanent_pmf(b, BASE.f), pairs, eps)
    disjoint = [((1, 1, 0, 0), (0, 0, 1, 1))]
    assert not dpkit.is_pure_dp(lambda b: permanent_pmf(b, BASE.f), disjoint, eps - 0.01)


def test_one_report_meets_epsilon_one_and_is_tight():
    pairs = [(b1, b2) for b1 in filters_with_at_most(4, 2) for b2 in filters_with_at_most(4, 2)]
    eps = epsilon_one_report(BASE)
    assert dpkit.is_pure_dp(lambda b: first_report_pmf(b, BASE), pairs, eps)
    disjoint = [((1, 1, 0, 0), (0, 0, 1, 1))]
    assert not dpkit.is_pure_dp(lambda b: first_report_pmf(b, BASE), disjoint, eps - 0.01)


def test_two_reports_of_one_value_stay_within_epsilon_infinity():
    params = RapporParams(k=3, h=1, f=F(1, 2), p=F(1, 4), q=F(3, 4))
    pairs = [((1, 0, 0), (0, 1, 0)), ((0, 0, 1), (1, 0, 0))]
    assert dpkit.is_pure_dp(lambda b: two_report_pmf(b, params), pairs, epsilon_permanent(params))
    # Two fresh draws of B' would spend more than one epsilon_1 each: the memo matters.
    p = two_report_pmf((1, 0, 0), params)
    q = two_report_pmf((0, 1, 0), params)
    assert dpkit.max_privacy_loss(p, q) > epsilon_one_report(params)


def test_random_parameters_against_closed_form_loss():
    rng = random.Random(11)
    for _ in range(500):
        k = rng.randint(2, 4)
        h = rng.randint(1, 2)
        den = rng.randint(3, 9)
        f = F(rng.randint(1, den - 1), den)
        pn = rng.randint(0, den - 2)
        p = F(pn, den)
        q = F(rng.randint(pn + 1, den), den)
        params = RapporParams(k=k, h=h, f=f, p=p, q=q)
        b1 = tuple(rng.randint(0, 1) for _ in range(k))
        b2 = tuple(rng.randint(0, 1) for _ in range(k))
        q_star, p_star = one_probabilities(params)
        # Independent oracle: the loss is the sum of the per-bit log ratios at the worst output.
        a = sum(1 for x, y in zip(b1, b2) if x == 1 and y == 0)
        c = sum(1 for x, y in zip(b1, b2) if x == 0 and y == 1)
        expect = a * math.log(q_star / p_star) + c * math.log((1 - p_star) / (1 - q_star))
        got = dpkit.max_privacy_loss(first_report_pmf(b1, params), first_report_pmf(b2, params))
        assert abs(got - expect) < 1e-9
        keep = math.log((1 - f / 2) / (f / 2))
        got_perm = dpkit.max_privacy_loss(permanent_pmf(b1, f), permanent_pmf(b2, f))
        assert abs(got_perm - (a + c) * keep) < 1e-9
        if a <= h and c <= h:
            assert got <= epsilon_one_report(params) + 1e-9
            assert got_perm <= epsilon_permanent(params) + 1e-9


def test_memo_is_reused_and_reports_have_the_right_law():
    rng = random.Random(5)
    client = RapporClient(cohort=0, params=BASE)
    client.report("a", rng)
    first = dict(client.memo)
    for _ in range(20):
        client.report("a", rng)
    assert client.memo == first
    client.report("b", rng)
    assert set(client.memo) == {"a", "b"}
    # Fresh clients: the first report has the law of first_report_pmf.
    n = 2000
    samples = [RapporClient(cohort=0, params=BASE).report("a", rng) for _ in range(n)]
    emp = dpkit.empirical_pmf(samples)
    exact = first_report_pmf(bloom_filter("a", 0, BASE), BASE)
    margin = dpkit.hoeffding_margin(n, 1e-6 / 16)
    for s, pr in exact.items():
        assert abs(emp.get(s, 0.0) - float(pr)) <= margin


def test_debiased_counts_are_exactly_unbiased():
    rng = random.Random(7)
    for _ in range(500):
        den = rng.randint(3, 8)
        f = F(rng.randint(0, den - 1), den)
        pn = rng.randint(0, den - 2)
        p = F(pn, den)
        q = F(rng.randint(pn + 1, den), den)
        params = RapporParams(k=3, h=1, f=f, p=p, q=q)
        n = rng.randint(1, 50)
        n_set = rng.randint(0, n)
        q_star, p_star = one_probabilities(params)
        expected_c = [[n_set * q_star + (n - n_set) * p_star, 0, 0]]
        t = debiased_counts(expected_c, [n], params)
        assert t[0][0] == n_set


def test_least_squares_recovers_counts_from_expected_bits():
    params = RapporParams(k=8, h=2, f=F(1, 2), p=F(1, 2), q=F(3, 4), m=2)
    candidates = ["apple", "fig", "kiwi"]
    truth = {"apple": 30, "fig": 12, "kiwi": 5}
    q_star, p_star = one_probabilities(params)
    # Half of the holders of each value are in each cohort; c is the exact expected count.
    half = F(sum(truth.values()), 2)
    c = []
    for j in range(params.m):
        row = []
        for i in range(params.k):
            n_set = sum(F(n, 2) for v, n in truth.items() if bloom_filter(v, j, params)[i])
            row.append(n_set * q_star + (half - n_set) * p_star)
        c.append(row)
    deb = debiased_counts(c, [half] * params.m, params)
    assert fit_candidates(deb, candidates, params) == [F(truth[v], 2) for v in candidates]


def test_end_to_end_estimate_is_close():
    rng = random.Random(9)
    params = RapporParams(k=8, h=2, f=F(1, 4), p=F(1, 4), q=F(3, 4), m=2)
    values = ["apple"] * 900 + ["fig"] * 600 + ["kiwi"] * 300
    reports = []
    for idx, v in enumerate(values):
        cohort = idx % params.m
        reports.append((cohort, RapporClient(cohort=cohort, params=params).report(v, rng)))
    c, totals = bit_counts(reports, params)
    assert totals == [900, 900]
    est = rappor_estimate(reports, ["apple", "fig", "kiwi"], params)
    for got, want in zip(est, [900, 600, 300]):
        assert abs(float(got) - want) < 250
