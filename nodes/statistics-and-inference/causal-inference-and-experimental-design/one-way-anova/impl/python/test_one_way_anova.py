# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-way-anova/. The authors are listed in prov/QHQ1W6.jsonl.

import math
import random
from fractions import Fraction

import pytest

from one_way_anova import one_way_anova, welch_anova
from stdist import f_ppf, t_sf

EXAMPLE = [[5, 7, 6, 8], [9, 11, 10, 12, 8], [6, 8, 7, 5, 9, 7]]


def exact_sums(groups: list[list[int]]) -> tuple[Fraction, Fraction, Fraction]:
    """SSB, SSW and SST from their definitions, in exact arithmetic."""
    big_n = sum(len(g) for g in groups)
    grand = Fraction(sum(sum(g) for g in groups), big_n)
    means = [Fraction(sum(g), len(g)) for g in groups]
    ssb = sum(len(g) * (m - grand) ** 2 for g, m in zip(groups, means))
    ssw = sum((v - m) ** 2 for g, m in zip(groups, means) for v in g)
    sst = sum((v - grand) ** 2 for g in groups for v in g)
    return ssb, ssw, sst


def test_example() -> None:
    r = one_way_anova(EXAMPLE)
    ssb, ssw, sst = exact_sums(EXAMPLE)
    assert (ssb, ssw, sst) == (Fraction(521, 15), Fraction(25), Fraction(896, 15))
    assert ssb + ssw == sst
    assert (r.df1, r.df2) == (2, 12)
    assert r.means == [6.5, 10.0, 7.0]
    assert abs(r.ssb - 521 / 15) < 1e-12 and abs(r.ssw - 25.0) < 1e-12
    assert abs(r.f - 1042 / 125) < 1e-12
    assert abs(r.p - 0.005374518329892695) < 1e-12
    assert r.f > f_ppf(0.95, 2, 12)


def test_decomposition_against_fractions() -> None:
    rng = random.Random(1)
    for _ in range(200):
        k = rng.randint(2, 6)
        groups = [[rng.randint(-50, 50) for _ in range(rng.randint(1, 7))] for _ in range(k)]
        if sum(len(g) for g in groups) <= k:
            continue
        ssb, ssw, sst = exact_sums(groups)
        assert ssb + ssw == sst
        if ssw == 0:
            continue
        r = one_way_anova(groups)
        df2 = sum(len(g) for g in groups) - k
        f = (ssb / (k - 1)) / (ssw / df2)
        assert abs(r.ssb - float(ssb)) <= 1e-9 * max(1.0, float(sst))
        assert abs(r.ssw - float(ssw)) <= 1e-9 * max(1.0, float(sst))
        assert abs(r.f - float(f)) <= 1e-9 * max(1.0, float(f))


def test_two_groups_f_is_t_squared() -> None:
    rng = random.Random(2)
    for _ in range(100):
        x = [rng.randint(0, 30) for _ in range(rng.randint(1, 8))]
        y = [rng.randint(0, 30) for _ in range(rng.randint(2, 8))]
        mx, my = Fraction(sum(x), len(x)), Fraction(sum(y), len(y))
        ss = sum((v - mx) ** 2 for v in x) + sum((v - my) ** 2 for v in y)
        if ss == 0:
            continue
        sp2 = ss / (len(x) + len(y) - 2)
        t2 = (mx - my) ** 2 / (sp2 * (Fraction(1, len(x)) + Fraction(1, len(y))))
        assert exact_sums([x, y])[0] / (sp2) == t2  # SSB / MSE = t^2, exactly
        r = one_way_anova([x, y])
        assert abs(r.f - float(t2)) <= 1e-10 * max(1.0, float(t2))
        assert abs(r.p - 2.0 * t_sf(math.sqrt(r.f), len(x) + len(y) - 2)) < 1e-12


def test_shift_does_not_cancel() -> None:
    shifted = [[1e9 + v for v in g] for g in EXAMPLE]
    assert abs(one_way_anova(shifted).f - 8.336) < 1e-6


def test_size_under_the_null() -> None:
    rng = random.Random(3)
    reps, alpha = 3000, 0.05
    rej = sum(one_way_anova([[rng.gauss(0.0, 1.0) for _ in range(n)] for n in (4, 6, 9)]).p <= alpha
              for _ in range(reps))
    se = math.sqrt(alpha * (1 - alpha) / reps)
    assert abs(rej / reps - alpha) < 4.0 * se


def test_welch_two_groups_is_welch_t_squared() -> None:
    rng = random.Random(4)
    for _ in range(50):
        x = [rng.gauss(0.0, 1.0) for _ in range(rng.randint(2, 9))]
        y = [rng.gauss(0.5, 3.0) for _ in range(rng.randint(2, 9))]
        mx, my = sum(x) / len(x), sum(y) / len(y)
        a = sum((v - mx) ** 2 for v in x) / (len(x) - 1) / len(x)
        b = sum((v - my) ** 2 for v in y) / (len(y) - 1) / len(y)
        t2 = (mx - my) ** 2 / (a + b)
        df = (a + b) ** 2 / (a * a / (len(x) - 1) + b * b / (len(y) - 1))
        f, df1, df2, p = welch_anova([x, y])
        assert df1 == 1
        assert abs(f - t2) <= 1e-10 * t2 and abs(df2 - df) <= 1e-10 * df
        assert abs(p - 2.0 * t_sf(math.sqrt(t2), df)) < 1e-12


def test_welch_example() -> None:
    f, df1, df2, p = welch_anova(EXAMPLE)
    assert df1 == 2
    assert abs(f - 7.110393149302828) < 1e-9
    assert abs(df2 - 7.490339568443729) < 1e-9
    assert abs(p - 0.01858036702427885) < 1e-9


def test_errors() -> None:
    with pytest.raises(ValueError):
        one_way_anova([[1.0, 2.0]])
    with pytest.raises(ValueError):
        one_way_anova([[1.0], [2.0]])
    with pytest.raises(ValueError):
        one_way_anova([[1.0, 1.0], [2.0, 2.0]])
