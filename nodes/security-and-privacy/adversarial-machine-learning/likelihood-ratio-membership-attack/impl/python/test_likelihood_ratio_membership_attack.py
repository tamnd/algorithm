# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/likelihood-ratio-membership-attack/. The authors are listed in prov/CGYJMS.jsonl.

"""Tests of the likelihood ratio membership attack on logistic models trained on seeded synthetic blobs."""

import math
import random
import statistics

from mlkit import make_blobs, sigmoid, train_logistic
from likelihood_ratio_membership_attack import (
    best_advantage,
    decide,
    lira_scores,
    logit_confidence,
    offline_score,
    online_score,
    tpr_at_fpr,
    train_shadows,
)


def test_example_of_the_page() -> None:
    assert abs(online_score(2.5, [2.0, 3.0, 4.0], [0.0, 1.0, 2.0]) - 1.5) < 1e-12
    assert abs(online_score(4.5, [5.0, 6.0, 7.0], [3.0, 4.0, 5.0]) + 1.5) < 1e-12
    assert abs(offline_score(2.5, [0.0, 1.0, 2.0]) - 0.9669037101389033) < 1e-12
    assert decide(1.5, 0.0) and not decide(-1.5, 0.0)


def test_logit_confidence_is_the_log_odds() -> None:
    rng = random.Random(7405)
    for _ in range(500):
        d = rng.randint(1, 8)
        w = [rng.uniform(-2, 2) for _ in range(d)]
        b = rng.uniform(-1, 1)
        x = [rng.uniform(-2, 2) for _ in range(d)]
        y = rng.randint(0, 1)
        p = sigmoid(sum(a * c for a, c in zip(w, x)) + b)
        c = p if y == 1 else 1 - p
        assert abs(logit_confidence((w, b), x, y) - math.log(c / (1 - c))) < 1e-9


def test_scores_match_an_independent_normal_oracle() -> None:
    rng = random.Random(7406)
    checked = 0
    while checked < 500:
        ins = [rng.gauss(rng.uniform(-3, 3), rng.uniform(0.5, 2)) for _ in range(rng.randint(2, 9))]
        outs = [rng.gauss(rng.uniform(-3, 3), rng.uniform(0.5, 2)) for _ in range(rng.randint(2, 9))]
        if statistics.pvariance(ins) < 0.25 or statistics.pvariance(outs) < 0.25:
            continue  # so that no density underflows to 0 for |phi| <= 5
        checked += 1
        phi = rng.uniform(-5, 5)
        n_in = statistics.NormalDist(statistics.fmean(ins), math.sqrt(statistics.pvariance(ins)))
        n_out = statistics.NormalDist(statistics.fmean(outs), math.sqrt(statistics.pvariance(outs)))
        expect = math.log(n_in.pdf(phi)) - math.log(n_out.pdf(phi))
        assert abs(online_score(phi, ins, outs) - expect) < 1e-8 * max(1.0, abs(expect))
        assert abs(offline_score(phi, outs) - n_out.cdf(phi)) < 1e-9
        v = rng.uniform(0.1, 3)
        fixed = math.log(statistics.NormalDist(n_in.mean, math.sqrt(v)).pdf(phi)) - math.log(
            statistics.NormalDist(n_out.mean, math.sqrt(v)).pdf(phi)
        )
        assert abs(online_score(phi, ins, outs, v, v) - fixed) < 1e-8 * max(1.0, abs(fixed))


def test_shadow_models_are_balanced_and_trained_on_their_masks() -> None:
    rng = random.Random(7407)
    centers = [[0.3] * 3, [-0.3] * 3]
    pool = make_blobs(rng, 12, 3, centers, 1.5)
    models, masks = train_shadows(pool, 3, rng, 20, 1.0, 0.0)
    assert len(models) == 6
    for i in range(12):
        assert sum(mk[i] for mk in masks) == 3
    for g, mk in zip(models, masks):
        assert sum(mk) == 6
        assert g == train_logistic([pool[i] for i in range(12) if mk[i]], 20, 1.0, 0.0)


def run_game(seed: int, ignore_data: bool) -> tuple[list[float], list[float], list[float], list[float]]:
    """32 models in 16 pairs; each is the target once, with the 30 models of the other pairs as shadows.

    Returns the LiRA and the raw phi scores of members and nonmembers. Leaving out the
    partner of the target gives every record 15 IN and 15 OUT values.
    """
    rng = random.Random(seed)
    d, m = 8, 32
    centers = [[0.3] * d, [-0.3] * d]
    pool = make_blobs(rng, m, d, centers, 1.5)
    models, masks = train_shadows(pool, 16, rng, 200, 1.0, 0.0)
    if ignore_data:
        models = [train_logistic(make_blobs(rng, m // 2, d, centers, 1.5), 200, 1.0, 0.0) for _ in models]
    lin, lout, pin, pout = [], [], [], []
    for j, target in enumerate(models):
        others = [q for q in range(len(models)) if q // 2 != j // 2]
        s = lira_scores(target, [models[q] for q in others], [masks[q] for q in others], pool, True)
        for i, (x, y) in enumerate(pool):
            phi = logit_confidence(target, x, y)
            if masks[j][i]:
                lin.append(s[i])
                pin.append(phi)
            else:
                lout.append(s[i])
                pout.append(phi)
    return lin, lout, pin, pout


def test_lira_beats_a_global_threshold_at_low_fpr() -> None:
    """A measurement: the per-record ratio finds members at FPR 1 percent where one threshold on phi does not."""
    lin, lout, pin, pout = run_game(7401, False)
    lira_low, base_low = tpr_at_fpr(lin, lout, 0.01), tpr_at_fpr(pin, pout, 0.01)
    assert lira_low >= 0.04 and lira_low >= 4 * base_low
    assert best_advantage(lin, lout) >= 0.2 and best_advantage(pin, pout) >= 0.2


def test_a_model_that_ignores_its_data_gives_about_zero_advantage() -> None:
    lin, lout, _, _ = run_game(7401, True)
    tpr = sum(decide(s, 0.0) for s in lin) / len(lin)
    fpr = sum(decide(s, 0.0) for s in lout) / len(lout)
    assert abs(tpr - fpr) <= 0.1
    assert tpr_at_fpr(lin, lout, 0.01) <= 0.03
