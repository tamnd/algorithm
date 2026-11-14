# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instrumental-variables-estimation/. The authors are listed in prov/CM6TM9.jsonl.

import math
import random
import statistics
from fractions import Fraction as Fr

import pytest

from instrumental_variables_estimation import (
    ar_pvalue,
    ar_set,
    ar_statistic,
    in_set,
    iv_analysis,
    moments,
    wald_estimate,
    wald_interval,
)
from stdist import f_ppf


def test_worked_example():
    z = [0, 0, 0, 0, 1, 1, 1, 1]
    d = [0, 0, 0, 1, 1, 1, 1, 0]
    y = [1, 2, 3, 6, 5, 6, 4, 2]
    yf, df, zf = ([Fr(v) for v in a] for a in (y, d, z))
    r = iv_analysis(yf, df, zf)
    assert r.beta == Fr(5, 2) == wald_estimate(yf, df, zf)
    assert r.alpha == Fr(19, 8)
    assert r.first_stage_f == Fr(2)
    m = moments(yf, df, zf)
    assert ar_statistic(m, Fr(5, 2)) == 0
    assert ar_statistic(m, 0) == Fr(75, 91)
    assert r.ar_set == ("line",)  # F = 2 is below F(1, 6, 0.95) = 5.99: the set is unbounded
    kind, lo, hi = ar_set(m, 0.30)  # F(1, 6, 0.70) = 1.27 < 2: bounded
    assert kind == "interval" and abs(lo + 2.5129) < 1e-4 and abs(hi - 3.9082) < 1e-4


def test_wald_equals_covariance_ratio_exactly():
    rng = random.Random(1)
    done = 0
    while done < 300:
        n = rng.randint(4, 15)
        z = [Fr(rng.randint(0, 1)) for _ in range(n)]
        d = [Fr(rng.randint(0, 3)) for _ in range(n)]
        y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        try:
            w = wald_estimate(y, d, z)
        except (ValueError, ZeroDivisionError):
            continue
        m = moments(y, d, z)
        assert w == m.szy / m.szd == iv_analysis(y, d, z).beta
        done += 1


def test_ar_set_matches_grid_inversion():
    """The closed-form set agrees with testing every grid point, away from its boundary."""
    rng = random.Random(2)
    kinds = set()
    for trial in range(150):
        n = rng.randint(8, 40)
        pi = rng.choice([0.0, 0.1, 0.3, 1.0, 3.0])
        z = [rng.gauss(0, 1) for _ in range(n)]
        d = [pi * a + rng.gauss(0, 1) for a in z]
        y = [0.5 * b + rng.gauss(0, 1) for b in d]
        m = moments(y, d, z)
        s = ar_set(m, 0.05)
        kinds.add(s[0])
        q = f_ppf(0.95, 1, n - 2)
        ends = [v for v in s[1:]]
        for i in range(-400, 401):
            b0 = i / 20
            if any(abs(b0 - e) < 1e-6 for e in ends):
                continue
            assert (ar_statistic(m, b0) <= q) == in_set(s, b0)
    assert {"interval", "complement", "line"} <= kinds


def test_ar_set_is_bounded_iff_the_first_stage_rejects():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(6, 30)
        pi = rng.choice([0.0, 0.2, 0.5, 2.0])
        z = [rng.gauss(0, 1) for _ in range(n)]
        d = [pi * a + rng.gauss(0, 1) for a in z]
        y = [b + rng.gauss(0, 1) for b in d]
        r = iv_analysis(y, d, z)
        q = f_ppf(0.95, 1, n - 2)
        if abs(r.first_stage_f - q) < 1e-9:
            continue
        assert (r.ar_set[0] == "interval") == (r.first_stage_f > q)
        if r.ar_set[0] == "interval":
            assert r.ar_set[1] <= r.beta <= r.ar_set[2]


def weak_sample(rng, n, pi, rho, beta=1.0):
    z = [rng.gauss(0, 1) for _ in range(n)]
    e = [rng.gauss(0, 1) for _ in range(n)]
    v = [rho * a + math.sqrt(1 - rho * rho) * rng.gauss(0, 1) for a in e]
    d = [pi * a + b for a, b in zip(z, v)]
    y = [beta * a + b for a, b in zip(d, e)]
    return y, d, z


def test_ar_size_under_a_weak_instrument():
    """n = 50, first-stage coefficient 0.05, corr(e, v) = 0.8, r = 2000 (seed 2026). The AR test is exact,
    so its rejection rate is within 0.05 +- 4 SE (SE = 0.0049). The Wald t test is not: it rejects in more
    than 9% of the samples (0.05 + 8 SE; the measured rate is 0.121)."""
    rng = random.Random(2026)
    r, ar_rej, t_rej = 2000, 0, 0
    q = f_ppf(0.95, 1, 48)
    for _ in range(r):
        y, d, z = weak_sample(rng, 50, 0.05, 0.8)
        m = moments(y, d, z)
        ar_rej += ar_statistic(m, 1.0) > q
        res = iv_analysis(y, d, z, alpha=0.05)
        t_rej += abs(res.beta - 1.0) > math.sqrt(q) * res.se  # sqrt(F(1, 48)) is the t(48) critical value
    se = math.sqrt(0.05 * 0.95 / r)
    assert abs(ar_rej / r - 0.05) < 4 * se
    assert t_rej / r > 0.09
    lo, hi = wald_interval(res, 50)
    assert abs(hi - lo - 2 * math.sqrt(q) * res.se) < 1e-9


def test_iv_consistent_where_ols_is_biased():
    """Strong instrument (coefficient 1), corr(e, v) = 0.5, n = 400, r = 300 (seed 5). OLS tends to
    1 + 0.5/2 = 1.25. IV has no finite mean with one instrument, so the median is checked: within
    4 SE + 0.01 of 1, with SE = 1.2533 SD / sqrt(r)."""
    rng = random.Random(5)
    iv, ols = [], []
    for _ in range(300):
        y, d, z = weak_sample(rng, 400, 1.0, 0.5)
        iv.append(iv_analysis(y, d, z).beta)
        m = moments(y, d, z)
        ols.append(m.syd / m.sdd)
    se = 1.2533 * statistics.stdev(iv) / math.sqrt(300)
    assert abs(statistics.median(iv) - 1) < 4 * se + 0.01
    assert abs(statistics.mean(ols) - 1.25) < 0.02


def test_input_checks():
    with pytest.raises(ValueError):
        wald_estimate([1, 2], [0, 1], [2, 0])
    with pytest.raises(ZeroDivisionError):
        wald_estimate([1, 2, 3, 4], [1, 0, 1, 0], [0, 0, 1, 1])
    with pytest.raises(ValueError):
        iv_analysis([1, 2, 3], [1, 2, 3], [1, 1, 1])
