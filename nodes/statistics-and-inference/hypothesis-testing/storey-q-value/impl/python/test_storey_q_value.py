# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/storey-q-value/. The authors are listed in prov/WKCJWX.jsonl.

import itertools
import random
import statistics
from fractions import Fraction

import pytest

from storey_q_value import pi0_estimate, q_values, sts_reject

BH95 = [0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000]


def q_values_brute_force(p: list, lam) -> list:
    """q_i = min over t in {p_j : p_j >= p_i} of min(1, pi0 m t / #{p_j <= t}), straight from the definition."""
    m = len(p)
    pi0 = min(Fraction(sum(1 for v in p if v > lam), 1) / (m * (1 - lam)), 1)
    return [min(min(Fraction(1), pi0 * m * t / sum(1 for v in p if v <= t)) for t in p if t >= pi) for pi in p]


def sts_brute_force(p: list, alpha, lam) -> list[bool]:
    """Storey-Taylor-Siegmund from the definition: t = sup{0 <= t <= lam : FDR*(t) <= alpha}, reject p_i <= t.

    FDR*(t) = pi0* m t / max(R(t), 1) increases between data points and drops at them, so the supremum is
    0, lam, a p-value, or a point j alpha / (pi0* m) where the ratio reaches alpha with R(t) = j.
    """
    m = len(p)
    pi0 = Fraction(1 + sum(1 for v in p if v > lam), 1) / (m * (1 - lam))
    candidates = {Fraction(0), lam} | {v for v in p if v <= lam}
    candidates |= {j * alpha / (pi0 * m) for j in range(1, m + 1) if j * alpha / (pi0 * m) <= lam}
    best = max(t for t in candidates if pi0 * m * t <= alpha * max(1, sum(1 for v in p if v <= t)))
    return [v <= best for v in p]


def test_worked_example_by_hand() -> None:
    # Four p-values are above 0.5, so pi0_hat = 4 / (15 * 0.5) = 0.5333 and pi0_star = 5 / 7.5 = 0.6667.
    assert pi0_estimate(BH95, 0.5) == pytest.approx(8 / 15)
    assert pi0_estimate(BH95, 0.5, plus_one=True) == pytest.approx(2 / 3)
    q = q_values(BH95, 0.5)
    # q_(9) = 0.5333 * 15 * 0.0459 / 9 = 0.0408, q_(10) = 0.5333 * 15 * 0.3240 / 10 = 0.2592.
    assert q[8] == pytest.approx(8 / 15 * 15 * 0.0459 / 9)
    assert sum(v <= 0.05 for v in q) == 9
    # The STS thresholds are k * 0.05 / (0.6667 * 15) = k * 0.005: 0.0344 <= 0.040 but 0.0459 > 0.045.
    assert sum(sts_reject(BH95, 0.05, 0.5)) == 8
    # With lambda = 0, pi0 = 1 and the q-values are the BH adjusted p-values: 4 below 0.05.
    assert sum(v <= 0.05 for v in q_values(BH95, 0)) == 4


def test_q_values_match_definition() -> None:
    rng = random.Random(2002)
    for _ in range(300):
        m = rng.randint(1, 12)
        p = [Fraction(rng.randint(0, 50), 50) for _ in range(m)]
        lam = Fraction(rng.choice([0, 1, 2, 3]), 4)
        assert q_values(p, lam) == q_values_brute_force(p, lam)


def test_sts_matches_definition() -> None:
    rng = random.Random(2004)
    for _ in range(500):
        m = rng.randint(1, 12)
        p = [Fraction(rng.randint(0, 40), 40) ** rng.choice([1, 2]) for _ in range(m)]
        lam = Fraction(rng.choice([1, 2, 3]), 4)
        alpha = Fraction(rng.randint(1, 8), 20)
        assert sts_reject(p, alpha, lam) == sts_brute_force(p, alpha, lam)


def test_q_value_rule_is_bh_at_alpha_over_pi0() -> None:
    """Rejecting q_i <= alpha is BH at level alpha / pi0_hat (Storey, Taylor and Siegmund 2004, Lemma 2)."""
    rng = random.Random(5)
    for _ in range(300):
        m = rng.randint(1, 12)
        p = [Fraction(rng.randint(0, 60), 60) for _ in range(m)]
        lam = Fraction(1, 2)
        pi0 = pi0_estimate(p, lam)
        alpha = Fraction(rng.randint(1, 6), 20)
        k = max([j for j in range(1, m + 1) if pi0 * m * sorted(p)[j - 1] <= j * alpha] or [0])
        threshold = sorted(p)[k - 1] if k else -1
        assert [v <= alpha for v in q_values(p, lam)] == [v <= threshold for v in p]


def test_invalid_input() -> None:
    assert q_values([], 0.5) == []
    assert sts_reject([], 0.1) == []
    with pytest.raises(ValueError):
        pi0_estimate([0.2], 1)
    with pytest.raises(ValueError):
        sts_reject([0.2], 0)


def test_exact_fdr_on_a_grid() -> None:
    """Null p-values uniform on {1/10, ..., 1}, independent; FDR summed exactly. STS has FDR <= (1 - lam^m0) alpha.

    The grid p-values are valid but not continuous; the leave-one-out proof on the page covers this case.
    """
    grid = [Fraction(k, 10) for k in range(1, 11)]
    lam, alpha = Fraction(1, 2), Fraction(1, 5)
    rng = random.Random(66)
    for m in (2, 3, 4):
        for m0 in range(1, m + 1):
            alt = [Fraction(rng.randint(0, 20), 100) for _ in range(m - m0)]
            total = Fraction(0)
            for nulls in itertools.product(grid, repeat=m0):
                reject = sts_reject(list(nulls) + alt, alpha, lam)
                r = sum(reject)
                if r:
                    total += Fraction(sum(reject[:m0]), r)
            assert total / 10**m0 <= (1 - lam**m0) * alpha


def test_monte_carlo_fdr_and_power() -> None:
    rng = random.Random(9440)
    nd = statistics.NormalDist()
    m, m0, alpha, reps = 40, 20, 0.1, 2000
    fdr = {"sts": 0.0, "q": 0.0, "bh": 0.0}
    power = dict.fromkeys(fdr, 0.0)
    for _ in range(reps):
        p = [nd.cdf(-(rng.gauss(0, 1) + (3.0 if i >= m0 else 0.0))) for i in range(m)]
        rules = {"sts": sts_reject(p, alpha), "q": [v <= alpha for v in q_values(p)], "bh": [v <= alpha for v in q_values(p, 0)]}
        for name, reject in rules.items():
            r = sum(reject)
            fdr[name] += sum(reject[:m0]) / r if r else 0.0
            power[name] += sum(reject[m0:]) / (m - m0)
    fdr = {k: v / reps for k, v in fdr.items()}
    power = {k: v / reps for k, v in power.items()}
    # BH has FDR exactly (m0/m) alpha = 0.05; STS is proved to be at most alpha = 0.1. Four standard errors < 0.02.
    assert abs(fdr["bh"] - 0.05) < 0.02
    assert fdr["sts"] <= 0.1 + 0.02
    # The plain q-value rule has no finite-sample guarantee. With this seed it measures 0.112, above alpha;
    # the standard error is 0.0018. It is only asymptotically valid.
    assert 0.1 < fdr["q"] < 0.13
    assert power["sts"] > power["bh"] and power["q"] > power["bh"]
