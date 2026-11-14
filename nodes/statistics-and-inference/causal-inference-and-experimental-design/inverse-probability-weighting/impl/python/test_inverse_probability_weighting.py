# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-probability-weighting/. The authors are listed in prov/GVS3R2.jsonl.

import itertools
import math
import random
from fractions import Fraction as Fr

import pytest

from inverse_probability_weighting import empirical_propensity, ipw_ate, ipw_att, ipw_interval, ipw_variance

# The worked example of the page: x is the stratum, e the known design propensity.
EX_X = [0, 0, 0, 0, 0, 1, 1, 1]
EX_T = [1, 1, 0, 0, 0, 1, 1, 0]
EX_Y = [8, 7, 6, 5, 7, 4, 3, 1]
EX_E = [Fr(1, 4)] * 5 + [Fr(3, 4)] * 3


def stratified(x, t, y, weight="all"):
    """Oracle: the subclassification estimate, sum over strata of (share) times (mean difference)."""
    out, total = Fr(0), 0
    for v in sorted(set(x)):
        idx = [i for i in range(len(x)) if x[i] == v]
        tr = [y[i] for i in idx if t[i] == 1]
        co = [y[i] for i in idx if t[i] == 0]
        size = len(idx) if weight == "all" else len(tr)
        out += size * (Fr(sum(tr), len(tr)) - Fr(sum(co), len(co)))
        total += size
    return out / total


def test_worked_example():
    est = ipw_ate(EX_T, EX_Y, EX_E)
    assert est.mu1_ht == Fr(26, 3) and est.mu0_ht == Fr(7, 2)
    assert est.ht == Fr(31, 6)
    assert est.mu1_hajek == Fr(13, 2) and est.mu0_hajek == Fr(7, 2)
    assert est.hajek == 3
    eh = empirical_propensity(EX_X, EX_T)
    assert eh == [Fr(2, 5)] * 5 + [Fr(2, 3)] * 3
    emp = ipw_ate(EX_T, EX_Y, eh)
    assert emp.ht == emp.hajek == Fr(15, 8) == stratified(EX_X, EX_T, EX_Y)
    assert ipw_att(EX_T, EX_Y, eh) == 2 == stratified(EX_X, EX_T, EX_Y, "treated")
    # the naive difference of means
    assert Fr(8 + 7 + 4 + 3, 4) - Fr(6 + 5 + 7 + 1, 4) == Fr(3, 4)


def test_positivity_and_shape_errors():
    with pytest.raises(ValueError):
        ipw_ate([1, 0], [1, 2], [Fr(1, 2), 1])
    with pytest.raises(ValueError):
        ipw_ate([1, 0], [1, 2], [0, Fr(1, 2)])
    with pytest.raises(ValueError):
        ipw_ate([1, 2], [1, 2], [Fr(1, 2), Fr(1, 2)])
    with pytest.raises(ValueError):
        ipw_ate([], [], [])
    with pytest.raises(ValueError):
        ipw_att([0, 0], [1, 2], [Fr(1, 2), Fr(1, 2)])
    one_arm = ipw_ate([1, 1], [3, 5], [Fr(1, 2), Fr(1, 4)])
    assert one_arm.hajek is None and one_arm.ht == Fr(3 * 2 + 5 * 4, 2)


def bernoulli_design(pi):
    """Every assignment vector with its probability under independent Bernoulli(pi_i) assignment."""
    for t in itertools.product((0, 1), repeat=len(pi)):
        p = Fr(1)
        for ti, q in zip(t, pi):
            p *= q if ti else 1 - q
        yield t, p


def test_ht_unbiased_and_variance_exact_bernoulli():
    rng = random.Random(20261114)
    for _ in range(60):
        n = rng.randint(1, 7)
        y0 = [rng.randint(-5, 9) for _ in range(n)]
        y1 = [rng.randint(-5, 9) for _ in range(n)]
        pi = [Fr(rng.randint(1, 9), 10) for _ in range(n)]
        sate = Fr(sum(y1) - sum(y0), n)
        mean = var2 = Fr(0)
        for t, p in bernoulli_design(pi):
            y = [y1[i] if t[i] else y0[i] for i in range(n)]
            tau = ipw_ate(t, y, pi).ht
            mean += p * tau
            var2 += p * tau * tau
        assert mean == sate
        var = var2 - mean * mean
        closed = sum(a * a * (1 - q) / q + b * b * q / (1 - q) + 2 * a * b for a, b, q in zip(y1, y0, pi)) / (n * n)
        assert var == closed


def test_complete_randomization_forms_agree_and_unbiased():
    rng = random.Random(7)
    for _ in range(40):
        n = rng.randint(2, 8)
        n1 = rng.randint(1, n - 1)
        y0 = [Fr(rng.randint(0, 20), 2) for _ in range(n)]
        y1 = [Fr(rng.randint(0, 20), 2) for _ in range(n)]
        e = [Fr(n1, n)] * n
        total, count = Fr(0), 0
        for treated in itertools.combinations(range(n), n1):
            t = [1 if i in treated else 0 for i in range(n)]
            y = [y1[i] if t[i] else y0[i] for i in range(n)]
            est = ipw_ate(t, y, e)
            dm = sum(y1[i] for i in treated) / n1 - sum(y0[i] for i in range(n) if i not in treated) / (n - n1)
            assert est.ht == est.hajek == dm
            total += est.ht
            count += 1
        assert total / count == (sum(y1) - sum(y0)) / n


def test_unequal_marginals_fixed_size_design_unbiased():
    """A design that is not Bernoulli: draw the treated set from a list of sets with given probabilities."""
    rng = random.Random(99)
    for _ in range(40):
        n = rng.randint(3, 6)
        sets = [s for k in range(1, n) for s in itertools.combinations(range(n), k)]
        w = [rng.randint(1, 5) for _ in sets]
        design = {s: Fr(wi, sum(w)) for s, wi in zip(sets, w)}
        pi = [sum((p for s, p in design.items() if i in s), Fr(0)) for i in range(n)]
        if any(q in (0, 1) for q in pi):
            continue
        y0 = [rng.randint(0, 9) for _ in range(n)]
        y1 = [rng.randint(0, 9) for _ in range(n)]
        mean = Fr(0)
        for s, p in design.items():
            t = [1 if i in s else 0 for i in range(n)]
            y = [y1[i] if t[i] else y0[i] for i in range(n)]
            mean += p * ipw_ate(t, y, pi).ht
        assert mean == Fr(sum(y1) - sum(y0), n)


def test_discrete_x_empirical_propensity_equals_stratified():
    rng = random.Random(31)
    done = 0
    while done < 500:
        n = rng.randint(4, 30)
        k = rng.randint(1, 4)
        x = [rng.randrange(k) for _ in range(n)]
        t = [rng.randint(0, 1) for _ in range(n)]
        if any(len({t[i] for i in range(n) if x[i] == v}) < 2 for v in set(x)):
            continue
        y = [Fr(rng.randint(-40, 40), rng.randint(1, 4)) for _ in range(n)]
        eh = empirical_propensity(x, t)
        est = ipw_ate(t, y, eh)
        s = stratified(x, t, y)
        assert est.ht == s and est.hajek == s
        assert ipw_att(t, y, eh) == stratified(x, t, y, "treated")
        done += 1


def test_variance_ht_is_sample_variance_of_psi():
    t, y, e = EX_T, EX_Y, EX_E
    psi = [Fr(ti * yi) / ei - Fr((1 - ti) * yi) / (1 - ei) for ti, yi, ei in zip(t, y, e)]
    m = sum(psi) / len(psi)
    s2 = sum((p - m) ** 2 for p in psi) / (len(psi) - 1)
    v_ht, v_h = ipw_variance(t, y, e)
    assert v_ht == s2 / len(psi)
    assert v_h > 0


def simulate(rng, n):
    """A superpopulation with a known propensity; the true ATE is 1."""
    t, y, e = [], [], []
    for _ in range(n):
        x = rng.random()
        ei = 0.2 + 0.6 * x
        ti = 1 if rng.random() < ei else 0
        y0 = 2 * x + rng.gauss(0, 1)
        y1 = y0 + 0.5 + x  # effect 0.5 + x, mean 1
        t.append(ti)
        y.append(y1 if ti else y0)
        e.append(ei)
    return t, y, e


def test_monte_carlo_bias_and_coverage():
    rng = random.Random(123)
    r, n = 600, 200
    cover = {"ht": 0, "hajek": 0}
    s_ht = s_h = 0.0
    for _ in range(r):
        t, y, e = simulate(rng, n)
        est = ipw_ate(t, y, e)
        s_ht += est.ht
        s_h += est.hajek
        for form in cover:
            lo, hi = ipw_interval(t, y, e, 0.05, form)
            cover[form] += lo <= 1.0 <= hi
    # the HT form is unbiased; the Hajek form has bias of order 1/n
    assert abs(s_ht / r - 1.0) < 0.06
    assert abs(s_h / r - 1.0) < 0.06
    tol = 4 * math.sqrt(0.05 * 0.95 / r) + 0.01
    for form in cover:
        assert abs(cover[form] / r - 0.95) < tol, (form, cover[form] / r)


def test_float_inputs_match_fractions():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(2, 12)
        t = [rng.randint(0, 1) for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        e = [Fr(rng.randint(1, 19), 20) for _ in range(n)]
        a = ipw_ate(t, y, e)
        b = ipw_ate(t, [float(v) for v in y], [float(v) for v in e])
        assert math.isclose(float(a.ht), b.ht, rel_tol=1e-12, abs_tol=1e-12)
        if a.hajek is not None:
            assert math.isclose(float(a.hajek), b.hajek, rel_tol=1e-12, abs_tol=1e-12)
