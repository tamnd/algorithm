# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harrell-c-index/. The authors are listed in prov/JWHWF0.jsonl.

import math
import random
from fractions import Fraction

import pytest

from harrell_c_index import censoring_survival, harrell_c, uno_c


def direct_counts(times, events, risk, weight=None, strict=False):
    """O(n^2): every ordered pair (i, j) with i an event and j known to outlast i."""
    n = len(times)
    weight = weight or [1] * n
    conc = disc = tied = comp = 0
    for i in range(n):
        if not events[i] or not weight[i]:
            continue
        for j in range(n):
            later = times[j] > times[i] or (not strict and times[j] == times[i] and not events[j])
            if j == i or not later:
                continue
            w = weight[i]
            comp += w
            if risk[i] > risk[j]:
                conc += w
            elif risk[i] < risk[j]:
                disc += w
            else:
                tied += w
    return conc, disc, tied, comp


def random_data(rng, n, tmax, rmax, pcens):
    times = [rng.randint(1, tmax) for _ in range(n)]
    events = [0 if rng.random() < pcens else 1 for _ in range(n)]
    risk = [rng.randint(0, rmax) for _ in range(n)]
    return times, events, risk


def test_hand_example() -> None:
    # Times 2, 3+, 5, 7+, 8 with risk scores 0.9, 0.5, 0.6, 0.1, 0.3. The comparable pairs are
    # (2,3+), (2,5), (2,7+), (2,8), (5,7+), (5,8): six pairs. The pair (5,7+) has 0.6 > 0.1 and
    # (5,8) has 0.6 > 0.3, and subject 1 has the highest risk, so all six agree: C = 1.
    res = harrell_c([2, 3, 5, 7, 8], [1, 0, 1, 0, 1], [0.9, 0.5, 0.6, 0.1, 0.3], exact=True)
    assert (res.concordant, res.discordant, res.tied_risk, res.comparable) == (6, 0, 0, 6)
    # Swap the scores of the subjects at 5 and 8: (5,7+) still agrees (0.3 > 0.1), (5,8) now
    # disagrees, so C = 5/6. Censored 3+ and 7+ are never the earlier member of a pair.
    res = harrell_c([2, 3, 5, 7, 8], [1, 0, 1, 0, 1], [0.9, 0.5, 0.3, 0.1, 0.6], exact=True)
    assert (res.concordant, res.discordant, res.comparable) == (5, 1, 6) and res.c_index == Fraction(5, 6)


def test_fenwick_count_matches_all_pairs() -> None:
    rng = random.Random(1982)
    for _ in range(300):
        times, events, risk = random_data(rng, rng.randint(1, 40), rng.randint(1, 10), rng.randint(0, 6), 0.4)
        conc, disc, tied, comp = direct_counts(times, events, risk)
        if comp == 0:
            with pytest.raises(ValueError):
                harrell_c(times, events, risk)
            continue
        res = harrell_c(times, events, risk, exact=True)
        assert (res.concordant, res.discordant, res.tied_risk, res.comparable) == (conc, disc, tied, comp)
        assert res.c_index == Fraction(2 * conc + tied, 2 * comp)
        assert math.isclose(harrell_c(times, events, risk).c_index, float(res.c_index), rel_tol=1e-12)


def test_binary_outcome_is_the_auc() -> None:
    # No censoring and two possible times: the comparable pairs are (case, control) pairs, and C is
    # the Mann-Whitney estimate of P(risk_case > risk_control) + P(tie)/2, the area under the ROC curve.
    rng = random.Random(1947)
    for _ in range(100):
        n = rng.randint(2, 30)
        times = [rng.choice([1, 2]) for _ in range(n)]
        times[0], times[1] = 1, 2
        risk = [rng.randint(0, 8) for _ in range(n)]
        cases = [r for r, t in zip(risk, times) if t == 1]
        controls = [r for r, t in zip(risk, times) if t == 2]
        u = sum(Fraction(1) if a > b else Fraction(1, 2) if a == b else 0 for a in cases for b in controls)
        assert harrell_c(times, [1] * n, risk, exact=True).c_index == u / (len(cases) * len(controls))


def test_without_censoring_or_ties_it_is_a_kendall_tau() -> None:
    # Every pair is comparable and C = (1 - tau)/2, with tau Kendall's tau between risk and time.
    rng = random.Random(1938)
    for _ in range(100):
        n = rng.randint(2, 40)
        times = rng.sample(range(1000), n)
        risk = rng.sample(range(1000), n)
        s = sum((1 if (times[i] - times[j]) * (risk[i] - risk[j]) > 0 else -1) for i in range(n) for j in range(i))
        tau = Fraction(s, n * (n - 1) // 2)
        res = harrell_c(times, [1] * n, risk, exact=True)
        assert res.comparable == n * (n - 1) // 2
        assert res.c_index == (1 - tau) / 2


def test_invariances() -> None:
    rng = random.Random(3)
    for _ in range(100):
        times, events, risk = random_data(rng, 25, 12, 1000, 0.3)
        try:
            base = harrell_c(times, events, risk, exact=True)
        except ValueError:
            continue
        assert harrell_c(times, events, [math.exp(r / 100) for r in risk], exact=True) == base
        rev = harrell_c(times, events, [-r for r in risk], exact=True)
        assert rev.concordant == base.discordant and rev.c_index == 1 - base.c_index
        assert harrell_c(times, events, [7] * len(times), exact=True).c_index == Fraction(1, 2)


def test_uno_matches_the_weighted_pair_sum() -> None:
    rng = random.Random(2011)
    for _ in range(200):
        times, events, risk = random_data(rng, rng.randint(2, 40), rng.randint(2, 12), 5, 0.4)
        g = censoring_survival(times, events)
        for tau in (math.inf, 6):
            weight = [1 / g[i] ** 2 if events[i] and times[i] < tau and g[i] > 0 else 0 for i in range(len(times))]
            conc, disc, tied, comp = direct_counts(times, events, risk, weight, strict=True)
            if comp == 0:
                continue
            res = uno_c(times, events, risk, tau)
            assert math.isclose(res.comparable, comp, rel_tol=1e-12)
            assert math.isclose(res.c_index, (conc + tied / 2) / comp, rel_tol=1e-12)


def test_censoring_survival_and_no_censoring() -> None:
    # G(t-) for the censoring times 3+ and 7+ in 2, 3+, 5, 7+, 8: 1 up to 3, then 1 - 1/4 = 3/4
    # after 3+ (four at risk at 3), then 3/4 (1 - 1/2) = 3/8 after 7+ (two at risk at 7).
    g = censoring_survival([2, 3, 5, 7, 8], [1, 0, 1, 0, 1])
    assert g == [1.0, 1.0, 0.75, 0.75, 0.375]
    rng = random.Random(9)
    for _ in range(50):
        n = rng.randint(2, 30)
        times = rng.sample(range(100), n)
        risk = [rng.random() for _ in range(n)]
        assert math.isclose(uno_c(times, [1] * n, risk).c_index, harrell_c(times, [1] * n, risk).c_index, rel_tol=1e-12)


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        harrell_c([], [], [])
    with pytest.raises(ValueError):
        harrell_c([1, 2], [1, 2], [0, 1])
    with pytest.raises(ValueError):
        harrell_c([1, 2], [0, 0], [0, 1])
    with pytest.raises(ValueError):
        uno_c([1, 2], [1, 1], [0, 1], tau=1)
