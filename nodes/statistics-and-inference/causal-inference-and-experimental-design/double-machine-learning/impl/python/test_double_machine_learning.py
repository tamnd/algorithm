# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-machine-learning/. The authors are listed in prov/AN6TYE.jsonl.

import math
import random
import statistics
from fractions import Fraction as Fr

import pytest

from double_machine_learning import (
    binned_learner,
    dml_ate,
    dml_plr,
    linear_learner,
    make_folds,
    oracle_learner,
    solve,
)


def aipw(x, t, y, e, m1, m0):
    n = len(t)
    return sum(m1(v) - m0(v) + (yi - m1(v)) / e(v) if ti == 1 else m1(v) - m0(v) - (yi - m0(v)) / (1 - e(v)) for v, ti, yi in zip(x, t, y)) / n


def test_oracle_learners_give_aipw_exactly():
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(6, 15)
        x = [Fr(rng.randint(0, 9), 9) for _ in range(n)]
        t = [i % 2 for i in range(n)]  # at least 3 units per arm, so no training set lacks an arm
        y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        e = lambda v: Fr(1, 5) + Fr(3, 5) * v
        m1 = lambda v: 2 + 3 * v
        m0 = lambda v: v * v
        target = aipw(x, t, y, e, m1, m0)
        for k in (1, 2, 3):
            # oracle learners ignore their training data, so the folds do not matter
            assert dml_ate_oracle(x, t, y, e, m1, m0, k).estimate == target


def dml_ate_oracle(x, t, y, e, m1, m0, k):
    """Outcome learner that returns m1 on treated training data and m0 on control data (told apart by a tag)."""
    tagged_x = [(v, ti) for v, ti in zip(x, t)]

    def outcome(xs, ys):
        arm = xs[0][1]
        f = m1 if arm == 1 else m0
        return lambda p: f(p[0])

    def prop(xs, ts):
        return lambda p: e(p[0])

    return dml_ate(tagged_x, t, y, outcome, prop, k=k, rng=random.Random(k))


def test_plr_without_cross_fitting_is_ols_exactly():
    """With k = 1 and linear learners on the same features, the residual-on-residual coefficient is the
    OLS coefficient of T in the regression of Y on (T, features) (Frisch-Waugh-Lovell)."""
    rng = random.Random(2)
    feats = lambda v: [Fr(1), v, v * v]
    for _ in range(40):
        n = rng.randint(6, 14)
        x = [Fr(rng.randint(-5, 5), 3) for _ in range(n)]
        t = [Fr(rng.randint(-4, 4)) for _ in range(n)]
        y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        rows = [[ti] + feats(v) for ti, v in zip(t, x)]
        p = len(rows[0])
        xtx = [[sum(r[a] * r[b] for r in rows) for b in range(p)] for a in range(p)]
        xty = [sum(r[a] * yi for r, yi in zip(rows, y)) for a in range(p)]
        try:
            ols = solve(xtx, xty)[0]
        except ValueError:
            continue
        r = dml_plr(x, t, y, linear_learner(feats), k=1)
        assert r.estimate == ols


def test_folds_are_balanced():
    for n in (5, 10, 37):
        for k in (1, 2, 3, 5):
            lab = make_folds(n, k, random.Random(n * k))
            sizes = [lab.count(f) for f in range(k)]
            assert sum(sizes) == n and max(sizes) - min(sizes) <= 1
    with pytest.raises(ValueError):
        make_folds(3, 4, None)


def test_cross_fitting_keeps_own_outcome_out_of_nuisances():
    """Raising y_i by 1 changes psi_i by exactly 1/e_i (treated) and no other unit of its fold."""
    rng = random.Random(3)
    n = 30
    x = [Fr(rng.randint(0, 20), 20) for _ in range(n)]
    t = [i % 2 for i in range(n)]
    y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
    lin = linear_learner(lambda v: [Fr(1), v])
    prop = oracle_learner(lambda v: Fr(1, 4) + v / 2)
    base = dml_ate(x, t, y, lin, prop, k=3, rng=random.Random(7))
    lab = make_folds(n, 3, random.Random(7))
    i = 1  # a treated unit
    y2 = list(y)
    y2[i] += 1
    new = dml_ate(x, t, y2, lin, prop, k=3, rng=random.Random(7))
    assert new.scores[i] - base.scores[i] == 1 / (Fr(1, 4) + x[i] / 2)
    for j in range(n):
        if j != i and lab[j] == lab[i]:
            assert new.scores[j] == base.scores[j]
    # without cross-fitting the fitted outcome model moves, so other scores change too
    a = dml_ate(x, t, y, lin, prop, k=1)
    b = dml_ate(x, t, y2, lin, prop, k=1)
    assert any(a.scores[j] != b.scores[j] for j in range(n) if j != i)


def expit(z):
    return 1 / (1 + math.exp(-z))


def sim_ate(n, rng):
    x, t, y = [], [], []
    for _ in range(n):
        xi = rng.random()
        ti = 1 if rng.random() < expit(-2 + 4 * xi) else 0
        x.append(xi), t.append(ti), y.append(xi + 2 * xi * xi + ti * (1 + xi) + rng.gauss(0, 1))
    return x, t, y


def test_debiasing_with_a_coarse_outcome_learner():
    """r = 40 samples, n = 1000 (seed 2026), true ATE 1.5. Outcome learner: 2 bins (badly biased);
    propensity learner: 10 bins. The plug-in regression is off by more than 0.15 on average;
    DML is within 4 SE + 0.03 of 1.5."""
    rng = random.Random(2026)
    dml, plug = [], []
    r = 40
    for _ in range(r):
        x, t, y = sim_ate(1000, rng)
        res = dml_ate(x, t, y, binned_learner(2), binned_learner(10), k=5, rng=random.Random(1))
        dml.append(res.estimate)
        m1 = binned_learner(2)([v for v, ti in zip(x, t) if ti], [yi for yi, ti in zip(y, t) if ti])
        m0 = binned_learner(2)([v for v, ti in zip(x, t) if not ti], [yi for yi, ti in zip(y, t) if not ti])
        plug.append(sum(m1(v) - m0(v) for v in x) / len(x))
    assert abs(statistics.mean(dml) - 1.5) < 4 * statistics.stdev(dml) / math.sqrt(r) + 0.03
    assert statistics.mean(plug) - 1.5 > 0.15


def test_cross_fitted_close_to_full_sample_aipw():
    """Stated tolerance: over 20 samples of n = 1000 (seed 5), the mean absolute difference between
    the cross-fitted (k = 5) and the full-sample (k = 1) estimates with 10-bin learners is below 0.03."""
    rng = random.Random(5)
    diffs = []
    for _ in range(20):
        x, t, y = sim_ate(1000, rng)
        cf = dml_ate(x, t, y, binned_learner(10), binned_learner(10), k=5, rng=random.Random(1))
        full = dml_ate(x, t, y, binned_learner(10), binned_learner(10), k=1)
        diffs.append(abs(cf.estimate - full.estimate))
    assert statistics.mean(diffs) < 0.03


def test_partially_linear_model():
    """Y = 0.5 T + 2 cos(2 pi X) + noise, T = cos(2 pi X) + noise. Linear-in-x OLS is biased (about 1.17);
    DML with 20-bin learners is within 4 SE + 0.03 of 0.5 over r = 30 samples of n = 1000 (seed 9)."""
    rng = random.Random(9)
    est, ols = [], []
    for _ in range(30):
        x, t, y = [], [], []
        for _ in range(1000):
            xi = rng.random()
            ti = math.cos(2 * math.pi * xi) + rng.gauss(0, 1)
            x.append(xi), t.append(ti), y.append(0.5 * ti + 2 * math.cos(2 * math.pi * xi) + rng.gauss(0, 1))
        est.append(dml_plr(x, t, y, binned_learner(20), k=5, rng=random.Random(1)).estimate)
        ols.append(dml_plr(x, t, y, linear_learner(lambda v: [1.0, v]), k=1).estimate)
    assert abs(statistics.mean(est) - 0.5) < 4 * statistics.stdev(est) / math.sqrt(30) + 0.03
    assert statistics.mean(ols) > 1.0


def test_input_checks():
    with pytest.raises(ValueError):
        dml_ate([0.1, 0.2], [1, 1], [1.0, 2.0], binned_learner(2), binned_learner(2), k=1)
    with pytest.raises(ValueError):
        xs = [Fr(1, 10), Fr(2, 10), Fr(3, 10)]
        ts = [Fr(1), Fr(2), Fr(3)]  # T is an exact linear function of X: no treatment residual is left
        dml_plr(xs, ts, [Fr(1), Fr(5), Fr(2)], oracle_learner(lambda v: v), k=1, treatment_learner=linear_learner(lambda v: [Fr(1), v]))
