# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimized-local-hashing/. The authors are listed in prov/4AE9P1.jsonl.

import math
import random
from fractions import Fraction

import pytest

import dpkit
from optimized_local_hashing import (
    AllFunctions,
    approximate_variance,
    keep_probability,
    olh_estimate,
    olh_report,
    optimal_range,
    report_pmf,
    variance_formula,
)

F = Fraction


def test_check_values():
    assert optimal_range(3) == 4
    assert keep_probability(3, 4) == F(1, 2)
    assert approximate_variance(1, 3, 4) == 3
    # Var*/n = 4 e^epsilon / (e^epsilon - 1)^2 at g = e^epsilon + 1.
    for e in (2, 3, 5, 9):
        assert approximate_variance(1, e, e + 1) == F(4 * e, (e - 1) ** 2)
    # Direct encoding over d = 1024 values at e^epsilon = 3 has Var*/n = (d - 2 + e) / (e - 1)^2.
    assert abs(math.sqrt(10000 * 3) - 173.2) < 0.1
    assert abs(math.sqrt(10000 * (1024 - 2 + 3) / 4) - 1600.8) < 0.1
    fam = AllFunctions(d=3, g=4)
    assert [fam.hash(27, v) for v in range(3)] == [3, 2, 1]


def test_bad_input():
    with pytest.raises(ValueError):
        AllFunctions(d=3, g=1)
    with pytest.raises(ValueError):
        olh_report(3, F(3), AllFunctions(d=3, g=4), random.Random(0))
    with pytest.raises(ValueError):
        olh_estimate([(0, 0)], F(1), AllFunctions(d=3, g=4))


def test_report_is_exactly_epsilon_ldp():
    for e, g, d in ((F(3), 4, 3), (F(2), 3, 3), (F(5, 2), 2, 4)):
        fam = AllFunctions(d=d, g=g)
        pairs = [((a,), (b,)) for a in range(d) for b in range(d) if a != b]
        mech = lambda x: report_pmf(x[0], e, fam)
        assert dpkit.is_pure_dp(mech, pairs, math.log(e))
        assert not dpkit.is_pure_dp(mech, pairs, math.log(e) - 0.01)


def test_family_is_pairwise_uniform():
    fam = AllFunctions(d=3, g=3)
    for a in range(3):
        for b in range(3):
            if a != b:
                pairs = [(fam.hash(s, a), fam.hash(s, b)) for s in range(fam.seeds)]
                assert all(pairs.count((x, y)) == fam.seeds // 9 for x in range(3) for y in range(3))


def exact_moments(data, v, e, fam):
    """Independent oracle: the exact mean and variance of the estimate, from each report's pmf."""
    g = fam.g
    p = keep_probability(e, g)
    mean_c = F(0)
    var_c = F(0)
    for u in data:
        hit = sum(pr for (s, y), pr in report_pmf(u, e, fam).items() if fam.hash(s, v) == y)
        mean_c += hit
        var_c += hit * (1 - hit)
    n = len(data)
    scale = p - F(1, g)
    return (mean_c - F(n, g)) / scale, var_c / scale ** 2


def test_estimate_is_unbiased_with_the_stated_variance():
    rng = random.Random(4)
    fam_cache = {}
    for _ in range(500):
        d = rng.randint(2, 3)
        g = rng.randint(2, 3)
        e = F(rng.randint(5, 40), 4)
        fam = fam_cache.setdefault((d, g), AllFunctions(d=d, g=g))
        n = rng.randint(1, 50)
        data = [rng.randrange(d) for _ in range(n)]
        v = rng.randrange(d)
        mean, var = exact_moments(data, v, e, fam)
        assert mean == data.count(v)
        assert var == variance_formula(n, data.count(v), e, g)


def test_optimal_range_minimizes_approximate_variance():
    rng = random.Random(6)
    cases = [F(2), F(3), F(7), F(15), F(49, 20)]
    cases += [F(rng.randint(41, 2000), 40) for _ in range(500)]
    for e in cases:
        values = {g: approximate_variance(1, e, g) for g in range(2, 60)}
        best = min(values.values())
        assert values[optimal_range(e)] == best
    # Rounding e^epsilon + 1 is not always best: at e^epsilon = 2.45, g = 4 beats g = 3.
    assert optimal_range(F(49, 20)) == 4
    assert approximate_variance(1, F(49, 20), 4) < approximate_variance(1, F(49, 20), 3)


def test_monte_carlo_report_law_and_estimate():
    rng = random.Random(8)
    e = F(3)
    fam = AllFunctions(d=2, g=4)
    n = 2000
    samples = [olh_report(1, e, fam, rng) for _ in range(n)]
    emp = dpkit.empirical_pmf(samples)
    exact = report_pmf(1, e, fam)
    margin = dpkit.hoeffding_margin(n, 1e-6 / len(exact))
    for r, pr in exact.items():
        assert abs(emp.get(r, 0.0) - float(pr)) <= margin
    fam8 = AllFunctions(d=8, g=4)
    data = [0] * 1000 + [3] * 600 + [5] * 400
    reports = [olh_report(v, e, fam8, rng) for v in data]
    est = olh_estimate(reports, e, fam8)
    sd = math.sqrt(approximate_variance(len(data), e, 4))
    truth = [data.count(v) for v in range(8)]
    for got, want in zip(est, truth):
        assert abs(float(got) - want) < 5 * sd
