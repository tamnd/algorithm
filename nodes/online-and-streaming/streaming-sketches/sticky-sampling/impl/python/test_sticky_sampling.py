# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sticky-sampling/. The authors are listed in prov/VTF6WC.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

import pytest

from sticky_sampling import StickySampling


def ideal_start(r: int, k: int) -> list[Fraction]:
    """P(the entry starts at occurrence l), l = 1..k, then P(no entry), when
    each of k occurrences is sampled with probability 1/r."""
    p = Fraction(1, r)
    out = [(1 - p) ** (l - 1) * p for l in range(1, k + 1)]
    return out + [(1 - p) ** k]


def exact_rule_step(dist: list[Fraction], new_r: int) -> list[Fraction]:
    """The start distribution after one change of rate with the exact rule:
    keep with probability 1/2, else move on and try each later occurrence
    with probability 1/new_r."""
    k = len(dist) - 1
    out = [Fraction(0)] * (k + 1)
    out[k] = dist[k]
    q = Fraction(1, new_r)
    for j in range(k):  # the start is occurrence j + 1
        out[j] += dist[j] / 2
        rest = dist[j] / 2
        for l in range(j + 1, k):
            out[l] += rest * q
            rest *= 1 - q
        out[k] += rest
    return out


def paper_rule_step(dist: list[Fraction]) -> list[Fraction]:
    """The start distribution after one change of rate with fair coins."""
    k = len(dist) - 1
    out = [Fraction(0)] * (k + 1)
    out[k] = dist[k]
    for j in range(k):
        rest = dist[j]
        for l in range(j, k):
            out[l] += rest / 2  # heads: stop here
            rest /= 2  # tails: one occurrence less
        out[k] += rest
    return out


def test_exact_rule_gives_the_state_of_the_new_rate() -> None:
    for k in range(1, 9):
        dist = ideal_start(1, k)
        for r in (2, 4, 8, 16):
            dist = exact_rule_step(dist, r)
            assert dist == ideal_start(r, k)


def test_paper_rule_is_exact_only_for_the_first_change() -> None:
    k = 3
    d2 = paper_rule_step(ideal_start(1, k))
    assert d2 == ideal_start(2, k)
    d4 = paper_rule_step(d2)
    assert d4 == [Fraction(1, 4), Fraction(1, 4), Fraction(3, 16), Fraction(5, 16)]
    assert ideal_start(4, k) == [Fraction(1, 4), Fraction(3, 16), Fraction(9, 64), Fraction(27, 64)]


def start_frequencies(paper_rule: bool, trials: int) -> list[float]:
    # t = ln(1/0.45)/0.5 = 1.597, so the rate is 1 for n <= 3, 2 for n <= 6, 4 for n <= 12.
    k = 3
    counts = Counter()
    for seed in range(trials):
        st = StickySampling(0.9, 0.5, 0.5, random.Random(seed), paper_rule=paper_rule)
        st.extend(["x"] * k + [("filler", i) for i in range(4)])
        assert st.r == 4
        counts[st.estimate("x")] += 1
    # estimate f = k - l + 1 for start l, and 0 for no entry
    return [counts[k - l + 1] / trials for l in range(1, k + 1)] + [counts[0] / trials]


def test_implementation_matches_the_ideal_state() -> None:
    trials = 20000
    emp = start_frequencies(False, trials)
    for e, p in zip(emp, ideal_start(4, 3)):
        p = float(p)
        assert abs(e - p) <= 4 * math.sqrt(p * (1 - p) / trials)
    emp_paper = start_frequencies(True, trials)
    assert abs(emp_paper[1] - 0.25) <= 4 * math.sqrt(0.25 * 0.75 / trials)
    assert emp_paper[1] - 3 / 16 > 0.04  # far from the ideal 3/16


def test_rates_and_estimates_never_too_large() -> None:
    rng = random.Random(1)
    st = StickySampling(0.2, 0.1, 0.1, rng)
    t = st.t
    assert math.isclose(t, math.log(50) / 0.1)
    freq = Counter()
    for i in range(int(20 * t)):
        x = rng.randrange(3) if rng.random() < 0.5 else rng.randrange(10**6)
        st.update(x)
        freq[x] += 1
        r = st.r
        assert (r == 1 and st.n <= 2 * t) or (r * t < st.n <= 2 * r * t)
        if i % 97 == 0:
            for y, c in st.f.items():
                assert 1 <= c <= freq[y]


def test_guarantee_failure_rate_at_most_delta() -> None:
    s, eps, delta = 0.1, 0.05, 0.2
    trials = 120
    failures = 0
    for seed in range(trials):
        rng = random.Random(10_000 + seed)
        st = StickySampling(s, eps, delta, rng)
        n = int(12 * st.t)
        freq = Counter()
        for _ in range(n):
            u = rng.random()
            x = int(u / 0.15) if u < 0.6 else rng.randrange(4, 4000)  # 4 items with 15 percent each
            st.update(x)
            freq[x] += 1
        rep = set(st.report())
        heavy = [x for x, c in freq.items() if c >= s * n]
        assert len(heavy) == 4
        bad = any(x not in rep or freq[x] - st.estimate(x) > eps * n for x in heavy)
        bad = bad or any(freq[x] < (s - eps) * n for x in rep)
        failures += bad
    tol = 3 * math.sqrt(delta * (1 - delta) / trials)
    assert failures / trials <= delta + tol


def test_expected_space_at_most_2t_with_the_exact_rule() -> None:
    # Runs of L equal items: 2t = 20, and N = 512 t ends the phase of rate 256.
    s, eps = 0.5, 0.1
    delta = math.exp(-1) / s  # so t = 10
    trials = 40
    totals = {False: 0, True: 0}
    for rule in (False, True):
        for seed in range(trials):
            st = StickySampling(s, eps, delta, random.Random(seed), paper_rule=rule)
            n = int(round(512 * st.t))
            for i in range(n):
                st.update(i // 10)
            assert st.r == 256
            totals[rule] += len(st)
    mean_exact = totals[False] / trials
    mean_paper = totals[True] / trials
    # The number of entries is a sum of independent indicators with mean <= 20,
    # so its variance is at most 20.
    assert mean_exact <= 20 + 3 * math.sqrt(20 / trials)
    assert mean_paper > 30  # the fair-coin rule keeps far more than 2t entries


def test_parameters() -> None:
    rng = random.Random(0)
    with pytest.raises(ValueError):
        StickySampling(0.1, 0.2, 0.1, rng)
    with pytest.raises(ValueError):
        StickySampling(0.1, 0.05, 0, rng)
    st = StickySampling(0.1, 0.05, 0.1, rng)
    assert st.estimate("z") == 0 and st.report() == []
