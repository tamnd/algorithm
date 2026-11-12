# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/likelihood-weighting/. The authors are listed in prov/S0B2H9.jsonl.

import math
import random
from fractions import Fraction as F

from likelihood_weighting import (effective_sample_size, exact_posterior, likelihood_weighting,
                                  proposal_distribution, sprinkler, weighted_sample)

EVIDENCE = [{"C": 1, "W": 1}, {"W": 1}, {"S": 1, "W": 1}]


class Fixed:
    def __init__(self, us):
        self.us = list(us)

    def random(self):
        return self.us.pop(0)


def test_trace_of_the_page():
    order = ["C", "S", "R", "W"]
    net = sprinkler()
    e = {"C": 1, "W": 1}
    x, w = weighted_sample(net, e, Fixed([0.30, 0.95]), order)
    assert (x["S"], x["R"]) == (0, 1) and math.isclose(w, 0.45)
    x, w = weighted_sample(net, e, Fixed([0.95, 0.30]), order)
    assert (x["S"], x["R"]) == (1, 1) and math.isclose(w, 0.495)
    x, w = weighted_sample(net, e, Fixed([0.40, 0.10]), order)
    assert (x["S"], x["R"]) == (0, 0) and w == 0


def test_exact_values_of_the_page():
    post, pe = exact_posterior(sprinkler(F), "R", {"C": 1, "W": 1})
    assert post[1] == F(202, 207) and pe == F(1863, 5000)


def test_weight_is_exactly_unbiased_for_p_of_e():
    # E_q[w] = sum over all samples of the mutilated network of q(x) w(x) = P(e), in exact arithmetic.
    net = sprinkler(F)
    for e in EVIDENCE:
        dist = proposal_distribution(net, e)
        assert sum(q for _, q, _ in dist) == 1
        assert sum(q * w for _, q, w in dist) == exact_posterior(net, "R", e)[1]
        # and q(x) w(x) is the joint P(x), so the weighted samples have the posterior as target
        for x, q, w in dist:
            p = 1
            for v, ps in net["parents"].items():
                p *= net["cpt"][v][tuple(x[a] for a in ps)][x[v]]
            assert q * w == p


def test_self_normalized_estimate_is_biased_for_one_sample():
    # With s = 1 the weight cancels, so the estimate has mean q(R = 1), not P(R = 1 | e).
    net = sprinkler(F)
    e = {"W": 1}
    dist = proposal_distribution(net, e)
    mean1 = sum(q for x, q, w in dist if x["R"] == 1)
    assert mean1 == F(1, 2)
    assert exact_posterior(net, "R", e)[0][1] == F(509, 719)


def test_seeded_convergence_to_exact_posteriors():
    s = 20000
    for i, e in enumerate(EVIDENCE):
        exact, pe = exact_posterior(sprinkler(F), "R", e)
        for query in ("R", "C"):
            want = exact_posterior(sprinkler(F), query, e)[0]
            est, zhat, ws = likelihood_weighting(sprinkler(), query, e, s, random.Random(10 + i))
            if query in e:
                continue
            assert abs(est[1] - float(want[1])) < 0.02
        # the mean weight estimates P(e) within four standard errors
        m = sum(ws) / s
        sd = math.sqrt(sum((w - m) ** 2 for w in ws) / (s - 1) / s)
        assert abs(zhat - float(pe)) < 4 * sd
        assert 0 < effective_sample_size(ws) <= s


def test_no_evidence_is_ancestral_sampling():
    est, zhat, ws = likelihood_weighting(sprinkler(), "W", {}, 2000, random.Random(5))
    assert all(w == 1 for w in ws) and zhat == 1.0
    assert math.isclose(effective_sample_size(ws), 2000)
