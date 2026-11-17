# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/base-quality-score-recalibration/. The authors are listed in prov/X92GPF.jsonl.

import math
import os
import random

import pytest

from base_quality_score_recalibration import (Obs, covariates, empirical_q, fit, recalibrate_read,
                                              recalibrated_q)


def counted(group, q, cycle, context, n, m):
    return [Obs(group, q, cycle, context, i < m) for i in range(n)]


def test_empirical_q():
    assert abs(empirical_q(9, 9998) - 30.0) < 1e-12
    assert abs(empirical_q(0, 0) - 10 * math.log10(2)) < 1e-12


def test_page_example():
    obs = counted("g", 30, 0, None, 9998, 9) + counted("g", 30, 1, None, 9998, 99)
    t = fit(obs)
    assert abs(t.d0("g") - (-10 * math.log10(109 / 19998) - 30)) < 1e-12
    assert abs(t.d0("g") - (-7.3644)) < 1e-4
    assert abs(t.d1("g", 30)) < 1e-12
    assert abs(recalibrated_q(t, "g", 30, 0, None) - 30) < 1e-9
    assert abs(recalibrated_q(t, "g", 30, 1, None) - 20) < 1e-9
    assert recalibrate_read(t, "g", "AC", [30, 30]) == [30, 20]
    # A group or a bin that was never seen keeps the reported quality or adds nothing.
    assert recalibrated_q(t, "other", 25, 0, None) == 25
    assert abs(recalibrated_q(t, "g", 30, 7, None) - (30 + t.d0("g"))) < 1e-9


def test_one_covariate_gives_the_bin_quality():
    # With no context, the sum telescopes to the empirical quality of the (q, cycle) bin.
    rng = random.Random(3)
    obs = [Obs("g", rng.choice((10, 20, 30)), rng.randrange(5), None, rng.random() < 0.02)
           for _ in range(5000)]
    t = fit(obs)
    for q in (10, 20, 30):
        for c in range(5):
            key = ("cycle", "g", q, c)
            if key in t.counts:
                m, n = t.counts[key]
                assert abs(recalibrated_q(t, "g", q, c, None) - empirical_q(m, n)) < 1e-9


def test_two_covariates_telescope():
    # Q + d0 + d1 is the quality of the q bin, so the sum is Qe(q, cycle) + Qe(q, context) - Qe(q).
    rng = random.Random(8)
    obs = simulate(rng, 300)
    t = fit(obs)
    for o in obs[:2000]:
        if o.context is None:
            continue
        def e(key):
            m, n = t.counts[key]
            return empirical_q(m, n)
        want = e(("cycle", "lane1", o.q, o.cycle)) + e(("context", "lane1", o.q, o.context)) - e(("q", "lane1", o.q))
        assert abs(recalibrated_q(t, o.group, o.q, o.cycle, o.context) - want) < 1e-9


def test_covariates():
    assert covariates("ACG") == [(0, None), (1, "AC"), (2, "CG")]


def simulate(rng, n_reads, length=40):
    """Reads whose true error rate grows with the cycle and is higher after a G."""
    obs = []
    for _ in range(n_reads):
        bases = "".join(rng.choice("ACGT") for _ in range(length))
        for (cycle, ctx), b in zip(covariates(bases), bases):
            q = rng.choice((20, 30, 40))
            p = 10 ** (-q / 10) * (1 + cycle / 8) * (3 if ctx and ctx[0] == "G" else 1)
            obs.append(Obs("lane1", q, cycle, ctx, rng.random() < min(p, 0.5)))
    return obs


def log_loss(obs, qual):
    s = 0.0
    for o in obs:
        p = 10 ** (-qual(o) / 10)
        s -= math.log(p if o.mismatch else 1 - p)
    return s / len(obs)


def test_recalibration_improves_calibration():
    rng = random.Random(11)
    train, test = simulate(rng, 4000), simulate(rng, 2000)
    t = fit(train)
    reported = log_loss(test, lambda o: o.q)
    recal = log_loss(test, lambda o: max(1, min(93, round(recalibrated_q(t, o.group, o.q, o.cycle, o.context)))))
    assert recal < reported
    # The reported Q30 bases are near Q23 in truth. The add-one counts in the small cycle bins
    # push the estimated error rate up a little; the bias shrinks as the training data grows.
    q30 = [o for o in test if o.q == 30]
    true_p = sum(1e-3 * (1 + o.cycle / 8) * (3 if o.context and o.context[0] == "G" else 1) for o in q30) / len(q30)
    mean_p = sum(10 ** (-recalibrated_q(t, o.group, o.q, o.cycle, o.context) / 10) for o in q30) / len(q30)
    assert 30 + 10 * math.log10(true_p) > 5
    assert abs(-10 * math.log10(true_p) - -10 * math.log10(mean_p)) < 1.5


def test_clamping():
    t = fit(counted("g", 40, 0, None, 50, 40))
    assert recalibrate_read(t, "g", "A", [40]) == [1]
    t = fit(counted("g", 40, 0, None, 50, 50))
    assert recalibrated_q(t, "g", 40, 0, None) < 1 and recalibrate_read(t, "g", "A", [40]) == [1]
    t = fit(counted("g", 2, 0, None, 10 ** 5, 0))
    assert recalibrate_read(t, "g", "A", [2]) == [50]


if __name__ == "__main__":
    raise SystemExit(pytest.main([os.path.abspath(__file__), "-q"]))
